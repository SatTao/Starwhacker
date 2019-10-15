# skyGroups.py

# defines the sky, skyViews and projections

# imports
import os
import json
import math
from starwhacker.celestialObjects import *
from starwhacker.starTools import *
import configparser
from PIL import Image, ImageDraw, ImageFont
import datetime as dt

class sky():

	def __init__(self):

		# These are made empty by default

		self.stars = []
		self.constellations = []
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

		with open(os.path.join(os.path.dirname(__file__),'../data',jsonfile), encoding='utf8') as constfile:  # encoding ensures there are no invalid characters - some star names are not provided in unicode.

			constdict = json.load(constfile)

			for body in constdict['features']:

				thisID = body['id']
				thisMultiCoord = body['geometry']['coordinates']

				newConstellation = constellation(thisID, thisMultiCoord)

				self.constellations.append(newConstellation)

		print('Added {} constellations'.format(len(self.constellations)))

		return self

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
		print('\nCONSTELLATIONS ({0})\n'.format(len(self.constellations)))
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

		self.cond = conditions(configFileName, viewName)

		self.update()

	def update(self):

		self.boundary = self.cond.getBoundary()
		self.radec = self.cond.getRADEC()

		self.stars=[] # Remove anything existing so we can repopulate, in case the sky has changed in the meantime
		for body in self.fullSky.stars:
			if body.meetsCondition(self.cond):
				self.stars.append(body.getCopy(self.cond)) # If the star passes all these filters then we will include it directly in this view

		# Now do the same for constellations
		self.constellations=[]
		for body in self.fullSky.constellations:
			if body.meetsCondition(self.cond):
				self.constellations.append(body.getCopy())

		return self

class projection():

	# All parameters needed are accessed from the associated skyView

	def __init__(self, view):

		# view is a valid skyView object

		self.view = view

		self.projectedStars = [] # A like for like list with the self.star attribute of the associated skyView

		self.projectedBounds=boundary(self.view.boundary.denseVertices) # The bounds, interpolated to a certain accuracy, and then projected like other points

		self.projectedConstellations = []

		self.projectedRadec=view.radec.getCopy()

		for body in self.view.stars:
			self.projectedStars.append(body.getCopy(self.view.cond)) 

		for body in self.view.constellations:
			self.projectedConstellations.append(body.getPartialCopyByCondition(self.view.cond))

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
		self.projectedRadec.smush(scale,[cx,cy])
		for body in self.projectedStars:
			body.smush(scale,[cx,cy])
		for body in self.projectedConstellations:
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

		# For a rectangular projection we need to do no work at all on boundaries or stars or constellations

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

		# Then we can project out the constellations. Be aware these may cross boundaries initially, or jump from 359-0 etc. Control this later TODO

		for body in self.projectedConstellations:

			newMultiVert = []

			for line in body.multiVertices:

				newLine=[]

				for coord in line:

					newCoord = self.lonlatToStereo(coord)
					newLine.append(newCoord)

				newMultiVert.append(newLine)

			body.multiVertices=newMultiVert

		newGrid=[]
		for line in self.view.radec.grid:

			newLine=[]

			for coord in line:

				newCoord = self.lonlatToStereo(coord)
				newLine.append(newCoord)

			newGrid.append(newLine)

		self.projectedRadec.grid=newGrid

		# And other data types after this too

		return 1

	def lonlatToStereo(self, point): # TODO this is known to throw a /0 error for projecting from 0,0 for some reason

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

		self.storagePath = os.path.join(os.path.dirname(__file__),'../output/images/',self.projection.view.cond.name)

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

		# Draw in the RADEC grid

		for index, line in enumerate(self.projection.projectedRadec.grid):

			for jindex, start in enumerate(line):

				if jindex < len(line)-1:

					x1 = round(scaleX(start[0]))
					y1 = round(scaleY(start[1]))
					end = self.projection.projectedRadec.grid[index][jindex+1]
					x2 = round(scaleX(end[0]))
					y2 = round(scaleY(end[1]))

					col='blue'

					draw.line([x1,y1,x2,y2],width=1,fill=col)

		# Draw in the constellations as lines for now. TESTING

		for index, body in enumerate(self.projection.projectedConstellations):

			for jindex, segment in enumerate(body.multiVertices):

				for kindex, start in enumerate(segment):

					if kindex < len(segment)-1:

						x1 = round(scaleX(start[0]))
						y1 = round(scaleY(start[1]))
						end = self.projection.projectedConstellations[index].multiVertices[jindex][kindex+1]
						x2 = round(scaleX(end[0]))
						y2 = round(scaleY(end[1]))

						col='red'

						draw.line([x1,y1,x2,y2],width=1,fill=col)

		# Put in some descriptive text to annotate the image

		# fnt = ImageFont.load_default()
		fnt = ImageFont.truetype("arial.ttf", 40)
		caption=self.projection.view.cond.name
		draw.text((20, self.majorDim-60), caption, font=fnt, fill='green')

		outputfilepath = os.path.join(self.storagePath, dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f.png"))
		pic.save(outputfilepath)
	
