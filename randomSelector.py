import os
import cv2
from random import randrange
import sys

if len(sys.argv) > 1:
    root_dir = sys.argv[1]
    print(root_dir)
else:
    root_dir = "C:\\Users\\alber\\Desktop\\D&DCharacters\\Reference Images\\why"

destination_dir = os.path.join(root_dir,"usable")

usable = False
screen_x,screen_y = (1000,600)

while not usable:
    dir = os.listdir(root_dir)
    pick = dir[randrange(0,len(dir))]
    file = os.path.join(root_dir,pick)
    if os.path.isfile(file) and not file.startswith('.') and not file.__eq__(__file__) and (file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg')):
        img = cv2.imread(os.path.join(root_dir,pick), cv2.IMREAD_COLOR)
        sizey,sizex=img.shape[0],img.shape[1]
        print(sizex,sizey)
        if sizex > screen_x:
            sizey = sizey * screen_x / sizex
            sizex = screen_x
        if sizey > screen_y:
            sizex = sizex * screen_y / sizey
            sizey = screen_y
        print(sizex,sizey)
        img = cv2.resize(img, (int(sizex), int(sizey)))
        cv2.imshow(pick, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        i = input("Usable? (y/n/q):")
        if i.lower() == 'y':
            usable = True
            os.rename(os.path.join(root_dir,pick), os.path.join(destination_dir,pick))
            os.remove(os.path.join(root_dir,pick))
        elif i.lower() == 'q':
            usable = True
    