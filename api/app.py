import requests
import requests_cache
from datetime import timedelta
from flask import Flask, request, jsonify, abort, make_response

# Use a free API for the rates, better and more comprehensive ones are paid.
RATES_URL = 'http://api.fixer.io/latest'

# Set up caching
expiration = timedelta(days=1)
requests_cache.install_cache(expire_after=expiration, old_data_on_error=True)

# Set up conversion table
conversion_table = {
    'EUR': 1
}

app = Flask(__name__)


# Handle 400 with a json.
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


# Makes sure we have the current exchange rates.
def update_rates():
    resp = requests.get(RATES_URL, timeout=0.1)

    rates_data = resp.json()
    for cur, value in rates_data['rates'].items():
        conversion_table[cur] = value


# The main part of the API, converts currencies.
@app.route('/currency_converter', methods=['GET'])
def convert():
    amount = request.args.get('amount', type=float)
    inp_cur = request.args.get('input_currency')
    out_cur = request.args.get('output_currency')

    update_rates()

    # Check if the required arguments are present.
    if amount is None or inp_cur is None:
        abort(400)
    if inp_cur not in conversion_table:
        abort(400)

    # Prepare the basis of the JSON response.
    response = {
        'input': {
            'amount': amount,
            'currency': inp_cur,
        }
    }
    if out_cur is not None:
        if out_cur not in conversion_table:
            abort(400)

        result = amount / conversion_table[inp_cur] * conversion_table[out_cur]
        response['output'] = {
            out_cur: format(result, '.2f')
        }
    else:
        response['output'] = {}
        for cur in conversion_table.keys():
            result = amount / conversion_table[inp_cur] * conversion_table[cur]
            response['output'][cur] = format(result, '.2f')

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
