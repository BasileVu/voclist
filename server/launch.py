"""Launches the app and setup folders / load db"""

import os

__author__ = "Basile Vu <basile.vu@gmail.com>"

DB_FOLDER = "db"


def prepare_db_folder():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)


if __name__ == "__main__":
    prepare_db_folder()
