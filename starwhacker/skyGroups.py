# skyGroups.py

# defines the sky, skyViews and projections

# imports
import os
import json
from starwhacker.celestialObjects import *
from starwhacker.starTools import *
import configparser

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

		# We want to know about min and max values for:
		# RA/Dec, Magnitude, BV

		RAs = list(body.RA for body in self.stars)
		self.rangeRA = [min(RAs),max(RAs)]
		decs = list(body.dec for body in self.stars)
		self.rangeDec = [min(decs),max(decs)]
		mags = list(body.mag for body in self.stars)
		self.rangeMag = [min(mags),max(mags)]
		BVs = list(body.BV for body in self.stars)
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

		self.name = viewName

		# Change this to check from the bounds config:

		self.stars = self.fullSky.stars

	def update():

		# Take the config file and scrape the parent fullSky object's starlist to find stars that match our requirements

		# This might include a named view self.name

		return self





# class projection():