"""Runs the server for the app."""

from argparse import ArgumentParser

from voclist import app, db, setup_app

__author__ = "Basile Vu <basile.vu@gmail.com>"


if __name__ == "__main__":
    setup_app("config/voclist.cfg")

    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="port to use for the server", default=5000)
    parser.add_argument("--host", type=str, help="address for the server to listen on", default="127.0.0.1")

    db.create_all()
    app.run(**vars(parser.parse_args()))
