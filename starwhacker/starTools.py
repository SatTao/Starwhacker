# starTools.py

# Utility functions that do repetitive jobs 

# imports here
import configparser
import random
import string

def makeInterpolator(inputRange,outputRange):

	# inputRange		[min,max]
	# outputRange 		as inputRange

	# Arranging max smaller than min on any axis will automatically flip the scaling.

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

def getRandomString(length):

	random.seed()
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(length))

