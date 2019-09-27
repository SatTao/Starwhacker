# starTools.py

# Utility functions that do repetitive jobs 

# imports here
import configparser
import random
import string
import math

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

def diagDistance(vertices):

	# Vertices looks like [[x1,y1],[x2,y2]]

	return math.sqrt(pow((vertices[1][0]-vertices[0][0]),2)+pow((vertices[1][1]-vertices[0][1]),2))

def getRandomString(length):

	random.seed()
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(length))

def insidePolygon(point, poly):

	# Checks whether a particular point lies inside a polygon boundary, useful for checking if stars are in a boundary.

	# Based on this: https://stackoverflow.com/questions/217578/how-can-i-determine-whether-a-2d-point-is-within-a-polygon

	

	return 0

