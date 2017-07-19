from flask import Flask, request, jsonify, abort, make_response

app = Flask(__name__)

# Trivial conversion table for now.
# TODO: Replace with a DB for retrieving and caching of actual rates.
conversion_table = {
    'CZK': 1,
    'USD': 0.044,
    'EUR': 0.038
}


# Handle 400 with a json.
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


# The main part of the API, converts currencies.
@app.route('/currency_converter', methods=['GET'])
def convert():
    amount = request.args.get('amount', type=int)
    inp_cur = request.args.get('input_currency')
    out_cur = request.args.get('output_currency')

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
    app.run(debug=True)
