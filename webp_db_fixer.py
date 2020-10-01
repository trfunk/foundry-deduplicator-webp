# This script is hardcoded for BG:DiA! You need to change it for other worlds
# You need to convert the pngs to webps (both need to be present) before running this
# It expects to sit one folder above the module
# The dbs need to be copied to the folder the script is to prevent data loss
# Partly stolen from https://stackoverflow.com/a/38514560

import glob
import os
import pathlib
import posixpath


def fix_db(db, replacement):									# rewriting all .png links to .webp links
	output = db + '2'
	with open(db, "r", encoding="utf8", newline='\n') as input_db:
		with open(output, "w", encoding="utf8", newline='\n') as output_db:
			data = input_db.read()
				data = data.replace(png, webp)
			data = data.replace("*.png","*.webp") 					# catching Tokenwildcards
			output_db.write(data)


def find_pngs():
	replacement = {}
	for file in glob.glob("**/*.png", recursive = True):					# find all .pngs (while traversing subdirectories)
		file = file.replace(os.sep, posixpath.sep)					# convert to linux path
		file = file.split('/', 1)[-1]                                         		# slice the worlds root folder off
		replacement[file] = file.replace('.png', '.webp')				# create dictonary with the path to the png as key and the path to the webp as value
	fix_db('actors.db', replacement)
	fix_db('items.db', replacement)
	fix_db('journal.db', replacement)
	fix_db('scenes.db', replacement)
	fix_db('tables.db', replacement)
	print('Fixed DBs')
	remove_duplicates(replacement)

def remove_duplicates(replacement):
	for png, webp in replacement.items():
		duplicated_png = pathlib.Path("bgdia/", png) 					# add the worlds root folder back, so they're actually valid paths (!!!BGDIA HARDCODED)
		duplicated_png.unlink() 	

if __name__ == "__main__":
	print("current working dir: " + os.getcwd())
	find_pngs()
