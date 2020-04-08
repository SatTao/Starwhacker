# _tools.py

# Utility functions

# imports here

import configparser
import random
import string
import math
import os

def makeInterpolator(inputRange,outputRange):
	'''
	Returns an interpolation function based on an input range and a desired output range. 
	Points falling outside the range used the interpolator will be mapped outside the range.

	inputRange		[min,max]
	outputRange 	as inputRange

	Arranging max smaller than min on any axis will automatically flip the scaling.

	'''

	inMin = inputRange[0]
	inMax = inputRange[1]
	inRange = inMax - inMin

	outMin = outputRange[0]
	outMax = outputRange[1]
	outRange = outMax - outMin

	scaleFactor = float(outRange) / float(inRange)

	def interp(point):
		return outMin + (point-inMin)*scaleFactor

	return interp

def makeRandomString(length=6,upper=False):
	'''
	Returns a random alphanumeric string of length 'length' (default to 6)
	'''

	random.seed()
	lets = string.ascii_uppercase if upper else string.ascii_letters
	lettersAndDigits = lets + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(length))

def clamp(val, minimum, maximum):
	'''
	Clamps val between the minimum and maximum values
	'''

	return minimum if val < minimum else maximum if val > maximum else val

def getStarSize(star, starScale):
	'''
	Returns [ringsize, drillsize] for the hole/pad associated with this star based on a provided scale factor
	'''
	
	ringsize=round(starScale(star.mag),1) # map the size and round to 1 decimal place

	# Next we need to define the drill hole size (if there is one, otherwise return 0)

	drills=[0.6, 0.8, 1.0, 1.2]

	if ringsize>=1.4:
		drillsize=clamp(round(ringsize-0.8,1)-((ringsize-0.8)%0.2),0.6,1.2)
	else:
		drillsize=0

	return [ringsize, drillsize]