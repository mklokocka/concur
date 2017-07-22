import requests
import requests_cache
from datetime import timedelta
from flask import Flask, request, jsonify, abort, make_response
from babel.numbers import get_currency_symbol

# Use a free API for the rates, better and more comprehensive ones are paid.
RATES_URL = 'http://api.fixer.io/latest'

# Set up caching
expiration = timedelta(hours=1)
requests_cache.install_cache(expire_after=expiration, old_data_on_error=True)

# Set up conversion table
conversion_table = {
    'EUR': 1
}

# Set up the currency symbol table
euro_symbol = get_currency_symbol('EUR', locale='en_US')

symbol_table = {
    euro_symbol: ['EUR']
}

app = Flask(__name__)


# Handle 400 with a json.
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


# Handle 504 with a json.
@app.errorhandler(504)
def timeout(error):
    return make_response(jsonify({'error': 'External API timeout'}), 504)


# Makes sure we have the current exchange rates.
def update_rates():
    try:
        resp = requests.get(RATES_URL, timeout=0.1)
    except requests.Timeout:
        abort(504)

    if not resp.from_cache:
        rates_data = resp.json()
        for cur, value in rates_data['rates'].items():
            # Add the currency to our conversion table.
            conversion_table[cur] = value

            # Add the currency to our symbol table.
            symbol = get_currency_symbol(cur, locale='en_US')
            symbol_table.setdefault(symbol, []).append(cur)


# The main part of the API, converts currencies.
@app.route('/currency_converter', methods=['GET'])
def convert_endpoint():
    amount = request.args.get('amount', type=float)
    inp_cur = request.args.get('input_currency')
    out_cur = request.args.get('output_currency')

    update_rates()

    # Check if the required arguments are present.
    if amount is None or inp_cur is None:
        abort(400)
    if inp_cur not in conversion_table and inp_cur not in symbol_table:
        abort(400)

    # Create a list of input currencies.
    input_currencies = symbol_table.get(inp_cur, [inp_cur])

    # Create a list of output currencies.
    output_currencies = symbol_table.get(out_cur, [out_cur])
    if out_cur is None:
        output_currencies = conversion_table.keys()

    # Alias for the conversion table.
    ct = conversion_table
    conversions = {
        inp_cur: {
               out_cur: amount / ct[inp_cur] * ct[out_cur]
               for out_cur in output_currencies
        }
        for inp_cur in input_currencies}

    responses = [{
        'input': {
            'amount': amount,
            'currency': inp_cur
        },
        'output': results}
        for inp_cur, results in conversions.items()]

    if len(responses) == 1:
        return jsonify(responses[0])
    else:
        return jsonify(responses)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
