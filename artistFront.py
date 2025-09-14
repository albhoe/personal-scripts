import os
import re

root_dir = "C:\\Users\\alber\\Desktop\\D&DCharacters\\Reference Images\\why\\usable\\"

files = []
for f in os.listdir(root_dir):
    f = root_dir+f
    if os.path.isfile(f):
        if not f.startswith('.'):
            if not f.__eq__(__file__):
                files.append(f)
            else:print(f+" equals __file__")
        else:
            print(f+" starts with '.'")
    else:
        print (f+" is not a file")

for f in files:
    destination = ''
    try:
        parenStart = f.index("(") + 1
        parenEnd = f.index(")")
    except ValueError:
        #There is no parenthesis in the file name (can be returned as normal)
        destination = f
    else:
        artistOrCount = f[parenStart:parenEnd]
        if len(artistOrCount) == 1 and artistOrCount[0].isdigit():
            #This is a count. The artist is unknown. Return as normal.
            destination = f 
        else:
            #This is the name of the artist
            nameIndex = len(root_dir)
            name = f[nameIndex:parenStart-2]
            if (len(name) == 0):
                destination = f[0:nameIndex] + artistOrCount + f[parenEnd+1:]
                #There are no characters depicted, or the artist is depicted as themselves
            else:
                destination = f[0:nameIndex] + artistOrCount +' (' + name + ')' + f[parenEnd+1:]
    os.rename(f,destination)
