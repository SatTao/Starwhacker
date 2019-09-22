# skyGroups.py

# defines the sky, skyViews and projections

# imports
import os
import json
import math
from starwhacker.celestialObjects import *
from starwhacker.starTools import *
import configparser


class boundary():

	def __init__(self,boundingVertices):

		self.vertices = boundingVertices
		# An array of points (normally RADEC) defining the boundary. Assumes straight lines between all.
		# [ [-10,-10], [-10,10], [10,10], [10,-10], [-10,-10] ] The first point is always repeated to close the loop

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

				# Only add in points if the indicated numberis greater than 2 (the two existing end points)

				if numPoints > 2:

					# Get fractions of 1 representing even divisions of numPoints-1 parts .|.|.|.|.|.|.|. etc, but no 0/numpoints or numpoints/numpoints

					fracs = [n/(numPoints-1) for n in range(1,numPoints-1)]

					for place in fracs:

						newvertex=[xinterp(place), yinterp(place)]
						newvertices.append(newvertex)

			else: # This is the final point

				newvertices.append(vertex) # Closes the polygon loop.

		self.denseVertices = newvertices # We now have a densely populated boundary polygon suitable for projection

class sky():

	def __init__(self):

		# These are made empty by default

		self.stars = []
		# DSOs and Galaxies might go here in the future

	def addStarsFromJSON(self, jsonfile):

		with open(os.path.join(os.path.dirname(__file__),'../data',jsonfile), encoding='utf8') as starfile:  # encoding ensures there are no invalid characters - some star names are not provided in unicode.

			stardict = json.load(starfile)

			for body in stardict['features']:

				try: 
					thisID = str(body['id'])
				except:
					thisID = getRandomString(6)

				try: 
					thisRA = float(body['geometry']['coordinates'][0])
					thisDec = float(body['geometry']['coordinates'][1])
				except:
					continue # Abandon if there's nothing here - it's really useless

				try:
					thisMag = float(body['properties']['mag'])
				except:
					thisMag = 0.0

				try:
					thisBV = float(body['properties']['bv'])
				except:
					thisBV = 0.0

				try: 
					thisDesig = str(body['properties']['desig'])
				except:
					thisDesig = ''

				try: 
					thisCon = str(body['properties']['con'])
				except:
					thisCon = 'NONE'	

				newstar = star(thisID, 
					thisRA, 
					thisDec, 
					thisMag, 
					thisBV, 
					thisDesig, 
					thisCon)

				self.stars.append(newstar)

		print('Added {} stars'.format(len(self.stars)))

		self.doStats()

		return self

	def addConstellationsFromJSON(self, jsonfile):

		return self #TODO

	def doStats(self):

		#FYI this will fail if there are no stars in the sky or view

		# We want to know about min and max values for:
		# RA/Dec, Magnitude, BV

		RAs = [body.RA for body in self.stars]
		self.rangeRA = [min(RAs),max(RAs)]
		decs = [body.dec for body in self.stars]
		self.rangeDec = [min(decs),max(decs)]
		mags = [body.mag for body in self.stars]
		self.rangeMag = [min(mags),max(mags)]
		BVs = [body.BV for body in self.stars]
		self.rangeBV = [min(BVs),max(BVs)]

		return self

	def vitalStatistics(self):

		# Print out a summary of the stars and ranges in our list of stars

		# Check if this is a named skyView or just a sky

		if hasattr(self, 'name'):
			namestr = ' called '+ self.name
		else:
			namestr=''

		print('\nThis {0} object{1} contains:\n'.format(type(self), namestr))
		print('STARS ({0})'.format(len(self.stars)))
		print('RA\tMin: ~{0:0.2f} \tMax: ~{1:0.2f} \tdegrees'.format(self.rangeRA[0], self.rangeRA[1]))
		print('Dec\tMin: ~{0:0.2f} \tMax: ~{1:0.2f} \tdegrees'.format(self.rangeDec[0], self.rangeDec[1]))
		print('Mag\tMin: ~{0:0.2f} \tMax: ~{1:0.2f} '.format(self.rangeMag[0], self.rangeMag[1]))
		print('BV\tMin: ~{0:0.2f} \tMax: ~{1:0.2f} '.format(self.rangeBV[0], self.rangeBV[1]))
		print('\nCONSTELLATIONS ({0})\n'.format(0))
		# TODO print('CONSTELLATIONS') data etc etc

class skyView(sky):

	def __init__(self, fullSky, configFileName, viewName):

		# fullSky is a sky() object with all geometries attached. 
		# configFileName is a .ini config file that defines a region of the sky named ViewName bounded by 
		# min and max RA and Dec, and also 
		# min and max values of magnitude and BV index, or 
		# constellation

		super().__init__() # creates a blank self.stars object [] which we may now manipulate

		self.fullSky = fullSky

		config = configparser.ConfigParser()
		config.read(os.path.join(os.path.dirname(__file__),'../config',configFileName))

		self.name = config[viewName]['name']
		self.configFileName=configFileName
		self.region=viewName

		self.update()

	def update(self):

		# Take the config file and scrape the parent fullSky object's starlist to find stars that match our requirements

		config = configparser.ConfigParser()
		config.read(os.path.join(os.path.dirname(__file__),'../config',self.configFileName))

		self.lonLatBounds = [float(config[self.region]['westBound']),float(config[self.region]['eastBound']),float(config[self.region]['southBound']),float(config[self.region]['northBound'])]
		self.magBounds = [float(config[self.region]['magMin']),float(config[self.region]['magMax'])]
		self.BVBounds = [float(config[self.region]['BVMin']),float(config[self.region]['BVMax'])]

		self.stars=[] # Remove anything existing so we can repopulate, in case the sky has changed in the meantime

		for body in self.fullSky.stars:

			if (self.lonLatBounds[0]<body.RA<self.lonLatBounds[1] and self.lonLatBounds[2]<body.dec<self.lonLatBounds[3] and self.magBounds[0]<body.mag<self.magBounds[1] and self.BVBounds[0]<body.BV<self.BVBounds[1]):

				self.stars.append(body) # If the star passes all these filters then we will include it in this view

		return self

class normalisedCentredProjection():

	# A normalised centred projection is a set of x y coordinates of celestial objects which have been projected in a certain way from lat and lon, 
	# and then normalised so that the maximum and minimum bounds are at 1 and -1 on an axis, each axis scaled equally
	# So it may appear that one axis is not normalised, but it really is. However, the centre of the projected points is on 0,0
	# All parameters needed are accessed from the associated skyView

	def __init__(self, view):

		# view is a valid skyView object

		self.view = view

		self.projectedStars = [] # A like for like list with the self.star attribute of the associated skyView
		self.projectedBounds = [] # The bounds, interpolated to a certain accuracy, and then projected like other points
		# where projectedBounds = [westBound, eastBound, southBound, northBound]
		# and westBound itself = [[x1,y1],[x2,y2,[x3,y3],[...]...]]
		# where points 1, 2, 3 etc are interpolated points on that line after projection.

		# TODO add and include DSOs and constellations etc here too

	def normalise(self):

		# Do stars first, eventually this will include any and all objects listed

		# TODO really this should take interpolated lines of boundaries and find the max min points of these to use for the min max and centralising calcs.

		# First we centre the whole set on 0,0

		xcoords = [coordSet[0] for coordSet in self.projectedStars]
		rangeX = [min(xcoords),max(xcoords)]
		ycoords = [coordSet[1] for coordSet in self.projectedStars]
		rangeY = [min(ycoords),max(ycoords)]

		midX = min(xcoords) + (max(xcoords)-min(xcoords))/2.0
		midY = min(ycoords) + (max(ycoords)-min(ycoords))/2.0

		xoffset = 0 - midX
		yoffset = 0 - midY

		for item in self.projectedStars:
			item[0]=item[0]+xoffset
			item[1]=item[1]+yoffset

		# These coordSets are now centred on the origin

		# Now we need to scale them. This should use boundary calcs. For now let's use stars because we haven't got boundary lines supported yet.

		# Which axis has the biggest difference between min and max? How big is it?

		maxDim = max(rangeX[1]-rangeX[0], rangeY[1]-rangeY[0])

		# Interpolate all these points based on scaling that max dimension to -1 and + 1

		interp = makeInterpolator([-maxDim/2,maxDim/2],[-1,1])

		for item in self.projectedStars:
			item[0]=interp(item[0])
			item[1]=interp(item[1])

		return None

class rectangularProjection(normalisedCentredProjection):

	def __init__(self, view):

		super().__init__()

		self.project()

	def project(self):


		# TODO, naturally

		# Gotta project the celestial bodies, and also the boundaries.

		return 0


