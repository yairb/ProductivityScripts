#!/usr/bin/python

import sys, os, shutil
import numpy as np
from PIL import Image, ImageFilter, ImageOps

def recreateFolder(folderName):
    if os.path.exists(folderName):
        shutil.rmtree(folderName)
    os.makedirs(folderName)

def changeColors(image, bgColor, threshold):
    # Because we want to support in colorful gifs - to allow rgb bgColor -
    # we covert the image back to rgb
    image = image.convert("RGB")
    # We use numpy to work with the image data array directly
    data = np.array(image)
    # Get the three channels of the image to compare to
    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    # Create mask to check if all channels (that probably all the same)
    # are bigger than threshold
    bgMask = (red > threshold) & (green > threshold) & (blue > threshold)
    # Replace all pixels that fit for the criteria with the bg color
    data[:,:,:3][bgMask] = bgColor
    # create back image from data array
    return Image.fromarray(data)

def fadeIn(image, bgColor, fgColor):
    folderName = "gifTemp"
    recreateFolder(folderName)
    filePath = "{0}/{1}.png"
    index = 0
    for threshold in range(0, 255, 25):
        changeColors(image.copy(), bgColor, threshold).save(filePath.format(folderName, index))
        index += 1
    os.system("ffmpeg -i " + folderName + "/%01d.png gifResults/fadeIn.gif")
    os.system("gifsicle -b gifResults/fadeIn.gif -d10 '#0--2' -d75 '#-1'")
    #cleanup
    shutil.rmtree(folderName)

if len(sys.argv) > 1:
    imageFileName = sys.argv[1]
else:
    print "arg not found. Run getAlive.py filename"
    sys.exit()
# load image
original = Image.open(imageFileName)

# convert to grayscale -> find edges -> invert
edges = ImageOps.invert(original.convert("L").filter(ImageFilter.FIND_EDGES))

#reset results folder
recreateFolder("gifResults")

fadeIn(edges, [255,255,255], [0,0,0])
