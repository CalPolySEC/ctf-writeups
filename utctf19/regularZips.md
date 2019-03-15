# Regular Zips
Category: Forensics

Extracting this [zip folder](assets/RegularZips.zip) and all of it's subfolders using a hint given in regex would not be reccomended manually, because it ended up having 1000 subfolders.

Using this [script](assets/regularZips.py), we were able to unzip them all, by first making a "dir0" directory and putting the first hint of ````^ 7 y RU[A-Z]KKx2 R4\d[a-z]B N$```` in a file in that directory called "hint.txt" and copied RegularZips.zip to that directory as "archive.zip"

Flag Obtained: utflag{bean_pure_omission_production_rally}
