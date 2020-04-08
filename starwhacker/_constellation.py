# _constellation.py

# Defines a constellation class which contains a multi-set of vertices

# imports

from starwhacker._coordinates import multiPolyline, polyline, position

class constellation(multiPolyline):

	def __init__(self, name, polyLineList):

		self.name=name

		super().__init__(polyLineList)

	



