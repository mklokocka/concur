import click
import requests
import json
from collections import OrderedDict

URL_BASE = 'http://localhost:8080/currency_converter'


@click.command()
@click.option('--amount', type=click.FLOAT)
@click.option('--input-currency')
@click.option('--output-currency', default=None)
def convert(amount, input_currency, output_currency):
    if amount is None:
        raise click.UsageError('Amount to convert argument required.')
    if input_currency is None:
        raise click.UsageError('Input currency argument required.')

    params = {
        'amount': amount,
        'input_currency': input_currency
    }

    if output_currency is not None:
        params['output_currency'] = output_currency

    try:
        resp = requests.get(URL_BASE, params=params)
        resp.raise_for_status()
    except requests.HTTPError:
        raise click.UsageError('Did you enter the right amount and '
                               'correct currency codes?')

    # Convert the response text into json with a preserved order for printing.
    ordered_resp = json.loads(resp.text, object_pairs_hook=OrderedDict)
    print(json.dumps(ordered_resp, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    convert()
