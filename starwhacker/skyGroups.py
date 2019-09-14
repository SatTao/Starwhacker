# skyGroups.py

# defines the sky, skyViews and projections

# imports
import os
import json
from starwhacker.celestialObjects import *
from starwhacker.starTools import *
from funcTools import reduce

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

		self.doStats()

		return self

	def addConstellationsFromJSON(self, jsonfile):

		return self #TODO

	def doStats(self):

		# We want to know about min and max values for:
		# RA/Dec, Magnitude, BV

		RAs = (body.RA for body in self.stars)
		self.rangeRA = [min(RAs),max(RAs)]
		decs = (body.dec for body in self.stars)
		self.rangeDec = [min(decs),max(decs)]
		mags = (body.mag for body in self.stars)
		self.rangeMag = [min(mags),max(mags)]
		BVs = (body.BV for body in self.stars)
		self.rangeBV = [min(BVs),max(BVs)]

# class skyView():