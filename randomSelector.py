import os
from random import randrange

root_dir = "C:\\Users\\alber\\Desktop\\D&DCharacters\\Reference Images\\why"

files = []
for f in os.listdir(root_dir):
    f = os.path.join(root_dir,f)
    if os.path.isfile(f) and not f.startswith('.') and not f.__eq__(__file__):
        files.append(f)
pick = files[randrange(0,len(files))]
print(pick)
b = os.open(pick,os.O_RDONLY)