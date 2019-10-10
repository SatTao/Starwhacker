# whack.py 

# Do some whacking

from starwhacker.celestialObjects import *
from starwhacker.skyGroups import *
from starwhacker.starTools import *

import sys
import os
import math

print("Now whacking")


s = sky().addStarsFromJSON('stars.14.json').addConstellationsFromJSON('constellations.lines.json')
s.doStats().vitalStatistics()

s_1 = skyView(s,'bounds.ini','centralBlock') # A part of s bounded by constraints in the .ini file
s_1.doStats().vitalStatistics()

p1 = stereoProjection(s_1, [-10,-10], 1).normalise() # A normalised stereo projection centred on 0 longitude, -40 latitude, with a scale factor of 1
p1.doStats().vitalStatistics()

I1 = drawing(p1,3000) # A square image 3000px wide
