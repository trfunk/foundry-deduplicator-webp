# https://gist.github.com/gruber/8891611
# Doesn't check for <img> tags and similar stuff
# File check will prob struggle with umlauts, url encoding, ...
# Haven't tested with case sensitive filesystems
# No idea about symlinks

import json
from collections import defaultdict
import pathlib
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


def search_db(db, media, images, thumbs):
    # path is still hardcoded, one day it won't
    path = pathlib.Path("bgdia/data/", db)
    with open(path, "r", encoding="utf8", newline='\n') as db:
        for line in db:
            data = json.loads(line)
            if 'img' in data:
                images[data["img"]].append(data["name"])
            if 'thumb' in data:
                thumbs[data["thumb"]].append(data["name"])
            if 'sounds' in data:
                # scenes.db also has sounds as a key, but no paths in there
                try:
                    media[data["sounds"][0]["path"]].append(data["name"])
                except IndexError:
                    pass


def check_for_string(input, output, string):
    for key, value in input.items():
        if string in key:
            output[key].append(value)
    for key, value in output.items():
        input.pop(key, None)


def check_if_exists(input, missing, empty):
    for key, value in input.items():
        # "worlds/" prefix seems to be hardcoded in the foundry db
        # removing it to make the filecheck work
        key = key.removeprefix('worlds/')
        key = key.replace('%20', ' ')
        # check for empty file paths
        if not key:
            empty[key].append(value)
        elif not pathlib.Path(key).is_file():
            missing[key].append(value)


media = defaultdict(list)
images = defaultdict(list)
thumbs = defaultdict(list)
system = defaultdict(list)
url = defaultdict(list)
missing = defaultdict(list)
empty = defaultdict(list)

search_db('actors.db', media, images, thumbs)
search_db('items.db', media, images, thumbs)
search_db('journal.db', media, images, thumbs)
search_db('scenes.db', media, images, thumbs)
search_db('tables.db', media, images, thumbs)
search_db('macros.db', media, images, thumbs)
search_db('playlists.db', media, images, thumbs)

check_for_string(images, system, 'systems/dnd5e/')
check_for_string(thumbs, system, 'systems/dnd5e/')
check_for_string(media, system, 'systems/dnd5e/')

check_for_string(images, url, 'http')
check_for_string(thumbs, url, 'http')
check_for_string(media, url, 'http')

check_if_exists(images, missing, empty)
check_if_exists(thumbs, missing, empty)
check_if_exists(media, missing, empty)

print("Url:")
for k, v in url.items():
    print("{}: {}".format(k, v))
    # print(k)

print("Images:")
for k, v in images.items():
    print(k)

print("Thumbs:")
for k, v in thumbs.items():
    print(k)

print("Media:")
for k, v in media.items():
    print(k)

print("System:")
for k, v in system.items():
    print(k)

print("Missing")
for k, v in missing.items():
    print("Missing: {} -> {}".format(k, v))

print("Empty")
for k, v in empty.items():
    # Should prob iterate the v to display each token/skill/etc in a new line
    print("Empty: {} -> {}\n".format(k, v))
