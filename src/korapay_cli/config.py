import getpass

from korapay_cli.utils import update_settings, reset_settings
from typer import Typer
from rich import print as rprint

config_app = Typer()


@config_app.command()
def credentials():
    """Configure public key"""
    public_key = getpass.getpass("Enter your public key: ")
    secret_key = getpass.getpass("Enter your secret key: ")
    encryption_key = getpass.getpass("Enter your encryption key: ")
    update_settings(option="public_key", value=public_key)
    update_settings(option="secret_key", value=secret_key)
    update_settings(option="encryption_key", value=encryption_key)
    rprint("Credentials saved saved! :boom:")


@config_app.command()
def reset():
    """Reset credentials"""
    reset_settings()
    rprint("credentials cleared! :boom:")
