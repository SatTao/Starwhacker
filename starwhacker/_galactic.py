# _galactic.py

# imports

from starwhacker._coordinates import position, polyline, multiPolyline
import math
import random
import os 
from PIL import Image, ImageDraw, ImageFont
import datetime

class galacticBlob(polyline):
	'''A class defining a blob centred on a position in the galaxy, sized and shaped according to the galactic density'''

	def __init__(self, pos, weight):

		self.weight=weight
		self.centre=pos

		# Randomise the centre position by plus or minus a certain amount maximum
		self.posRand = 0.5
		self.centre.RA+=((random.random()-0.5)*2*self.posRand)
		self.centre.dec+=((random.random()-0.5)*2*self.posRand) # Todo change this to a normal distribution?

		# Create a list of positions that surround the centre, radius proportional to weight, and then disturb them in or out.

		self.angleRad=3
		self.radRand=0.1
		angles = [(theta + (random.random()-0.5)*2*self.angleRad) for theta in range(0,361,15)]
		tempPolyline=[]
		for theta in angles:
			r=(random.random()-0.5)*2*self.radRand
			tempPolyline.append(position(self.centre.RA + r*math.sin(theta), self.centre.dec + r*math.cos(theta)))
		
		super().__init__(tempPolyline)

class galaxy(multiPolyline):
	'''A class holding many galacticBlobs, extending multiPolyline'''

	def __init__(self, sourceImage, samplesPerUnit):

		self.source=Image.open('./data/'+sourceImage)
		self.samplesPerUnit=samplesPerUnit

	def populate():
		'''
		Populate the galaxy with a set galacticBlobs
		'''

		return None

	def filter():
		'''
		Filter the included galacticPoints to include only those within the boundary
		'''

		return None