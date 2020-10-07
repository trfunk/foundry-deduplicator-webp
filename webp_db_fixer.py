# This script is hardcoded for BG:DiA! You need to change it for other worlds
# You need to convert the pngs to webps (both need to be present) before running this
# It expects to sit one folder above the module
# The dbs need to be copied to the folder the script is to prevent data loss
# Partly stolen from https://stackoverflow.com/a/38514560

import glob
import os
import pathlib
import posixpath
import sys


def fix_db(db, replacement):
    input_filepath = pathlib.Path("bgdia/data/", db + '2')
    output_filepath = pathlib.Path("bgdia/data/", db + '3')
    with open(input_filepath, "r", encoding="utf8", newline='\n') as input_db:
        with open(output_filepath, "w", encoding="utf8", newline='\n') as output_db:
            data = input_db.read()
            for original, webp in replacement.items():
                data = data.replace(original, webp)
            # catching Tokenwildcards
            data = data.replace("*.png", "*.webp")
            data = data.replace("*.jpg", "*.webp")
            data = data.replace("*.jpeg", "*.webp")
            output_db.write(data)


def find_pngs(path, replacement):
    # find all .pngs (while traversing subdirectories)
    for file in glob.glob(path + '/**/*.png', recursive=True):
        # convert to linux path
        file = file.replace(os.sep, posixpath.sep)
        # slice the worlds root folder off
        file = file.split('/', 1)[-1]
        # create dictonary with the path to the png as key and the path to the webp as value
        replacement[file] = file.replace('.png', '.webp')


def find_jpgs(path, replacement):
    for file in glob.glob(path + '/**/*.jpg', recursive=True):
        file = file.replace(os.sep, posixpath.sep)
        file = file.split('/', 1)[-1]
        replacement[file] = file.replace('.jpg', '.webp')
    # jpegs aswell
    for file in glob.glob(path + '/**/*.jpeg', recursive=True):
        file = file.replace(os.sep, posixpath.sep)
        file = file.split('/', 1)[-1]
        replacement[file] = file.replace('.jpeg', '.webp')


def fix(path):
    replacement = {}
    find_pngs(path, replacement)
    find_jpgs(path, replacement)
    fix_db('actors.db', replacement)
    fix_db('items.db', replacement)
    fix_db('journal.db', replacement)
    fix_db('scenes.db', replacement)
    fix_db('tables.db', replacement)
    print('Fixed DBs')
    remove_duplicates(replacement)


def remove_duplicates(replacement):
    for png, webp in replacement.items():
        # add the worlds root folder back, so they're actually valid paths (!!!BGDIA HARDCODED)
        duplicated_png = pathlib.Path("bgdia/", png)
        duplicated_png.unlink()


if __name__ == "__main__":
    if sys.argv[1]:
        fix(sys.argv[1])
    else:
        print("Please pass the path to check as parameter to the script")
