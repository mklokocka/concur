import click
import requests
import json
from collections import OrderedDict

URL_BASE = 'http://{0}:8080/currency_converter'


@click.command()
@click.option('--amount', type=click.FLOAT, help='Amount to convert.')
@click.option('--input-currency', help='The currency to convert from.')
@click.option('--output-currency', default=None,
              help='Optional. The currency to convert to.')
@click.option('--host', default='localhost',
              help='Optional. The host hosting the conversion API.')
def convert(amount, input_currency, output_currency, host):
    """"A program for converting currencies."""
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
        resp = requests.get(URL_BASE.format(host), params=params, timeout=0.1)
        resp.raise_for_status()
    except requests.HTTPError:
        raise click.UsageError('Did you enter the right amount and '
                               'correct currency codes?')
    except requests.exceptions.Timeout:
        raise click.UsageError('Timeout. Did you provide a correct host?')

    # Convert the response text into json with a preserved order for printing.
    ordered_resp = json.loads(resp.text, object_pairs_hook=OrderedDict)
    print(json.dumps(ordered_resp, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    convert()
