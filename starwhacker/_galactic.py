# _galactic.py

# imports

from starwhacker._coordinates import position, polyline, multiPolyline
from starwhacker._tools import makeInterpolator, clamp
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
		self.posRand = 0.3
		self.centre.RA+=((random.random()-0.5)*2*self.posRand)
		self.centre.dec+=((random.random()-0.5)*2*self.posRand) # Todo change this to a normal distribution?

		# Create a list of positions that surround the centre, radius proportional to weight, and then disturb them in or out.

		self.angleRand=5
		self.radRand=0.2*self.weight
		angles = [(theta + (random.random()-0.5)*2*self.angleRand)*2*math.pi/360 for theta in range(0,361,45)]
		
		# First and last must be identical
		fl=((random.random()-0.5)*2*self.angleRand)*2*math.pi/360
		angles[0]=fl
		angles[-1]=fl

		tempPolyline=[]
		for theta in angles:
			r=(random.random()-0.5)*2*self.radRand
			tempPolyline.append(position(self.centre.RA + (self.weight+r)*math.sin(theta), self.centre.dec + (self.weight+r)*math.cos(theta)))
		
		super().__init__(tempPolyline)

class galaxy(multiPolyline):
	'''A class holding many galacticBlobs, extending multiPolyline'''

	def __init__(self, sourceImage, samplesPerUnit):

		self.source=Image.open('./data/'+sourceImage)
		self.samplesPerUnit=samplesPerUnit
		self.degToPixScaleX=makeInterpolator([-180, 180],[0, self.source.width-1])
		self.degToPixScaleY=makeInterpolator([-90, 90],[self.source.height-1, 0]) # Image pixels are upside down, naturally

		super().__init__(self.makePopulation())

	def makePopulation(self):
		'''
		Populate the galaxy with a set galacticBlobs
		'''

		# We will take the source image and scan over it in a grid pattern using samplesPerUnit

		totalSteps=self.samplesPerUnit*360
		tempCollection=[]
		for i in range(int(-totalSteps/2), int(totalSteps/2) + 1, self.samplesPerUnit):
			for j in range(int(-totalSteps/4), int(totalSteps/4) + 1, self.samplesPerUnit): # Only +- 90 degrees in declination

				# Find the pixelwise and radec position
				iDeg = i/self.samplesPerUnit
				jDeg = j/self.samplesPerUnit
				iPix = clamp(int(self.degToPixScaleX(iDeg)),1,self.source.width)
				jPix = clamp(int(self.degToPixScaleY(jDeg)),1,self.source.height)
				# At each position we find the 'weight' by sampling the brightness

				(r,g,b,a)=self.source.getpixel((iPix,jPix))
				w=1*(r+g+b)/(3*255)
				if w>0.1:
					tempCollection.append(galacticBlob(position(iDeg, jDeg), w))

		return tempCollection