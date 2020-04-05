# _drawing.py

# A class that defines a drawing object which takes information from a _sky and writes it to an image.

# imports
from starwhacker._sky import sky
from starwhacker._tools import makeInterpolator

import math
import json
import os 
from PIL import Image, ImageDraw, ImageFont
import datetime

class drawing():
	''' A class that defines a drawing object, which takes data from a sky object and exports it as an image'''

	def __init__(self, fromSky, majorDimension):

		self.sky=fromSky
		self.majorDim = majorDimension
		self.storagePath=os.path.join(os.path.dirname(__file__),'../output/_images/',self.sky.name)
		if not os.path.isdir(self.storagePath):
			os.mkdir(self.storagePath)

	def render(self):
		'''
		Exports a drawing (.png image) to the default path
		'''

		# Make simple square images for now. Doesn't matter if there's blank space.

		scaleX = makeInterpolator([-1,1],[0,self.majorDim])
		scaleY = makeInterpolator([-1,1],[self.majorDim, 0]) 
		# Since image writing Y axis is upside down

		# NB all star positions will be rounded to nearest pixel out of necessity 

		# Create a blank, black image

		pic = Image.new('RGB', (self.majorDim, self.majorDim), 'black')
		draw = ImageDraw.Draw(pic) # Create a drawing object

		# Draw in the boundary in yellow dashed.

		self.drawLine(draw, scaleX, scaleY, self.sky.objects['boundary'].vertices, 'yellow', 3, dashed=True)

		# Export the image

		outputfilepath = os.path.join(self.storagePath, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f.png"))
		pic.save(outputfilepath)

		return None

	def drawLine(self, draw, scaleX, scaleY, _object, col, width, dashed=False):
		'''
		Draws a line in the final image for every element of the list.
		'''

		# We will always be passed a list of positions

		for index, point in enumerate(_object):
			if index < len(_object)-1:
				x1 = round(scaleX(point.RA))
				y1 = round(scaleY(point.dec))
				end = _object[index+1]
				x2 = round(scaleX(end.RA))
				y2 = round(scaleY(end.dec))

				if dashed:
					colour=col if index%2==0 else 'black'

				draw.line([x1,y1,x2,y2],width=width,fill=colour)

		return None

	def drawStar(self, draw, scaleX, scaleY, _object):
		'''
		Draws a star in the final image
		'''

		return None

