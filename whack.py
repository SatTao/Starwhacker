# whack.py 

# Do some whacking

from starwhacker.classes import *

import sys
import os

print("Now whacking")


s = sky().addStarsFromJSON('./data/stars.6.json')
s.drawSkyImage(4000,[-180,-90,180,90])



