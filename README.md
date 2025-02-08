# Korapay CLI

[![Downloads](https://static.pepy.tech/badge/korapay-cli)](https://pepy.tech/project/korapay-cli)
[![Downloads](https://static.pepy.tech/badge/korapay-cli/month)](https://pepy.tech/project/korapay-cli)
[![Downloads](https://static.pepy.tech/badge/korapay-cli/week)](https://pepy.tech/project/korapay-cli)

A command line app for interacting with [Korapay's](https://www.korahq.com/) API. Built with
[Typer](https://typer.tiangolo.com/) and [korapay-client](https://gray-adeyi.github.io/korapay_client/v0.1/)

## Installation

Korapay CLI can be installed from pypi with pip as shown below.

```bash
pip install korapay-cli
```
or with [uv](https://docs.astral.sh/uv/)
```bash
uv tool install korapay-cli
```

## First time configurations

You're required to add your korapay integration credentials (i.e. public key,secret key and encryption key) to the cli 
on first use as shown below.  This package provides `korapay` and `kp` as the cli's entry point

```bash
korapay config crendtials
# or
kp config crendtials
```

This sets up your korapay cli for use in development mode if the test secret key is used. This credentials can be
removed with `korapay reset` or `kp reset`. The credentials are stored in `$HOME/.config/.korapay-cli/.settings.json`
for mac and linux and `C:\Users\<user>\AppData\Local\.korapay-cli/.settings.json` on windows

Run `korapay --help` or `kp --help` to see available commands

## Examples

### Resolve an account number

```bash
# kp or korapay resolve-bank-account [BANK_CODE] [ACCOUNT_NUMBER]
kp resolve-bank-account 214 5273681014
```

Running the command above should yield a result similar to the dump shown below

```bash
Response(status_code=200, status=True, message='Request completed', data={'bank_name': 'FCMB Plc', 'bank_code': '214', 'account_number': '5273681014', 'account_name': 'ADEYI GBENGA MICHAEL'})
```

By default, the results you get from the cli is a `Response` object which is a pydantic model returned
by [korapay-client](https://gray-adeyi.github.io/korapay-client/). To get a json result, use the `--json`
flag.

```bash
# kp or korapay resolve-bank-account [BANK_CODE] [ACCOUNT_NUMBER]
kp resolve-bank-account 214 5273681014 --json
```

Running the command above should yield a result similar to the dump shown below

```bash
{"bank_name": "FCMB Plc", "bank_code": "214", "account_number": "5273681014", "account_name": "ADEYI GBENGA MICHAEL"}
```

## Source code

[https://github.com/gray-adeyi/korapay-cli](https://github.com/gray-adeyi/korapay-cli)
