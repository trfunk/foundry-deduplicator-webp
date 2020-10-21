# foundry-deduplicator-webp (DATA LOSS/CORRUPTION VERY POSSIBLE, HAVE BACKUPS, HANDLE WITH CARE)

Collection of horrible python scripts I hacked together to deduplicate files in a foundry world, delete the duplicates and rewrite the foundry databases so the world doesn't break. Optional script to rewrite all the internal `.jpeg`, `.jpg` and `.png` files to `.webp`. Unsure how/if it deals with symlinks and/or Unicode characters. **Use at your own risk.**

**Tested on/with:** 
- Exactly one world (lmao)
- Foundry 0.6.6. 
- Python 3.9, 3.8.1
- Win 10 x64 

## Usage (Not up to date)
0. **Make a backup!!**

### Deduplication (Will delete duplicates)
1. Place all the scripts one folder above the world you want to torment.
2. Run `duplicates.py` with the worlds root folder as argument. This will create a textfile called `dedup.txt` with original filename and duplicates listed as absolute paths:
```
C:\Users\trfunk\Desktop\worlds\bgdia\token\img1.png,C:\Users\trfunk\Desktop\worlds\bgdia\avatar\img3.png
C:\Users\trfunk\Desktop\worlds\bgdia\token\img1.png,C:\Users\trfunk\Desktop\worlds\bgdia\token\img124.png
                        ^ the scripts are in the world folder, bgdia folder is the argument
```
3. Fix any hardcoded shit [like the worlds root folder](../main/rewrite_and_remove.py#L19-L21), [twice](../main/rewrite_and_remove.py#L72).
4. Run `rewrite_and_remove.py` with `dedup.txt` as argument.
5. If you don't want to convert the images to webp, go to the `data/` folder and rename any `.db2` files to `.db`. Overwrite if needed. Else skip this step.

### Webp rewriting (Will delete any .png, .jpg and .jpeg)
6. Use [VanceCole's bulk-convert-to-webp.ps1 powershell script](https://github.com/VanceCole/macros/blob/main/imagemagick/bulk-convert-to-webp.ps1) to convert all `.png` files to `.webp` (converts `.jpegs`, `.jpgs` and `.gifs` aswell). **Make sure this step is finished and worked before you continue with step 7. Else your world will be corrupted.**
7. Fix some hardcoded shit like the [world's root folder name](../main/webp_db_fixer.py#L15-16), ([twice](../main/webp_db_fixer.py#L15-16)). If you renamed the the `.db2` files to `.db` you will have to either rename them back, or [change the script](../main/webp_db_fixer.py#L15-16).
8. Run `webp_db_fixer.py` with the world's root folder as argument. The script will only rewrite and delete `.jpeg`, `.jpg` and `.png` files to `.webp`, since it doesn't deal with animated gifs yet.  
9. Go to the `data/` folder and rename any `.db3` files to `.db`. Overwrite if needed. Can remove all `.db2` files.
10. Edit `world.json` in the world's root folder and rewrite the background value from `.png` to `.webp`.

### Cleanup
11. Run `remove_empty_folders.py` with the world's root folder as argument. 
12. Before running this again, make sure to remove `dedup.txt` since `duplicates.py` will just append the duplicate files at the end of the file - resulting in unintended behaviour.

Done.

## Example

```
duplicates.py bgdia/
rewrite_and_remove.py dedup.txt
bulk-convert-to-webp.ps1
webp_db_fixer.py bgdia/
remove_empty_folders.py bgdia/
list_used_media.py > usedmedia.txt
```
Make sure to rename the `.db3` files afterwards and edit `world.json`. 

### Todo
- Fix the horrible hardcoded mess.
- Integrate .webp conversation

### Do Maybe
- .mp3, .flac to opus .ogg?
- Animated .gif to .webm? (And deal with gifs in general)
- Scan DBs for unused media files and list them (maybe delete aswell?)
- Merge into one file

### Thanks
- VanCole for his [macros](https://github.com/VanceCole/macros)
- Stackoverflow (https://stackoverflow.com/a/38514560, https://stackoverflow.com/a/36113168, https://stackoverflow.com/a/23488980)



