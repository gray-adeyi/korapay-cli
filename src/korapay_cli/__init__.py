from korapay_cli.korapay import root_app
from korapay_cli.config import config_app

root_app.add_typer(config_app, name="config")


def run():
    root_app()


if __name__ == "__main__":
    run()
