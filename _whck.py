# _whck.py

# Script to automate test runs of the new _version of starwhacker

from starwhacker._sky import sky
from starwhacker._coordinates import position
from starwhacker._drawing import drawing
from starwhacker._board import board

import time

print('Now whacking!')

print('Adding stars to sky')

start=time.time()
s=sky().addStarsFromJson('stars.14.json').addConstellationsFromJSON('constellations.lines.json').makeGrid(10)
s.vitalStatistics()
stop=time.time()
print('{0:0.4f} seconds elapsed'.format(stop-start))

print('Filtering the sky, and interpolating lines')

start=time.time()
s.filterAndInterpolate('scorpio', 1.0)
s.vitalStatistics()
stop=time.time()
print('{0:0.4f} seconds elapsed'.format(stop-start))

print('Stereo-projecting')

start=time.time()
s.stereoProject()
s.vitalStatistics()
stop=time.time()
print('{0:0.4f} seconds elapsed'.format(stop-start))

print('Normalising')

start=time.time()
s.normalise()
s.vitalStatistics()
stop=time.time()
print('{0:0.4f} seconds elapsed'.format(stop-start))

d=drawing(s,200,targetConstellation='Sco') # Major Dimension of 200mm, target constellation is scorpio
d.render()

b=board(s,200,targetConstellation='Sco') # Major dimension of 200mm, target constellation is scorpio
b.render()

print('Whacked!')

