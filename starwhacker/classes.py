## Class definitions
import os
import sys
import configparser
import datetime
import math
import json


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

		self.stars = []

	def getStarCount(self):

		return len(self.stars)

	def addStarsFromJSON(self, jsonfile):

		with open(jsonfile, encoding='utf8') as starfile:  # encoding ensures there are no invalid characters - some star names are not provided in unicode.

			stardict = json.load(starfile)

			for body in stardict['features']:

				self.stars.append(star().setID(int(body['id'])).setMagnitude(float(body['properties']['mag'])).setLatLon(body['geometry']['coordinates'][0],body['geometry']['coordinates'][1]))

			return self





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



