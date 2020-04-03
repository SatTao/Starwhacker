# _stars.py

from starwhacker._coordinates import position

# Defines the star class which inherits from the position class

class star(position):
	'''A class which defines a star, including technical information, and several utility functions'''

	def __init__(self, ID, rightAscension, declination, magnitude, blueVioletIndex, designation, constellation):

		super().__init__(rightAscension, declination)

		# The apparent magnitude

		self.mag = magnitude

		# This is the apparent colour of the star between -2 and 2, roughly

		self.BV = blueVioletIndex if isinstance(blueVioletIndex,float) else 0.0

		# This is the star's name, if it has one, in that region

		self.desig = designation if isinstance(designation,str) else ''

		# This is the star's parent constellation:

		self.con = constellation if isinstance(constellation,str) else ''

	# Simple utility functions

	def getCopy(self):
		'''
		Returns a copy of itself.
		'''

		return star(self.ID, self.RA, self.dec, self.mag, self.BV, self.desig, self.constellation)

	def matches(self, boundary, mags, BVs):
		'''
		Returns true if it matches the specified conditions:
		boundary is a polyline which it must fall within.
		mags is a list [minMag, maxMag] which its mag value must be in range
		ditto BVs 
		'''

		if (self.isInsidePolyline(boundary) and mags[0]<=self.mag<=mags[1] and BVs[0]<=self.BV<=BVs[1]):
			return True
		else:
			return False

