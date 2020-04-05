# _sky.py

# imports

import os
import json
import configparser

from starwhacker._stars import star
from starwhacker._coordinates import position, polyline
from starwhacker._tools import makeInterpolator

# Defines the sky class which holds data on stars and other celestial objects of interest. 
# A sky can be cropped and projected and filtered to leave only objects of interest.
# We do not anticipate re-using a sky over multiple projections or regions.

class sky():
	'''A class which defines a sky containing objects, and may have projections and views applied'''

	def __init__(self, objectDict=None):

		# The following dictionary holds all the objects of the sky

		if objectDict==None:
			self.objects = {
			'stars':[],
			'constellations':[],
			'DSOs':[],
			'grid':None,
			'boundary':None
			}
		else:
			self.objects=objectDict

	# Functions for adding objects to the sky

	def addStarsFromJson(self, jsonFile):
		'''
		Adds stars defined in a supplied json file to the objects dictionary.
		'''

		stardict=None
		# encoding ensures there are no invalid characters - some star names are not provided in unicode.
		with open(os.path.join(os.path.dirname(__file__),'../data',jsonFile), encoding='utf8') as starfile: 
			stardict = json.load(starfile) # Load the file into a temporary dictionary
		
		
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

			newStar = star(thisID, 
				thisRA, 
				thisDec, 
				thisMag, 
				thisBV, 
				thisDesig, 
				thisCon)

			self.objects['stars'].append(newStar)

		return self

	# Simple utility functions

	def vitalStatistics(self):
		'''
		Print out a summary of the stars, constellations and ranges in our list of stars
		'''

		# Check if this is a named skyView or just a sky

		print('\nThis sky contains:\n')

		print('STARS ({0})'.format(len(self.objects['stars'])))
		RAs = [body.RA for body in self.objects['stars']]
		print('RA\tMin: ~{0:0.2f} \tMax: ~{1:0.2f} \tdegrees'.format(min(RAs), max(RAs)))
		decs = [body.dec for body in self.objects['stars']]
		print('Dec\tMin: ~{0:0.2f} \tMax: ~{1:0.2f} \tdegrees'.format(min(decs), max(decs)))
		mags = [body.mag for body in self.objects['stars']]
		print('Mag\tMin: ~{0:0.2f} \tMax: ~{1:0.2f} '.format(min(mags), max(mags)))
		BVs = [body.BV for body in self.objects['stars']]
		print('BV\tMin: ~{0:0.2f} \tMax: ~{1:0.2f} '.format(min(BVs), max(BVs)))

		print('\nCONSTELLATIONS ({0})\n'.format(len(self.objects['constellations'])))
		
		# TODO print('CONSTELLATIONS') data etc etc

		return None

	# Self-modification functions

	def filter(self,configurationName):
		'''
		Filter the objects of the sky to include only those matching a set of conditions.

		Conditions are defined in a named block (configurationName) in the _bounds.ini file.

		Later we may overload this function to allow for inline condition setting too.
		'''

		# First we read data from the relevant block in the configuration file

		config=configparser.ConfigParser()
		config.read(os.path.join(os.path.dirname(__file__),'../config','_bounds.ini'))

		self.name=config[configurationName]['name']

		self.objects['boundary'] = polyline([position(p[0],p[1]) for p in json.loads(config[configurationName]['boundary'])])
		mags=json.loads(config[configurationName]['mags'])
		BVs=json.loads(config[configurationName]['BVs'])

		# Then we filter stars based on this data

		self.objects['stars'] = list(filter(lambda x: x.matches(self.objects['boundary'], mags, BVs),self.objects['stars']))

		# Later we will filter other object types here too

		return self

	def interpolate(self, nodesPerUnit):
		'''
		Tell all of our interpolatable objects to interpolate themselves.
		'''

		if self.objects['constellations']:
			for con in self.objects['constellations']:
				con.interpolate(nodesPerUnit)

		if self.objects['boundary']:
			self.objects['boundary'].interpolate(nodesPerUnit)

		if self.objects['grid']:
			self.objects['grid'].interpolate(nodesPerUnit)

		return None

	def stereoProject(self, lonLatCentroid=position(0,0), R=100):
		'''
		Projects all objects in the sky stereographically, about a centroid, with an R value.
		'''

		# All objects in self.objects need to be projected.

		for key in self.objects.keys():

			# If an entry in the objects dictionary is not populated then skip it.
			if type(self.objects[key]) is type(None):
				continue

			# If it's a list, then each entry in the list will offer a projection method.
			elif type(self.objects[key]) is list:
				for item in self.objects[key]:
					item.stereoProject(lonLatCentroid,R)

			# If it's a single item (e.g. the boundary or RADEC grid), then do the stereo projection on it.
			else:
				self.objects[key].stereoProject(lonLatCentroid,R)

		return self

	def normalise(self):
		'''
		Centre everything about 0,0 and squash/stretch it so the greatest extents are -1->+1
		'''

		# Get the current extents from the boundary [[minRA, maxRA],[minDec, maxDec]]
		# The greatest extents will map to -1 > +1, the other axis less.

		[[minRA,maxRA],[minDec,maxDec]] = self.objects['boundary'].getExtents()

		# Find the dead centres on each axis, because we need to scale and translate

		cRA = minRA+(maxRA-minRA)/2
		cDec = minDec+(maxDec-minDec)/2

		# Modify the ranges as if they were centred on 0,0

		minRA=minRA-cRA
		maxRA=maxRA-cRA

		minDec=minDec-cDec
		maxDec=maxDec-cDec

		# Find which axis has a greater extent

		greater = [minRA, maxRA] if max((maxRA-minRA),(maxDec-minDec)) == (maxRA-minRA) else [minDec, maxDec]

		# Make an interpolator (we will use it on both axes)

		scalefunc = makeInterpolator(greater,[-1,1])
		c=position(cRA,cDec)

		# Scale each axis respecting the orignal centroid so that everything ends up centred on 0,0

		for key in self.objects.keys():

			# If an entry in the objects dictionary is not populated then skip it.
			if type(self.objects[key]) is type(None):
				continue

			# If it's a list, then each entry in the list will offer a scale and centre method.
			elif type(self.objects[key]) is list:
				for item in self.objects[key]:
					item.scaleAndCentre(scalefunc,c)

			# If it's a single item (e.g. the boundary or RADEC grid), then do the stereo projection on it.
			else:
				self.objects[key].scaleAndCentre(scalefunc,c)		

		return self