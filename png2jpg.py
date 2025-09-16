import cv2
import os
import sys

print(sys.argv)
if len(sys.argv) > 1:
    root_dir = sys.argv[1]
    print(root_dir)
else:
    root_dir = "C:\\Users\\alber\\Desktop\\D&DCharacters\\Reference Images\\why"
    
for file in os.listdir(root_dir):
    if file.endswith(".png"):
        end = file.index('.')
        newname = file[0:end] + ".jpg"

        png_img = cv2.imread(os.path.join(root_dir, file))
        cv2.imwrite(os.path.join(root_dir, newname), png_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])