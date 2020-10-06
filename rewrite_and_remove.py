# Hardcoded for BG:DiA, need to change stuff for other worlds
# Expects to sit one folder above the root folder of the world
# Directly edits the dbs, data corruption possible!
# Need to pass a plain text encoded textfile as argument.
# Expects .dbs in the same folder as the script.
# Tags empty files as duplicates
# Deletes duplicate files


from collections import defaultdict
import os
import pathlib
import posixpath
import sys


def fix_db(db, duplicates):
    # rewrites the img references to the non duplicates we won't delete
    input_filepath = pathlib.Path("bgdia/data/", db)
    # remove hardcoded mess
    output_filepath = pathlib.Path("bgdia/data/", db + '2')
    with open(input_filepath, "r", encoding="utf8", newline='\n') as input_db:
        with open(output, "w", encoding="utf8", newline='\n') as output_db:
            data = input_db.read()
            for filename, lists in duplicates.items():
                for duplicate in lists:
                    data = data.replace(duplicate, filename)
            output_db.write(data)


def fix_format(line):

    # split a dedup.txt line into the filename and the duplicate
    filename, duplicate = line.split(",")
    # since the list produces the absolute path we have to slice of
    filename = fix_path(filename)
    # everything that isn't relative to the world's root folder
    duplicate = fix_path(duplicate)
    return filename, duplicate


def fix_path(path):
    path = os.path.relpath(path)
	# replace the windows seperator with the linux one
    path = path.replace(os.sep, posixpath.sep)
    path = path.partition('/')[-1]
    return path



def fix_and_delete(dedup_file):
    # slapping all the paths into a dictonary with the 'chosen' original file as key
    duplicates = defaultdict(list)
    # and all others as values : {filename: {duplicate1, duplicate2}, ...}
    with open(dedup_file, 'r', encoding="utf8") as file_object:
        for cnt, line in enumerate(file_object):
            filename, duplicate = fix_format(line.rstrip())
            # remove newlines
            duplicates[duplicate].append(filename)
        fix_db('actors.db', duplicates)
        fix_db('items.db', duplicates)
        fix_db('journal.db', duplicates)
        fix_db('scenes.db', duplicates)
        fix_db('tables.db', duplicates)
        print('Fixed DBs')
        remove_duplicates(duplicates)


def remove_duplicates(duplicates):
    for filename, lists in duplicates.items():
        for duplicate in lists:
            # assemble a full path again so we can delete the duplicates
            duplicated_img = pathlib.Path(os.getcwd(), 'bgdia/', duplicate)
            duplicated_img.unlink()


if __name__ == "__main__":
    print("current working dir: " + os.getcwd())
    if sys.argv[1]:
        fix_and_delete(sys.argv[1])
    else:
        print("Please pass the file with the deduplication paths.")
