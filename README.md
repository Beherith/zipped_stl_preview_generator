# zipped_stl_preview_generator
Generates 1k .png preview images of a folder of zip, rar and 7z files containing .stl files 
Handles archives inside archives. 

# Requirements and dependencies:

1. pyunpack - handles .7z, .zip and .rar archives. Install with pip install pyunpack
https://pypi.org/project/pyunpack/

2. stl-thumb.exe - a GPU accelerated stl renderer, from https://github.com/unlimitedbacon/stl-thumb it is included in this repo

3. convert.exe - A command line tool to convert images, used for resizing 4k renders to 1k previews (fool's antialiasing)

# How to use:
1. Checkout the repo to the same drive you have your folder full of archives of .stls. Run it with

python stl_preview_generator.py --folder mystlarchivefolder

2. An stl-preview folder will be created next to the script, that is where all the images will be stored.

3. An stl_preview_database.json file will be created and it stores each archive that has been processed, so that rerunning the script will only process new stuff

4. The names of the images will contain the _full_ path to each .stl file, making windows search much more useful. Each archive will be prepended with [Z], each directory will be prepended with [D]

5. Enjoy!

![Results:](https://raw.githubusercontent.com/Beherith/zipped_stl_preview_generator/master/screenshot_stl_preview_generator.PNG)
