# celestialObjects.py

# Contains all classes of celestial object

# imports

from starwhacker.starTools import *

class celestialObject():

	def __init__(self, ID, RightAscension, Declination, Magnitude):

		# These are the longitude and latitude of the object in degrees

		self.RA = RightAscension
		self.dec = Declination

		# This is the apparent brightness of the object in a logarithmic scale

		self.mag = Magnitude if isinstance(Magnitude,float) else 0.0
		
		# This is some kind of ID, be it a name or number

		self.ID = ID

	def smush(self, scalefunc, centres):

		self.RA=scalefunc(self.RA-centres[0])
		self.dec=scalefunc(self.dec-centres[1])

	def makeDistinctCopy(self):

		# TODO implement a CO copying mechanism
		# Until I get around to this, we just instantiate with a full argument list like normal

		return None

	# TODO add an areYouWithin? function that accepts a (polygon) boundary and returns true of it's inside. Clean up skyGroups code this way.

	
class star(celestialObject):

	def __init__(self, ID, RightAscension, Declination, Magnitude, BlueVioletIndex, Designation, Constellation):

		super().__init__(ID, RightAscension, Declination, Magnitude)

		# This is the apparent colour of the star between -2 and 2, roughly

		self.BV = BlueVioletIndex if isinstance(BlueVioletIndex,float) else 0.0

		# This is the star's name, if it has one, in that region

		self.desig = Designation if isinstance(Designation,str) else ''

		# This is the star's parent constellation:

		self.constellation = Constellation if isinstance(Constellation,str) else ''

class constellation():

	def __init__(self, id, multiLineCoords):

		self.id=id
		self.multiVertices=multiLineCoords

	def smush(self, scalefunc, centres):

		# to do, to assist with scaling and normalisation etc

		newMultiVert = []

		for line in self.multiVertices:

			newLine=[]

			for coord in line:

				newCoord = [scalefunc(coord[0]-centres[0]), scalefunc(coord[1]-centres[1])]
				newLine.append(newCoord)

			newMultiVert.append(newLine)

		self.multiVertices=newMultiVert

# Can add DSOs, galaxies and more here later

