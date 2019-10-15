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

	
class star(celestialObject):

	def __init__(self, ID, RightAscension, Declination, Magnitude, BlueVioletIndex, Designation, Constellation):

		super().__init__(ID, RightAscension, Declination, Magnitude)

		# This is the apparent colour of the star between -2 and 2, roughly

		self.BV = BlueVioletIndex if isinstance(BlueVioletIndex,float) else 0.0

		# This is the star's name, if it has one, in that region

		self.desig = Designation if isinstance(Designation,str) else ''

		# This is the star's parent constellation:

		self.constellation = Constellation if isinstance(Constellation,str) else ''

	def meetsCondition(self, cond):

		# Return true if this object passes the tests of the filtering conditions.

		# if (cond.lonLatBounds[0]<self.RA<cond.lonLatBounds[1] and cond.lonLatBounds[2]<self.dec<cond.lonLatBounds[3] and cond.magBounds[0]<self.mag<cond.magBounds[1] and cond.BVBounds[0]<self.BV<cond.BVBounds[1]):
		if any(insidePolygon([self.RA, self.dec],cond.boundary.vertices)) and cond.magBounds[0]<self.mag<cond.magBounds[1] and cond.BVBounds[0]<self.BV<cond.BVBounds[1]:
			return True
		else:
			return False

	def getCopy(self, cond):

		inside = insidePolygon([self.RA, self.dec],cond.boundary.vertices)
		mod=0
		if not inside[1]:
			mod=-180 if inside[0] else 180

		newstar = star(self.ID, 
					self.RA+mod, 
					self.dec, 
					self.mag, 
					self.BV, 
					self.desig, 
					self.constellation)

		return newstar

class constellation():

	def __init__(self, id, multiLineCoords):

		self.id=id
		self.multiVertices=multiLineCoords

	def smush(self, scalefunc, centres):

		newMultiVert = []

		for line in self.multiVertices:

			newLine=[]

			for coord in line:

				newCoord = [scalefunc(coord[0]-centres[0]), scalefunc(coord[1]-centres[1])]
				newLine.append(newCoord)

			newMultiVert.append(newLine)

		self.multiVertices=newMultiVert

	def meetsCondition(self, cond):

		# Return true if any section of this object passes the tests of the filtering conditions.

		for segment in self.multiVertices:
			for coord in segment:
				# if (cond.lonLatBounds[0]<coord[0]<cond.lonLatBounds[1] and cond.lonLatBounds[2]<coord[1]<cond.lonLatBounds[3]): 
				if any(insidePolygon([coord[0], coord[1]], cond.boundary.vertices)):
					return True
		return False

	def getCopy(self):

		return constellation(self.id, self.multiVertices)

	def getPartialCopyByCondition(self, cond):

		# How to do this, and what should it do?

		f = lambda pt : any(insidePolygon(pt, cond.boundary.vertices))

		newmv=[]

		for segment in self.multiVertices:
			seg=[]
			for coord in segment:
				inside = insidePolygon([coord[0], coord[1]], cond.boundary.vertices)
				if any(inside):
					mod=0
					if not inside[1]:
						mod=-180 if inside[0] else 180
					coord[0]=coord[0]+mod
				seg.append(coord)
			newmv.append(seg)

		newconst=constellation(self.id,newmv)

		return newconst



# Can add DSOs, galaxies and more here later

