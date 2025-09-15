import os
import cv2
from random import randrange

root_dir = "C:\\Users\\alber\\Desktop\\D&DCharacters\\Reference Images\\why"
destination_dir = "C:\\Users\\alber\\Desktop\\D&DCharacters\\Reference Images\\why\\usable"

usable = False
files = []
for f in os.listdir(root_dir):
    file = os.path.join(root_dir,f)
    if os.path.isfile(file) and not file.startswith('.') and not file.__eq__(__file__) and (file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg')):
        files.append(f)

while not usable:
    
    pick = files[randrange(0,len(files))]

    img = cv2.imread(os.path.join(root_dir,pick), cv2.IMREAD_COLOR)
    cv2.imshow(pick, img)
    cv2.waitKey(0)
    i = input("Usable? (y/n/q):")
    if i.lower() == 'y':
        usable = True
        os.rename(os.path.join(root_dir,pick), os.path.join(destination_dir,pick))
        os.remove(os.path.join(root_dir,pick))
    elif i.lower() == 'q':
        usable = True
    cv2.destroyAllWindows()