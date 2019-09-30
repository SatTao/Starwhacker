# starTools.py

# Utility functions that do repetitive jobs 

# imports here
import configparser
import random
import string
import math
import os

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

	nvert = len(poly)
	polyXs=[i[0] for i in poly]
	polyYs=[i[1] for i in poly]

	c=False
	j=nvert-1

	for i in range(nvert):
		if ((polyYs[i]>point[1]) != (polyYs[j]>point[1])) and (point[0] < ((polyXs[j]-polyXs[i]) * (point[1]-polyYs[i]) / (polyYs[j]-polyYs[i]) + polyXs[i]) ):
			c = not c
		j=i

	return c

class boundary():

	def __init__(self,boundingVertices):

		self.vertices = boundingVertices
		# An array of points (normally RADEC) defining the boundary. Assumes straight lines between all.
		# [ [-10,-10], [-10,10], [10,10], [10,-10], [-10,-10] ] The first point is always repeated to close the loop

	def smush(self, scalefunc, centres):

		self.vertices=list(map(lambda i: [scalefunc(i[0]-centres[0]),scalefunc(i[1]-centres[1])],self.vertices))

	def interpolate(self, ptsPerUnit):

		# Treats lines between points as straight, then adds in interpolated points on those lines, with even spacing.

		# Iterate through the bounding vertices, take the next one, and find the defining equation.

		newvertices = []

		for index, vertex in enumerate(self.vertices):

			if (index<len(self.vertices)-1): # Avoids the last point in the sequence

				# Create interpolator functions for x and y

				nextVertex = self.vertices[index+1]

				xinterp = makeInterpolator([0,1],[vertex[0],nextVertex[0]])
				yinterp = makeInterpolator([0,1],[vertex[1],nextVertex[1]])

				# Calculate diagonal distance between the bounding vertices

				diagUnits = diagDistance([vertex,nextVertex])

				# put in the current vertex unchanged

				newvertices.append(vertex)

				# Find the how many points we need to fit on this line.

				numPoints = math.ceil(ptsPerUnit*diagUnits) # Always round up.

				# Only add in points if the indicated number is greater than 2 (the two existing end points)

				if numPoints > 2:

					# Get fractions of 1 representing even divisions of numPoints-1 parts .|.|.|.|.|.|.|. etc, but no 0/numpoints or numpoints/numpoints

					fracs = [n/(numPoints-1) for n in range(1,numPoints-1)]

					for place in fracs:

						newvertex=[xinterp(place), yinterp(place)]
						newvertices.append(newvertex)

			else: # This is the final point

				newvertices.append(vertex) # Closes the polygon loop.

		self.denseVertices = newvertices # We now have a densely populated boundary polygon suitable for projection


class conditions():

	# A class defining a set of conditions pulled from an .ini file, which can be passed to an object to check whether the conditions are met.

	def __init__(self, configFileName, region):

		self.configFileName = configFileName
		self.region = region

		config = configparser.ConfigParser()
		config.read(os.path.join(os.path.dirname(__file__),'../config',self.configFileName))

		self.name = config[self.region]['name']

		self.lonLatBounds = [float(config[self.region]['westBound']),float(config[self.region]['eastBound']),float(config[self.region]['southBound']),float(config[self.region]['northBound'])]
		self.magBounds = [float(config[self.region]['magMin']),float(config[self.region]['magMax'])]
		self.BVBounds = [float(config[self.region]['BVMin']),float(config[self.region]['BVMax'])]

		# TODO for now we can take the lonlat bounds and convert them to polygon corners to create a boundary object.

		boundingPolygon = [[self.lonLatBounds[0],self.lonLatBounds[3]],[self.lonLatBounds[1],self.lonLatBounds[3]],[self.lonLatBounds[1],self.lonLatBounds[2]],[self.lonLatBounds[0],self.lonLatBounds[2]],[self.lonLatBounds[0],self.lonLatBounds[3]]]
		self.boundary = boundary(boundingPolygon)
		self.boundary.interpolate(1)

		self.radec=RADEC(int(config[self.region]['gridSpacing']))
		self.radec.interpolate(1)

	def getBoundary(self):

		return self.boundary

	def getRADEC(self):

		return self.radec

class RADEC():

	# A Class representing the geometry of a Right Ascension, Declination grid, used for drawing and boards

	def __init__(self, majorTicks):

		self.majorTicks=majorTicks # Spacing between grid lines in both dimensions in degrees

		self.grid=[ [[i,-90],[i,90]] for i in range(-180, 180+self.majorTicks, self.majorTicks)] # Inclusive of final point, this is vertical lines
		self.grid=self.grid+[ [[-180,j],[180,j]] for j in range(-90, 90+self.majorTicks, self.majorTicks)] # Inclusive of final point, this is horizontal lines

	def interpolate(self, ptsPerUnit):

		# Treats lines between points as straight, then adds in interpolated points on those lines, with even spacing.

		# Iterate through the lines in the grid, and add interpolated points on the lines

		newGrid=[]

		for line in self.grid:

			newline=[line[0]] # Put in the first point

			xinterp = makeInterpolator([0,1],[line[0][0],line[1][0]])
			yinterp = makeInterpolator([0,1],[line[0][1],line[1][1]])

			# Calculate diagonal distance between the bounding vertices

			diagUnits = diagDistance([line[0],line[1]])

			# Find the how many points we need to fit on this line.

			numPoints = math.ceil(ptsPerUnit*diagUnits) # Always round up.

			# Only add in points if the indicated number is greater than 2 (the two existing end points)

			if numPoints > 2:

				# Get fractions of 1 representing even divisions of numPoints-1 parts .|.|.|.|.|.|.|. etc, but no 0/numpoints or numpoints/numpoints

				fracs = [n/(numPoints-1) for n in range(1,numPoints-1)]

				for place in fracs:

					newvertex=[xinterp(place), yinterp(place)]
					newline.append(newvertex)

			newline.append(line[1]) # Put back the final point of the grid line

			newGrid.append(newline)

		self.grid = newGrid

	def smush(self, scalefunc, centres):

		newGrid = []

		for line in self.grid:

			newLine=[]

			for coord in line:

				newCoord = [scalefunc(coord[0]-centres[0]), scalefunc(coord[1]-centres[1])]
				newLine.append(newCoord)

			newGrid.append(newLine)

		self.grid=newGrid

	def getCopy(self):

		temp = RADEC(self.majorTicks)
		temp.grid=self.grid
		return temp