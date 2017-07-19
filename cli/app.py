import click
import requests
import json
from collections import OrderedDict


# Method defining the url of the host serving the API.
def url_base():
    return 'http://localhost:5000'


# Helper function for formatting the request URL.
def format_url(amount, input_currency, output_currency=None):
    url = url_base() + '/currency_converter?amount=%d&input_currency=%s'\
                            % (amount, input_currency)
    if output_currency is not None:
        url = url + '&output_currency=%s' % output_currency

    return url


@click.command()
@click.option('--amount', type=click.FLOAT)
@click.option('--input-currency')
@click.option('--output-currency', default=None)
def convert(amount, input_currency, output_currency):
    if amount is None:
        raise click.UsageError('Amount to convert argument required.')
    if input_currency is None:
        raise click.UsageError('Input currency argument required.')

    resp = requests.get(format_url(amount, input_currency, output_currency))

    # Check for error, inform the user of them.
    if resp.status_code != 200:
        if resp.status_code == 400:
            raise click.UsageError('Did you enter the right amount and '
                                   'correct currency codes?')

    # Convert the response text into json with a preserved order for printing.
    ordered_resp = json.loads(resp.text, object_pairs_hook=OrderedDict)
    print(json.dumps(ordered_resp, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    convert()
