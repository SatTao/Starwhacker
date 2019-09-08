## Class definitions
import os
import sys
import configparser
import datetime
import math
import json
from PIL import Image, ImageDraw # Handles image writing for debugging NOTE this assumes Pillow, not original PIL
import datetime as dt

class board:

	def __init_(self):

		print('Made a board')

	def setGridSize(self, gridSize):

		self.gridSize = gridSize

	def setMaxDimensions(self, maxWidth, maxHeight):

		self.maxWidth = maxWidth
		self.maxHeight = maxHeight

class sky:

	def __init__(self):

		self.pwd = os.path.dirname(__file__) # Gets absolute path to the directory that contains this file, not calling location.

		self.stars = []

		self.constellations = []

		self.starsMaxMag = 0
		self.starsMinMag = 100 # lol hacky but who cares

	def getStarCount(self):

		return len(self.stars)

	def addStarsFromJSON(self, jsonfile):

		with open(jsonfile, encoding='utf8') as starfile:  # encoding ensures there are no invalid characters - some star names are not provided in unicode.

			stardict = json.load(starfile)

			for body in stardict['features']:

				newstar = star().setID(int(body['id'])).setMagnitude(float(body['properties']['mag'])).setLonLat(body['geometry']['coordinates'][0],body['geometry']['coordinates'][1])
				
				try:
					newstar.setBVIndex(float(body['properties']['bv']))
				except:
					newstar.setBVIndex(0.0) # Because some of them have no BV index listed YAB

				self.stars.append(newstar)

				# Keep track of the range of magnitudes in the sky right now

				if newstar.mag > self.starsMaxMag:
					self.starsMaxMag = newstar.mag
				if newstar.mag < self.starsMinMag:
					self.starsMinMag = newstar.mag

		return self

	def addConstellationsFromJSON(self, jsonfile):

		return self #TODO

	def drawSkyImage(self, imageDim, bounds):

		# Get dimensions of image based on bounds of skymap, assume rectangular projection. Don't allow overedge sections.

		# bounds looks like [lonmin, latmin, lonmax, latmax]

		[westBound, southBound, eastBound, northBound] = bounds

		vertExtent = int(abs(northBound-southBound))
		horizExtent = int(abs(eastBound-westBound))

		if horizExtent >= vertExtent :
			imageWidth = int(imageDim)
			imageHeight = int(imageDim*(vertExtent/horizExtent))
		else:
			imageHeight = int(imageDim)
			imageWidth = int(imageDim*(horizExtent/vertExtent))

		# Create a blank, black image

		pic = Image.new('RGB', (imageWidth, imageHeight), 'black')

		draw = ImageDraw.Draw(pic) # Create a drawing object

		# Mark the positions and relative sizes of the stars naively for now

		for star in self.stars:

			if (star.lat > southBound and star.lat < northBound and star.lon > westBound and star.lon < eastBound):

				starRad = math.ceil(6 * (1 - (star.mag / (self.starsMaxMag - self.starsMinMag))))

				[starPosx, starPosy] = self.linearMap([star.lon,star.lat],[westBound, southBound, eastBound, northBound],[0,0,imageWidth,imageHeight])

				redHue = 200 + int(star.BV*25)
				blueHue = 225 - int(star.BV*25)

				draw.ellipse([starPosx-starRad,starPosy-starRad,starPosx+starRad,starPosy+starRad],fill=(redHue,200,blueHue,0))

		# save the image to the appropriate output folder

		outputfilepath = os.path.join(os.path.dirname(__file__),'../output/images/', dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.png"))
		pic.save(outputfilepath)

	def linearMap(self, inputPoint, inputBounds, outputBounds):

		# inputPoint is [x, y] in original coordinate system
		# inputBounds is [xmin, ymin, xmax, ymax] for input coordinate system
		# outputBounds is [xmin, ymin, xmax, ymax] for output coordinate system

		outx = int(outputBounds[0] + (outputBounds[2]-outputBounds[0]) * (inputPoint[0]-inputBounds[0]) / (inputBounds[2]-inputBounds[0] ))
		outy = outputBounds[3] - int(outputBounds[1] + (outputBounds[3]-outputBounds[1]) * (inputPoint[1]-inputBounds[1]) / (inputBounds[3]-inputBounds[1] )) # account for -ve y coordinates in images

		return [outx, outy]

class star:

	def __init__(self):

		a=1

	def setID(self, ID):

		self.ID=ID

		return self

	def setMagnitude(self, mag):

		self.mag = mag

		return self

	def setLonLat(self, lon, lat):

		self.lat = lat
		self.lon = lon

		return self

	def setRADec(self, RA, dec):

		self.RA = RA
		self.dec = dec

		return self

	def setBVIndex(self, BV):

		self.BV = BV

		return self



