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
s_1 = skyView(s,'bounds.ini','testRegion')
s_1.doStats().vitalStatistics()

print(len(s_1.boundary.denseVertices))

p1 = projection(s_1)
p1.doStats().vitalStatistics()

p1.normalise()

p1.doStats().vitalStatistics()

# print(p1.projectedBounds.vertices)

# s.drawSkyImageRectProjection(4000,[-10,-10,10,10])
# s.drawSkyImageStereoProjection(4000,[-10,-10,10,10])