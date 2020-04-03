# _sky.py

# imports

import os
import json
import configparser

from starwhacker._stars import star
from starwhacker._coordinates import position, polyline

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
		
		# 
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
