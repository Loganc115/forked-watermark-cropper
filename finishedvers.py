import os as os
import math
from PIL import Image
import shutil  # ?
import tkinter
from tkinter import filedialog

THRESHOLD = 8
INPUT_DIRECTORY =tkinter.filedialog.askdirectory(title='where da memes boiii')
OUTPUT_DIRECTORY =(tkinter.filedialog.askdirectory(title= 'where do you want em?')+'/')
NOT_JPGS = (OUTPUT_DIRECTORY+"/notjpegs")
try:    os.mkdir(NOT_JPGS)
except: pass

UNABLETOCROP_DIR = (OUTPUT_DIRECTORY+"/Unable to crop")
try:    os.mkdir(UNABLETOCROP_DIR)
except: pass
# Get color difference

def color_difference(pixel1, pixel2):
    difference = math.sqrt(
        abs(pixel2[0] - pixel1[0]) ** 2 + abs(pixel2[1] - pixel1[1]) ** 2 + abs(pixel2[2] - pixel1[2]) ** 2)
    return difference

#I added this to see if I could at least see the files in the directory
for file in os.listdir(INPUT_DIRECTORY):
    filename = os.fsdecode(file)
    print(filename)
# Assumes image has watermark and attempts to crop
def crop():
    try:
        for file in os.listdir(INPUT_DIRECTORY):  # For each file in directory
            filename = os.fsdecode(file)  # Get filename
            if filename.endswith(".jpg"):
                img = Image.open(INPUT_DIRECTORY + "/" + filename)
                pix = img.load()
                width, length = img.size
                curr_y = length - 1

                # While color difference is less than threshold, move up and decrease Y height
                while color_difference(pix[0, curr_y], pix[0, length - 1]) < THRESHOLD:
                    curr_y = curr_y - 1
                watermark_size = length - curr_y

                # For possible bad crops since the average watermark size is 21 pixels or less
                cropped = img.crop((0, 0, width, length - watermark_size))
                if watermark_size > 21:
                    print("[Skipped]:", filename, watermark_size)
                    # img.show()
                    # cropped.show()
                    shutil.move(NOT_JPGS)
                else:  # Save image
                    cropped.save(OUTPUT_DIRECTORY + filename, format='JPEG', subsampling=0, quality=100)
    except:
        shutil.move(UNABLETOCROP_DIR)








# Just check image for iFunny watermark
def has_watermark():
    pass


def menu():
    print("Cropping images...")
    crop()
    print("Done")


if __name__ == "__main__":
    menu()


