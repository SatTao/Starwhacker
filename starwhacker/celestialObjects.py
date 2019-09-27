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

	
class star(celestialObject):

	def __init__(self, ID, RightAscension, Declination, Magnitude, BlueVioletIndex, Designation, Constellation):

		super().__init__(ID, RightAscension, Declination, Magnitude)

		# This is the apparent colour of the star between -2 and 2, roughly

		self.BV = BlueVioletIndex if isinstance(BlueVioletIndex,float) else 0.0

		# This is the star's name, if it has one, in that region

		self.desig = Designation if isinstance(Designation,str) else ''

		# This is the star's parent constellation:

		self.constellation = Constellation if isinstance(Constellation,str) else ''

# Can add DSOs, galaxies and more here later

