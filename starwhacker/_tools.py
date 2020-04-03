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

def makeRandomString(length=6):
	'''
	Returns a random alphanumeric string of length 'length' (default to 6)
	'''

	random.seed()
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(length))

