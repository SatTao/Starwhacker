## Class definitions
import os
import sys
import configparser
import datetime
import math
import json
from PIL import Image ImageDraw # Handles image writing for debugging
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

		print('Making the sky')

		self.pwd = os.path.dirname(__file__) # Gets absolute path to the directory that contains this file, not calling location.

		self.stars = []

		self.constellations = []

	def getStarCount(self):

		return len(self.stars)

	def addStarsFromJSON(self, jsonfile):

		with open(jsonfile, encoding='utf8') as starfile:  # encoding ensures there are no invalid characters - some star names are not provided in unicode.

			stardict = json.load(starfile)

			for body in stardict['features']:

				self.stars.append(star().setID(int(body['id'])).setMagnitude(float(body['properties']['mag'])).setLatLon(body['geometry']['coordinates'][0],body['geometry']['coordinates'][1]))

		return self

	def addConstellationsFromJSON(self, jsonfile):

		return self #TODO

	def drawSkyImage(self, imageDim, northBound, southBound, eastBound, westBound):

		# Get dimensions of image based on bounds of skymap, assume rectangular projection. Don't allow overedge sections.

		vertExtent = int(abs(northBound-southBound))
		horizExtent = int(abs(eastBound-westBound))

		if horizExtent >=vertExtent :
			imageWidth = int(imageDim)
			imageHeight = int(imageDim*(vertExtent/horizExtent))
		else:
			imageHeight = int(imageDim)
			imageWidth = int(imageDim*(horizExtent/vertExtent))

		# Create a blank, black image

		pic = Image.new('RGB', (imageWidth, imageHeight), 'black') #TODO change
		pic.save(dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.png"))



class star:

	def __init__(self):

		print('Made a star')

	def setID(self, ID):

		self.ID=ID

		return self

	def setMagnitude(self, mag):

		self.mag = mag

		return self

	def setLatLon(self, lat, lon):

		self.lat = lat
		self.lon = lon

		return self

	def setRADec(self, RA, dec):

		self.RA = RA
		self.dec = dec

		return self



