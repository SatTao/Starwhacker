# whack.py 

# Do some whacking

from starwhacker.celestialObjects import *
from starwhacker.skyGroups import *
from starwhacker.starTools import *

import sys
import os
import math

print("Now whacking")


s = sky().addStarsFromJSON('stars.6.json')
s.doStats().vitalStatistics()
s_1 = skyView(s,'test.ini','testRegion')
s_1.doStats().vitalStatistics()
# s.drawSkyImageRectProjection(4000,[-10,-10,10,10])
# s.drawSkyImageStereoProjection(4000,[-10,-10,10,10])