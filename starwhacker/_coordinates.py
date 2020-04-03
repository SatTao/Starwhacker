# coordinates.py

from starwhacker._tools import makeInterpolator

import math


##--------------------------------------------------------------------------------------------------------------------------------##


# Defines the 'position' class which contains RA- and Dec- style coordinates, and a variety of functions to modify them.

class position():
	'''A class which contains coordinates={'Right Ascension':00.000,'Declination':00.000}, and several functions to modify these.'''

	def __init__(self, rightAscension, declination):

		self.RA=rightAscension
		self.dec=declination

	# Simple utility functions

	def isIdentical(self,other):
		'''
		Checks whether this position is the same as another position
		'''

		return self.RA==other.RA and self.dec==other.dec

	def getDiagonalDistance(self, other):
		'''
		Returns the diagonal distance in the current units to the other position
		'''

		return math.sqrt(pow((other.RA-self.RA),2)+pow((other.dec-self.dec),2))

	def getCopy(self):

		'''
		Returns a copy of itself
		'''

		return position(self.RA,self.dec)

	def getCoordsAsList(self):
		'''
		Returns the coordinates of the position as a list [RA, Dec]
		'''

		return [self.RA, self.dec]

	def isInsidePolyline(self, boundary):
		'''
		Returns true if it falls within the boundary (a polyline) provided
		'''

		if boundary.isClosed():

			nvert = len(boundary.vertices)
			polyXs=[point.RA for point in boundary.vertices]
			polyYs=[point.dec for point in boundary.vertices]

			c=False
			j=nvert-1

			for i in range(nvert):
				if ((polyYs[i]>self.dec) != (polyYs[j]>self.dec)) and (self.RA < ((polyXs[j]-polyXs[i]) * (self.dec-polyYs[i]) / (polyYs[j]-polyYs[i]) + polyXs[i]) ):
					c = not c
				j=i

			if c:
				return True

		return False

	# Self-modification functions

	def scaleAndCentre(self, scalefunc, centre):
		
		'''
		Scales and centres its own coordinates, given a scale function 'scalefunc' and a new centroid 'centre'.

		scalefunc is a linear interpolator function made with makeInterpolator.

		centre is a position object.
		'''

		self.RA=scalefunc(self.RA-centre.RA)
		self.dec=scalefunc(self.Dec-centre.dec)


##--------------------------------------------------------------------------------------------------------------------------------##


# Defines the polyline class which is collection of positions forming a line, along with a variety of functions to modify them.
		
class polyline():
	'''A class which defines a line as a sequence of points, [position_1, position_2, ...], and several functions to modify these.'''

	def __init__(self, vertexList):

		self.vertices = vertexList

	# Simple utility functions

	def isClosed(self):
		'''
		Checks whether or not the polyline forms a simple closed figure (first vertex is identical to last vertex), and there are at least 3 vertices.
		'''

		return len(self.vertices)>=3 and self.vertices[0].isIdentical(self.vertices[-1])

	def getCopy(self):
		'''
		Returns a copy of itself
		'''

		return line(self.vertices)

	def getExtents(self):
		'''
		Returns its x and y extents as [[minX, maxX],[minY, maxY]] (maps to RA and Dec effectively)
		'''

		RAs = [vertex.RA for vertex in self.vertices]
		decs = [vertex.dec for vertex in self.vertices]

		return [[min(RAs), max(RAs)], [min(decs), max(decs)]]



	# Self-modification functions

	def scaleAndCentre(self, scalefunc, centre):
		'''
		Scales and centres the coordinates of its vertices, given a scale function 'scalefunc' and a new centroid 'centre'.

		scalefunc is a linear interpolator function made with makeInterpolator.

		centre is a position object.
		'''

		for vertex in self.vertices:

			vertex.scaleAndCentre(scalefunc,centre)

		return None

	def interpolate(self, nodesPerUnit):
		'''
		Interpolates naive straight lines between existing vertices and splits them into new vertices.

		Aims to keep roughly nodesPerUnit nodes per unit of distance.

		Keeps start and end nodes of each line as they are so corners remain in the same place.
		'''

		# Goes around the polyline in order enumerating pairs of points, interpolating, and recording the new vertices

		interpolatedVertices=[]

		for index, vertex in enumerate(self.vertices):

			if index==len(self.vertices)-1: 
				# Add in the final point
				interpolatedVertices.append(vertex)
				break

			# Get the next position in the line.

			other = self.vertices[index+1]

			# Build interpolation functions between the two points.

			xInterp = makeInterpolator(vertex.RA,other.RA)
			yInterp = makeInterpolator(vertex.dec,other.dec)

			# Work out how many points to place in between, keeping the end nodes as they are (in order to maintain sharp corners if required)

			distance = vertex.getDiagonalDistance(other)
			numPoints = round(nodesPerUnit * distance)

			# We include the start point as a vertex

			interpolatedVertices.append(vertex)

			if numPoints > 2:

				# Get fractions of 1 representing even divisions of numPoints-1 parts .|.|.|.|.|.|.|. etc, but no 0/numpoints or numpoints/numpoints

				fracs = [float(n/(numPoints-1)) for n in range(1,numPoints-1)]

				for place in fracs:

					newVertex=[position(xinterp(place), yinterp(place))]
					interpolatedVertices.append(newVertex)

		# Update the vertex list to the newly interpolated version

		self.vertices=interpolatedVertices

		return None


##--------------------------------------------------------------------------------------------------------------------------------##


# Defines the multiPolyLine class which is a collection of independent polyLines, suitable for a RADEC grid or a constellation.

class multiPolyLine():
	''' A class which defines a collection of independent polyLines and several functions to modify them. ''' 


	def __init__(self, polyLineList):

		self.collection = polyLineList

	# Simple utility functions

	def getCopy(self):
		'''
		Returns a copy of itself
		'''
		return multiPolyLine(self.collection)

	def getExtents(self):
		'''
		Returns its x and y extents as [[minX, maxX],[minY, maxY]] (maps to RA and Dec effectively)
		'''

		childExtents = [child.getExtents() for child in self.collection]

		# Each extent looks like: [[min(RAs), max(RAs)], [min(Decs), max(Decs)]]

		minRA= min([extent[0][0] for extent in childExtents])
		maxRA= max([extent[0][1] for extent in childExtents])

		minDec= min([extent[1][0] for extent in childExtents])
		maxDec= max([extent[1][1] for extent in childExtents])

		return [[minRA, maxRA],[minDec, maxDec]]


	# scaleandcentre, interpolate TODO
