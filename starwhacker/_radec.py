# _radec.py

# Defines a RADEC grid class which looks like little crosses at gridline intersections, a la old space photos

# imports

from starwhacker._coordinates import multiPolyline, polyline, position

class radec(multiPolyline):

	def __init__(self, majorGrid):

		# We must build a suitable polyLineList of crosses at the intersection of every grid

		polyLineList=[]

		for i in range(-360, 361, majorGrid):
			for j in range(-90, 91, majorGrid):
				[h, v] = self.getCrossAsPairOfPolylinesAtPosition(position(i, j), 1.0)
				polyLineList.append(h)
				polyLineList.append(v)

		super().__init__(polyLineList)

	def getCrossAsPairOfPolylinesAtPosition(self, atPosition, size):
		'''
		Returns [polyline1, polyline2] which contain 3 positions each and create a cross about position,
		with full extent of size
		'''

		RA=atPosition.RA
		dec=atPosition.dec

		# Handle the horizontal line
		RAs=[RA-size/2, RA-size/8, RA+size/8, RA+size/2]
		horiz=polyline([position(x, dec) for x in RAs])

		# Handle the vertical line
		decs=[dec-size/2, dec-size/8, dec+size/8, dec+size/2]
		vert=polyline([position(RA, y) for y in decs])

		return [horiz, vert]


