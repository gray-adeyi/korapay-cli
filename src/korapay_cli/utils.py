import functools
import json
import os.path
from json import JSONDecodeError
from typing import Type

import typer
from korapay_client import KorapayClient, ClientError
from rich import print as rprint
from pathlib import Path
from typer import get_app_dir

APP_CONFIG_DIR_NAME = ".korapay-cli"

CACHED_SETTINGS: dict | None = None


def get_settings_path() -> Path:
    app_dir = get_app_dir(APP_CONFIG_DIR_NAME)
    if not os.path.isdir(app_dir):
        os.mkdir(app_dir)
    return Path(app_dir) / ".settings.json"


def get_all_settings() -> dict:
    global CACHED_SETTINGS
    if CACHED_SETTINGS:
        return CACHED_SETTINGS
    settings_path = get_settings_path()
    if not settings_path.is_file():
        with settings_path.open("w+") as f:
            f.write(json.dumps({}))
    with settings_path.open("r") as f:
        CACHED_SETTINGS = json.loads(f.read())
        return CACHED_SETTINGS


def get_settings(option: str) -> str | None:
    all_settings = get_all_settings()
    return all_settings.get(option)


def update_settings(option: str, value: str):
    all_settings = get_all_settings()
    all_settings[option] = value
    settings_path = get_settings_path()
    with settings_path.open("w") as f:
        f.write(json.dumps(all_settings))


def reset_settings():
    global CACHED_SETTINGS
    CACHED_SETTINGS = None
    settings_path = get_settings_path()
    with settings_path.open("w+") as f:
        f.write(json.dumps({}))


def get_korapay_client() -> KorapayClient:
    public_key = get_settings("public_key")
    secret_key = get_settings("secret_key")
    encryption_key = get_settings("encryption_key")

    if not public_key:
        raise typer.Abort()

    if not secret_key:
        raise typer.Abort()

    if not encryption_key:
        raise typer.Abort()

    return KorapayClient(
        public_key=public_key, secret_key=secret_key, encryption_key=encryption_key
    )


def parse_cli_string(
    raw_string: str, arg_or_option_name: str, expected_type: Type, many: bool = False
):
    """parses the json encoded string gotten form the cli input to the expected type.

    Args:
        raw_string: the json decodable value passed in by the user to the cli to be parsed into the expected type.
        arg_or_option_name: the name of the cli argument or option.
        expected_type: the expected type
        many: for `expected_type` other than `list` or `dict` if what we want is a list[expected_type], many should be
            set to `True`.
    """
    try:
        parsed_data = json.loads(raw_string)
        if isinstance(parsed_data, expected_type):
            return parsed_data
        if isinstance(parsed_data, dict) and not many:
            return expected_type(**parsed_data)
        if isinstance(parsed_data, list) and many:
            return [expected_type(**item) for item in parsed_data]
    except (json.decoder.JSONDecodeError, TypeError):
        rprint(
            f"[bold red]Error![/bold red] unable to parse value in `{arg_or_option_name}` option or argument, expects a json decodable string"
            f" that can be parsed into a {'`list` of ' if many else ''}`{expected_type.__name__}` model.\nSee https://gray-adeyi.github.io/korapay_client/v0.1/api_reference/models/"
        )
        raise typer.Exit(code=1)


def colorized_print(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        rprint(response)

    return wrapper


def override_output(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except ClientError as error:
            rprint(
                f"an error occurred while making a request to korapay: error: {error}"
            )
            raise typer.Exit(code=1)
        if kwargs["json"]:
            try:
                return json.dumps(response.data)
            except (JSONDecodeError, TypeError):
                rprint(
                    f"unable to decode data as json.\ngot: data: {response.data}\nmessage: {response.message}"
                )
                raise typer.Exit(code=1)
        return response

    return wrapper
