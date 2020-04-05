# _whck.py

# Script to automate test runs of the new _version of starwhacker

from starwhacker._sky import sky
from starwhacker._coordinates import position
from starwhacker._drawing import drawing

import time

print('Now whacking!')

print('Adding stars to sky')

start=time.time()
s=sky().addStarsFromJson('stars.14.json')
s.vitalStatistics()
stop=time.time()
print('{0:0.4f} seconds elapsed'.format(stop-start))

print('Filtering the sky')

start=time.time()
s.filter('testwhack')
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
s.stereoProject(position(10,10), 100)
s.vitalStatistics()
stop=time.time()
print('{0:0.4f} seconds elapsed'.format(stop-start))

print('Normalising')

start=time.time()
s.normalise()
s.vitalStatistics()
stop=time.time()
print('{0:0.4f} seconds elapsed'.format(stop-start))

d=drawing(s,2000)
d.render()

print('Whacked!')

