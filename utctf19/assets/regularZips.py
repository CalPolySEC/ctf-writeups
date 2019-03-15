'''
    Author: meinfr13nd
    Date created: 3/09/2019
    Date last modified: 3/09/2019
    Python Version: 3.6.7
'''
import sre_yield as sre
from zipfile import ZipFile
import os

curidx = 399
while True:
   curfile = "dir" + str(curidx) + "/archive.zip" #current archive file
   f = ZipFile(curfile)
   curhint = "dir" + str(curidx) + "/hint.txt"
   with open(curhint) as hintfile:
       pattern = hintfile.read().rstrip('\n') #load regex hint
   curdir = "dir" + str(curidx + 1)
   os.makedirs("dir" + str(curidx + 1), exist_ok=True) #make the next directory to extract to
   found = False
   for item in sre.AllStrings(pattern): #try all regex stings
       try:
           f.extractall(path=curdir, pwd=item.encode("utf-8"))
           print(item)
           found = True
       except Exception as e:
           continue
       if found:
           break
   if not found:
       raise ValueError("The hint file did not produce the password")
   curidx += 1
