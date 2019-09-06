## Class definitions
import os
import sys
import configparser
import datetime
import math

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

		print('ok')

class star:

	def __init__(self):

		print('Made a star')

	def setLatLon(self, lat, lon):

		self.lat = lat
		self.lon = lon

	def setRADec(self, RA, dec):

		self.RA = RA
		self.dec = dec



