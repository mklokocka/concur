# concur
A simple API application enabling easy conversion of currencies and a command 
line interface to this API.

## API

The API provides an easy web service interface for converting currencies.

### Installation

The easiest way to start using the API is building a Docker image and running
image. Note that you have to expose the port 8080 to the application.

If you do not have Docker, the required Python libraries are listed in
requirements.txt and can be installed with:

```
pip install -r requirements.txt
```

It is best to use a virtualenv before installing those libraries to avoid
cluttering up your main installation.

### Usage

The server runs at the localhost:8080. You can call it as follows:

```
GET /currency_converter?amount=50&input_currency=CZK&output_currency=USD HTTP/1.1
{
    'input': {
        'amount': 50.0,
        'input_currency': 'CZK'
    }
    'output': {
        'USD': 2.24
    }
}
```

You can also omit the `output_currency` part of the call, asking for all
possible conversions:

```
GET /currency_converter?amount=21.34&input_currency=EUR HTTP/1.1
{
    'input': {
        'amount': 21.34,
        'input_currency': 'EUR'
    }
    'output': {
        'AUD': 185.22,
        'BGN': 246.45,
        'BRL': 456.46,
        ...
    }
}
```

The API also accepts currency symbols instead of currency codes. One symbol
can correspond to more than one currency (for example, $ is used very often),
therefore there can be more possibilities on which precise currency the user
meant. Therefore the API returns all possibilities:

```
GET /currency_converter?amount=50&input_currency=CZK&output_currency=$ HTTP/1.1
{
    'input': {
        'amount': 50.0,
        'input_currency': 'CZK'
    }
    'output': {
        'SGD': 3.05,
        'USD': 2.24
    }
}
```

Or:

```
GET /currency_converter?amount=234.5&input_currency=$&output_currency=AUD HTTP/1.1
[
    {
        'input': {
            'amount': 234.5,
            'input_currency': 'SGD'
        }
        'output': {
            'AUD': 217.17
        }
    },
    {
        'input': {
            'amount': 234.5,
            'input_currency': 'USD'
        }
        'output': {
            'AUD': 296.08
        }
    }
]
```

Both of those can be combined, in the case of ambiguous symbol both on input,
and on output.

## CLI

The CLI application is a client to the API given above.

### Installation

This application does not have a Dockerfile as it is a simple CLI application.
Therefore the easiest way to run it is to install all requirements, again by 
running:

```
pip install -r requirements.txt
```

### Usage

```
./app.py --amount 100 --input_currency EUR --output_currency RUB
{
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "RUB": 6861.8
    }
}
```

Of course it is only an interface to the API, passing a symbol instead of a code
provides the same responses as given above.