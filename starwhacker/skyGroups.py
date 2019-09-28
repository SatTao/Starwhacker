# skyGroups.py

# defines the sky, skyViews and projections

# imports
import os
import json
import math
from starwhacker.celestialObjects import *
from starwhacker.starTools import *
import configparser
from PIL import Image, ImageDraw
import datetime as dt


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

		# TODO for now we can take the latlon bounds and convert them to polygon corners to create a boundary object.

		boundingPolygon = [[self.lonLatBounds[0],self.lonLatBounds[3]],[self.lonLatBounds[1],self.lonLatBounds[3]],[self.lonLatBounds[1],self.lonLatBounds[2]],[self.lonLatBounds[0],self.lonLatBounds[2]],[self.lonLatBounds[0],self.lonLatBounds[3]]]

		self.boundary = boundary(boundingPolygon)
		self.boundary.interpolate(1) # Interpolate it to one point per degree roughly.

		self.stars=[] # Remove anything existing so we can repopulate, in case the sky has changed in the meantime

		for body in self.fullSky.stars:

			if (self.lonLatBounds[0]<body.RA<self.lonLatBounds[1] and self.lonLatBounds[2]<body.dec<self.lonLatBounds[3] and self.magBounds[0]<body.mag<self.magBounds[1] and self.BVBounds[0]<body.BV<self.BVBounds[1]):

				self.stars.append(body) # If the star passes all these filters then we will include it in this view

		return self

class projection():

	# All parameters needed are accessed from the associated skyView

	def __init__(self, view):

		# view is a valid skyView object

		self.view = view

		self.projectedStars = [] # A like for like list with the self.star attribute of the associated skyView

		self.projectedBounds=boundary(self.view.boundary.denseVertices) # The bounds, interpolated to a certain accuracy, and then projected like other points

		for body in self.view.stars:

			newstar = star(body.ID, 
					body.RA, 
					body.dec, 
					body.mag, 
					body.BV, 
					body.desig, 
					body.constellation)

			self.projectedStars.append(newstar)

		# So now the projected_ arrays are separate copies of the unprojected arrays in the view. We can modify them without affecting the original view.

		# These arrays are in degrees latitude and longitude. We keep them that way now, without normalising. 
		# The reason is that some projections rely on retaining the original scaling and centre (e.g. the stereo projection)
		# The inherited projection classes will normalise and centre after projection, to avoid problems.
		# Then drawing or PCB classes will accept normalised centred projections only for simplicity.

		# TODO add and include DSOs and constellations etc here too

	def normalise(self): # This is typically only accessed after the descendent projection classes have done their projection stuff.

		# Test the projectedBoundary to get min and max values. Find the dead centre. Find the greatest extent. 

		xs=[vertex[0] for vertex in self.projectedBounds.vertices]
		ys=[vertex[1] for vertex in self.projectedBounds.vertices]

		cx=min(xs) + (max(xs)-min(xs))/2
		cy=min(ys) + (max(ys)-min(ys))/2

		# Centralise the boundaries by subracting the centres from each axis

		xs=list(map(lambda x:x-cx,xs))
		ys=list(map(lambda y:y-cy,ys))

		# Find which axis has the greater extent

		greater = xs if max((max(xs)-min(xs)),(max(ys)-min(ys)))==(max(xs)-min(xs)) else ys

		# Set up a scaling interpolating function

		scale=makeInterpolator([min(greater),max(greater)],[-1,1])

		# Use to scale everything in the projected arrays until it's all between -1 and 1 and centred on 0,0

		self.projectedBounds.smush(scale,[cx,cy])
		for body in self.projectedStars:
			body.smush(scale,[cx,cy])
		# Other smush functions go here.

		# TODO round the numbers to reasonable accuracy here?

		return self

	def doStats(self):

		#FYI this will fail if there are no stars

		# We want to know about min and max values for:
		# RA/Dec

		RAs = [body.RA for body in self.projectedStars]
		self.rangeRA = [min(RAs),max(RAs)]
		decs = [body.dec for body in self.projectedStars]
		self.rangeDec = [min(decs),max(decs)]

		return self

	def vitalStatistics(self):

		# Print out a summary of the stars and ranges in our list of stars

		print('\nThis {} object contains:\n'.format(type(self)))
		print('STARS ({0})'.format(len(self.projectedStars)))
		print('RA\tMin: ~{0:0.2f} \tMax: ~{1:0.2f} \tarb. units'.format(self.rangeRA[0], self.rangeRA[1]))
		print('Dec\tMin: ~{0:0.2f} \tMax: ~{1:0.2f} \tarb. units'.format(self.rangeDec[0], self.rangeDec[1]))

		print('\nCONSTELLATIONS ({0})\n'.format(0))


class rectangularProjection(projection):

	def __init__(self, view):

		super().__init__(view)

		self.project()

	def project(self):

		# For a rectangular projection we need to do no work at all on boundaries or stars

		return 1

class stereoProjection(projection):

	def __init__(self, view, lonlatCentroid=[0,0], R=100):

		super().__init__(view)

		self.lonlatCentroid=lonlatCentroid
		self.R=R

		self.project()

	def project(self):

		# We need to project the boundary and stars, and later on more objects too.

		# Boundary first. This is not yet a normalised boundary, the coords are in degrees.

		self.projectedBounds.vertices=list(map(self.lonlatToStereo, self.projectedBounds.vertices))

		# Then we need to do the stars

		for body in self.projectedStars:

			pro=self.lonlatToStereo([body.RA, body.dec])
			body.RA = pro[0]
			body.dec = pro[1]

		# And other data types after this too

		return 1

	def lonlatToStereo(self, point):

		# This takes in a point [lon, lat] and transforms it to a cartesian output point [x,y] based on a stereo transform.

		lon = math.radians(point[0])
		lat = math.radians(point[1])
		lonC = math.radians(self.lonlatCentroid[0])
		latC = math.radians(self.lonlatCentroid[1])

		k = 2*self.R / (1 + math.sin(latC)*math.sin(lat) + math.cos(latC)*math.cos(lat)*math.cos(lon-lonC))

		projectedX = k * math.cos(lat) * math.sin(lon-lonC)
		projectedY = k * (math.cos(latC) * math.sin(lat) - math.sin(latC) * math.cos(lat) * math.cos(lon-lonC))

		return [projectedX, projectedY]	

class drawing():

	# A class that takes a projection and produces an output image

	def __init__(self, projection, majorDim):

		self.projection = projection

		# This class assumes that the projection is normalised before it comes in. 

		self.majorDim = majorDim # The major dimension of the exported image

		self.storagePath = os.path.join(os.path.dirname(__file__),'../output/images/',self.projection.view.name)

		if not os.path.isdir(self.storagePath):
			os.mkdir(self.storagePath)

		self.draw()

	def draw(self):

		# Make simple square images for now. Doesn't matter if there's blank space.

		scaleX = makeInterpolator([-1,1],[0,self.majorDim])
		scaleY = makeInterpolator([-1,1],[self.majorDim, 0]) # Since image writing Y axis is upside down

		# NB all star positions will be rounded to nearest pixel out of necessity 

		# Create a blank, black image

		pic = Image.new('RGB', (self.majorDim, self.majorDim), 'black')

		draw = ImageDraw.Draw(pic) # Create a drawing object

		# Draw in the stars

		for body in self.projection.projectedStars:

			starRad = math.ceil(6 * (1 - (body.mag / (self.projection.view.rangeMag[1] - self.projection.view.rangeMag[0]))))
			redHue = 200 + int(body.BV*25)
			blueHue = 225 - int(body.BV*25)

			starPosx = round(scaleX(body.RA))
			starPosy = round(scaleY(body.dec))

			draw.ellipse([starPosx-starRad,starPosy-starRad,starPosx+starRad,starPosy+starRad],fill=(redHue,200,blueHue,0))

		# Draw in the boundary IN THE FUTURE use the jointing function to smooth these curves multicoord

		for index, start in enumerate(self.projection.projectedBounds.vertices):

			if index < len(self.projection.projectedBounds.vertices)-1:

				x1 = round(scaleX(start[0]))
				y1 = round(scaleY(start[1]))
				end = self.projection.projectedBounds.vertices[index+1]
				x2 = round(scaleX(end[0]))
				y2 = round(scaleY(end[1]))

				col='yellow' if index%2==0 else 'black'

				draw.line([x1,y1,x2,y2],width=1,fill=col)

		outputfilepath = os.path.join(self.storagePath, dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f.png"))
		pic.save(outputfilepath)
	
