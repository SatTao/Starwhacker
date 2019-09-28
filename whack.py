# whack.py 

# Do some whacking

from starwhacker.celestialObjects import *
from starwhacker.skyGroups import *
from starwhacker.starTools import *

import sys
import os
import math
import time

print("Now whacking")


s = sky().addStarsFromJSON('stars.14.json')
s.doStats().vitalStatistics()
s_1 = skyView(s,'bounds.ini','testRegion')
s_1.doStats().vitalStatistics()

# print(len(s_1.boundary.denseVertices))

p1 = rectangularProjection(s_1)
p1.doStats().vitalStatistics()
p1.normalise()
p1.doStats().vitalStatistics()

p2 = stereoProjection(s_1, [40,-40], 1)
p2.doStats().vitalStatistics()
p2.normalise()
p2.doStats().vitalStatistics()

p3 = stereoProjection(s_1, [30,-40], 20)
p3.doStats().vitalStatistics()
p3.normalise()
p3.doStats().vitalStatistics()

p4 = stereoProjection(s_1, [30,-40], 100)
p4.doStats().vitalStatistics()
p4.normalise()
p4.doStats().vitalStatistics()

I1 = drawing(p1,1000)
time.sleep(1)
I2 = drawing(p2,2000)
time.sleep(1)
I3 = drawing(p3,2000)
time.sleep(1)
I4 = drawing(p4,2000)

# s.drawSkyImageRectProjection(4000,[-10,-10,10,10])
# s.drawSkyImageStereoProjection(4000,[-10,-10,10,10])