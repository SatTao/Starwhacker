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

print('Filtering the sky')

start=time.time()
s.filter('scorpio')
s.vitalStatistics()
stop=time.time()
print('{0:0.4f} seconds elapsed'.format(stop-start))

print('Interpolating')

start=time.time()
s.interpolate(1.0)
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

d=drawing(s,200) # Major Dimension of 200mm
d.render()

b=board(s,200) # Major dimension of 200mm
b.render()

print('Whacked!')

