# foundry-deduplicator-webp (DATA LOSS/CORRUPTION VERY POSSIBLE, HAVE BACKUPS, HANDLE WITH CARE)

Collection of horrible python scripts I hacked together to deduplicate files in a foundry world, delete the duplicates and rewrite the foundry databases so the world doesn't break. Optional script to rewrite all the internal .png links to .webp. Tested with exactly one world (lmao) on Foundry 0.6.6. Uses pathlib so needs modern python (I think atleast 3.4, but 3.8 is probably safer). Unsure how/if it deals with symlinks.

## Usage
### Deduplication
1. Place all the scripts one folder above the world you want to torment.
2. Run `duplicates.py` with the worlds root folder as argument. This will create a textfile called `dedup.txt` with original filename and duplicates listed as absolute paths:
```
C:\Users\trfunk\Desktop\worlds\bgdia\token\img1.png,C:\Users\trfunk\Desktop\worlds\bgdia\avatar\img3.png
C:\Users\trfunk\Desktop\worlds\bgdia\token\img1.png,C:\Users\trfunk\Desktop\worlds\bgdia\token\img124.png
                        ^ the scripts are in the world folder, bgdia folder is the argument
```
3. Copy the `actors.db`, `items.db`, `journal.db`, `scenes.db` and `tables.db` of the world into the folder the scripts are in.
4. Fix any hardcoded shit [like the worlds root folder](../main/rewrite_and_remove.py#L34-L35), [twice](../main/rewrite_and_remove.py#L56).
5. Run `rewrite_and_remove.py` with `dedup.txt` as argument.
6. Remove the `actors.db`, `items.db`, `journal.db`, `scenes.db` and `tables.db` files and rename `actors.db2`, `items.db2`, `journal.db2`, `scenes.db2` and `tables.db2` to `actors.db`, `items.db`, `journal.db`, `scenes.db` and `tables.db`.
7. Overwrite the database files in the worlds data/ folder with the newly created databases (`actors.db`, `items.db`, `journal.db`, `scenes.db` and `tables.db`).

### Webp rewriting

8. Use [VanceCole's bulk-convert-to-webp.ps1 powershell script](https://github.com/VanceCole/macros/blob/main/imagemagick/bulk-convert-to-webp.ps1) to convert all .png files to .webp (converts .gifs and .jpgs aswell, but the script won't touch these)
9. Fix some hardcoded shit like the [world's root folder name](https://github.com/trfunk/foundry-deduplicator-webp/blob/fc9ee3a315bc87fc1a5319e030cd0d9df0ee55d1/webp_db_fixer.py#L39) and run it. It again assumes the foundry .dbs (`actors.db`, `items.db`, `journal.db`, `scenes.db` and `tables.db`) to be in the same folder as the scripts
10. Remove the `actors.db`, `items.db`, `journal.db`, `scenes.db` and `tables.db` files and rename `actors.db2`, `items.db2`, `journal.db2`, `scenes.db2` and `tables.db2` to `actors.db`, `items.db`, `journal.db`, `scenes.db` and `tables.db`.
11. Overwrite the database files in the worlds data/ folder with the newly created databases (`actors.db`, `items.db`, `journal.db`, `scenes.db` and `tables.db`).

Done.

### Todo
- Fix the horrible hardcoded mess.
- `duplicate.py` probably horrible explodes dealing with non ascii letters?
- Make the db workflow less tedious
- Take on .gifs, .jpgs, etc aswell
- Integrate .webp conversation

### Do Maybe
- .mp3, .flac to opus .ogg?
- Animated .gif to .webm?
- Remove (then) empty folders
- Scan DBs for unused media files and list them (maybe delete aswell?)
- Merge into one file

### Thanks
- VanCole for his [macros](https://github.com/VanceCole/macros)
- Stackoverflow (https://stackoverflow.com/a/38514560, https://stackoverflow.com/a/36113168, https://stackoverflow.com/a/23488980)



