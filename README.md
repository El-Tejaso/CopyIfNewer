# copy_if_newer

A useful utility script for keeping copied backup folders in other locations in sync. It is much faster than a normal copy, because it will only copy over files that are newer. 

## How to use

Run this:
```
python main.py
```

And then in the ui, select the source and destination folders.
The script will recurse through every folder in the source folder, and for each file, if the corresponding file in the destination folder does not exist, or is older than the one in the source file, it will create/copy it from the source file. 

NOTE: This script does not delete files that are no-longer in the source folder but are in the destination folder, it only overwrites files if they are newer in the source folder, or creates them if not already present in the destination folder.