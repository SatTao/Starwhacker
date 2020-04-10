# _drawing.py

# A class that defines a drawing object which takes information from a _sky and writes it to an image.

# imports
from starwhacker._sky import sky
from starwhacker._tools import makeInterpolator, clamp, getStarSize

import math
import json
import os 
from PIL import Image, ImageDraw, ImageFont
import datetime

class drawing():
	''' A class that defines a drawing object, which takes data from a sky object and exports it as an image'''

	def __init__(self, fromSky, realMajorDim, targetConstellation='XXX'):

		self.sky=fromSky
		self.pixelsPerMm=10
		self.realMajorDim=realMajorDim
		self.targetConstellation=targetConstellation
		self.majorDim = self.realMajorDim*self.pixelsPerMm
		self.storagePath=os.path.join(os.path.dirname(__file__),'../output/_images/',self.sky.name)
		if not os.path.isdir(self.storagePath):
			os.mkdir(self.storagePath)

	def render(self):
		'''
		Exports a drawing (.png image) to the default path
		'''

		# Make simple square images for now. Doesn't matter if there's blank space.

		scaleX = makeInterpolator([-1,1],[0,self.realMajorDim])
		scaleY = makeInterpolator([-1,1],[self.realMajorDim, 0]) 
		# Since image writing Y axis is upside down

		# NB all star positions will be rounded to nearest pixel out of necessity 

		# Create a blank, black image

		pic = Image.new('RGB', (self.majorDim, self.majorDim),'white')
		draw = ImageDraw.Draw(pic) # Create a drawing object

		# Draw in the board bounded by boundary, in black.

		self.drawPolygon(draw, scaleX, scaleY, self.sky.objects['boundary'].vertices, (10,10,20))

		# Draw in the galactic background (which is copper covered in mask, so underneath all other elements)

		for blob in self.sky.objects['galaxy'].collection:
			if len(blob.vertices)>2:
				self.drawPolygon(draw, scaleX, scaleY, blob.vertices, (30,30,10))

		# Draw in the radec grid crosses in white (silkscreen) (do it first because silkscreen is subtracted from mask)

		for pl in self.sky.objects['grid'].collection:
			self.drawLine(draw, scaleX, scaleY, pl.vertices, 'white', 4)

		# Draw constellations in gold, like the stars 

		for con in self.sky.objects['constellations']:
				w=0.5
				fntsize=24
				if con.name.lower()==self.targetConstellation.lower():
					w=1
					fntsize=36
				for line in con.collection:
					self.drawLine(draw, scaleX, scaleY, line.vertices, 'GoldenRod', math.ceil(w*self.pixelsPerMm))
				fnt = ImageFont.truetype("arial.ttf", fntsize)
				# Get the centre of the visible constellation, and type the name there.
				cen=con.getCentre()
				textx=round(scaleX(cen.RA)*self.pixelsPerMm)
				texty=round(scaleY(cen.dec)*self.pixelsPerMm)
				draw.text((textx, texty), con.name, font=fnt, fill='white')

		# Draw in the stars in gold

		self.drawStars(draw, scaleX, scaleY, self.sky.objects['stars'])

		# Export the image

		outputfilepath = os.path.join(self.storagePath, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f.png"))
		pic.save(outputfilepath)

		return None

	def drawPolygon(self, draw, scaleX, scaleY, _object, fill):
		'''
		Draws a filled polygon in the final image, using the elements of _object as vertices.
		'''

		xy=[]
		for index, point in enumerate(_object):
				xy.append((round(scaleX(point.RA)*self.pixelsPerMm), round(scaleY(point.dec)*self.pixelsPerMm)))

		draw.polygon(xy, fill=fill)

		return None


	def drawLine(self, draw, scaleX, scaleY, _object, col, width, dashed=False):
		'''
		Draws a line in the final image for every element of the list. _object
		'''

		# We will always be passed a list of positions

		for index, point in enumerate(_object):
			if index < len(_object)-1:
				x1 = round(scaleX(point.RA)*self.pixelsPerMm)
				y1 = round(scaleY(point.dec)*self.pixelsPerMm)
				end = _object[index+1]
				x2 = round(scaleX(end.RA)*self.pixelsPerMm)
				y2 = round(scaleY(end.dec)*self.pixelsPerMm)

				colour=col
				if dashed:
					colour=col if index%2==0 else 'black'

				draw.line([x1,y1,x2,y2],width=width,fill=colour)

		return None

	def drawStars(self, draw, scaleX, scaleY, _object):
		'''
		Draws a star in the final image as an anular ring or circle.
		'''

		# Get the range of properties for the stars.

		mags = [body.mag for body in _object]
		# BVs = [body.BV for body in _object]

		# Magnitude maps to size (and shape) (BV maps to colour (in images only), not used)
		ringmin=.8 # diameter in mm
		ringmax=4
		starScale = makeInterpolator([max(mags),min(mags)], [ringmin, ringmax])

		for body in _object:

			starPosx = round(scaleX(body.RA)*self.pixelsPerMm)
			starPosy = round(scaleY(body.dec)*self.pixelsPerMm)

			[padSize, holeSize] = getStarSize(body, starScale)
			padSize=padSize*self.pixelsPerMm
			holeSize=holeSize*self.pixelsPerMm

			draw.ellipse([starPosx-padSize/2,starPosy-padSize/2,starPosx+padSize/2,starPosy+padSize/2],fill='GoldenRod')
			if holeSize>0:
				draw.ellipse([starPosx-holeSize/2,starPosy-holeSize/2,starPosx+holeSize/2,starPosy+holeSize/2],fill='white')

		return None
