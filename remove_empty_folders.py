# Deletes empty folders recursively.
# Takes a path as argument
# Yoinked from https://stackoverflow.com/a/23488980

import os
import sys


def remove_empty_dir(path):
    try:
        os.rmdir(path)
    except OSError:
        pass


def remove_empty_dirs(path):
    for root, dirnames, filenames in os.walk(path, topdown=False):
        for dirname in dirnames:
            remove_empty_dir(os.path.realpath(os.path.join(root, dirname)))


if __name__ == "__main__":
    if sys.argv[1]:
        remove_empty_dirs(sys.argv[1])
    else:
        print("Please pass the path to check as parameter to the script")
