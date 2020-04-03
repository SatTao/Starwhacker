# _whck.py

# Script to automate test runs of the new _version of starwhacker

from starwhacker._sky import sky

print('Now whacking!')

s=sky().addStarsFromJson('stars.14.json')
s.vitalStatistics()
s.filter('testwhack')
s.vitalStatistics()

print('Whacked!')

