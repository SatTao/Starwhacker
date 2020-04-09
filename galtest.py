# galtest.py

import math
import os 
from PIL import Image, ImageDraw, ImageFont
import datetime

im=Image.open('./data/GAIA_pixMod.png')
print(im.getpixel((1,1)))

