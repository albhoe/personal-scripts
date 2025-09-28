#python -u C:\Users\alber\Desktop\scripts\randomSelector.py "C:\\Users\\alber\\Desktop\\D&DCharacters\\Reference Images\\why" 

import os
import cv2
from random import randrange
import sys

if len(sys.argv) > 1:
    root_dir = sys.argv[1]
if len(sys.argv) > 2:
    search = sys.argv[2]
else:
    root_dir = "C:\\Users\\alber\\Desktop\\D&DCharacters\\Reference Images\\why"
    search = ''
destination_dir = os.path.join(root_dir,"usable")
usable = False
screen_x,screen_y = (1500,700)

reportPath = os.path.join(root_dir,".most_recent.txt")

with open(reportPath,"w") as rf:
    rf.write ("File name: Usability\n")
    while not usable:
        dir = os.listdir(root_dir)
        pick = dir[randrange(0,len(dir))]
        file = os.path.join(root_dir,pick)
        if os.path.isfile(file) and not file.__eq__(__file__) and \
            (file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg')) \
                and pick[:pick.rfind('.')].find(search) >= 0:
            print (pick)
            img = cv2.imread(os.path.join(root_dir,pick), cv2.IMREAD_COLOR)
            sizey,sizex=img.shape[0],img.shape[1]
            if sizex > screen_x:
                sizey = sizey * screen_x / sizex
                sizex = screen_x
            if sizey > screen_y:
                sizex = sizex * screen_y / sizey
                sizey = screen_y
            img = cv2.resize(img, (int(sizex), int(sizey)))
            cv2.imshow(pick, img)
            cv2.moveWindow(pick, 0,0)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            i = input("Usable? (y/n/q):")
            if i.lower() == 'y':
                usable = True
                os.rename(os.path.join(root_dir,pick), os.path.join(destination_dir,pick))
                os.remove(os.path.join(root_dir,pick))
                rf.write(str(pick) + ": Usable\n")
            elif i.lower() == 'q':
                usable = True
                rf.write(str(pick) + ": Quit\n")
            else:
                rf.write(str(pick) + ": Not Usable\n")
