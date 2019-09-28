# whack.py 

# Do some whacking

from starwhacker.celestialObjects import *
from starwhacker.skyGroups import *
from starwhacker.starTools import *

import sys
import os
import math

print("Now whacking")


s = sky().addStarsFromJSON('stars.14.json')
s.doStats().vitalStatistics()
s_1 = skyView(s,'bounds.ini','testRegion')
s_1.doStats().vitalStatistics()

p2 = stereoProjection(s_1, [0,-40], 1)
p2.doStats().vitalStatistics()
p2.normalise()
p2.doStats().vitalStatistics()

I2 = drawing(p2,3000)
