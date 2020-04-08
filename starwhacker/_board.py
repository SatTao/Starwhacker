# _board.py

# Defines the board class.

# imports

import os
import datetime

from starwhacker._tools import makeRandomString, makeInterpolator, getStarSize
from starwhacker._kicadtemplates import templates 

class board():

	def __init__(self, fromSky, majorDim, targetConstellation='XXX'):

		self.sky = fromSky
		self.majorDim = majorDim
		self.targetConstellation=targetConstellation
		self.diagOffset=20
		self.scaleX = makeInterpolator([-1,1],[0+self.diagOffset,self.majorDim+self.diagOffset])
		self.scaleY = makeInterpolator([-1,1],[self.majorDim+self.diagOffset, 0+self.diagOffset])

		self.storagePath=os.path.join(os.path.dirname(__file__),'../output/_boards/',self.sky.name)
		if not os.path.isdir(self.storagePath):
			os.mkdir(self.storagePath)
		
	def render(self):

		filename=os.path.join(self.storagePath, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.kicad_pcb"))

		with open(filename, 'w') as file:

			# Write the file header
			self.doHeader(file, self.sky.name)

			# Write the Boundary
			self.doBoundary(file, self.sky.objects['boundary'].vertices)

			# Open a module containing the stars
			self.doOpenModule(file, 'STARS', 'F.Cu', 0, 0, 'ftprnt_STARS', 'ftprnt_STARS')

			# Insert the stars
			# Get a list of the magnitudes of the relevant stars
			starmags=[point.mag for point in self.sky.objects['stars']]
			ringmin=.8 # diameter in mm
			ringmax=4
			starScale = makeInterpolator([max(starmags),min(starmags)], [ringmin, ringmax])

			for index, point in enumerate(self.sky.objects['stars']):
				[size, drill] = getStarSize(point, starScale)
				self.doStar(file, index, self.scaleX(point.RA), self.scaleY(point.dec), size, drill, point.name)

			# Close the module
			self.doCloseModule(file)

			# Open a module containing the radec grid silkscreen
			self.doOpenModule(file, 'RADEC', 'F.Cu', 0, 0, 'ftprnt_RADEC', 'ftprnt_RADEC')

			# Insert the radec grids as silkscreen lines
			self.doGrid(file, self.sky.objects['grid'].collection)

			# Close the module
			self.doCloseModule(file)

			# Insert the constellations as traces with mask-free lines over the top
			for con in self.sky.objects['constellations']:
				self.doConstellation(file, con)

			# Write the final bracket
			file.write(templates['ender'])
		
		return None

	def doHeader(self, file, boardName):
		file.write(templates['header'].format(boardName,datetime.datetime.now().strftime("%Y-%m-%d")))
		return None

	def doBoundary(self, file, boundary):
		for index, vertex in enumerate(boundary):
			if index < len(boundary)-1:
				x1 = self.scaleX(vertex.RA)
				y1 = self.scaleY(vertex.dec)
				end = boundary[index+1]
				x2 = self.scaleX(end.RA)
				y2 = self.scaleY(end.dec)
				file.write(templates['edge'].format(x1,y1,x2,y2))

		return None

	def doOpenModule(self, file, moduleName, moduleLayer, modPosX, modPosY, modRef, modVal):
		file.write(templates['openModule']
			.format(moduleName, 
				moduleLayer, 
				makeRandomString(length=8,upper=True), 
				makeRandomString(length=8,upper=True), 
				modPosX, 
				modPosY, 
				modRef, 
				modVal))

		return None

	def doCloseModule(self, file):
		file.write(templates['closeModule'])

		return None

	def doStar(self, file, padNum, posX, posY, size, drill, name):
		if drill!=0:
			file.write(templates['TH_star'].format(padNum, posX, posY, size, size, drill))
		else:
			file.write(templates['SMD_star'].format(padNum, posX, posY, size, size))
		# if the star has a name
		if len(name):
			self.doSilkScreenText(file, name, posX+2.5, posY, 2, back=True)

		return None

	def doGrid(self, file, grid):

		for section in grid:
			for index, vertex in enumerate(section.vertices):
				if index < len(section.vertices)-1:
					x1 = self.scaleX(vertex.RA)
					y1 = self.scaleY(vertex.dec)
					end = section.vertices[index+1]
					x2 = self.scaleX(end.RA)
					y2 = self.scaleY(end.dec)
					file.write(templates['silk_line'].format(x1,y1,x2,y2))

		return None

	def doSilkScreenText(self, file, text, posX, posY, size, back=False):

		if not back:
			file.write(templates['silk_text'].format(text, posX, posY, size, size))
		else:
			file.write(templates['silk_text_back'].format(text, posX, posY, size, size))

		return None

	def doConstellation(self, file, con):

		for section in con.collection:
			for index, vertex in enumerate(section.vertices):
				if index < len(section.vertices)-1:
					x1 = self.scaleX(vertex.RA)
					y1 = self.scaleY(vertex.dec)
					end = section.vertices[index+1]
					x2 = self.scaleX(end.RA)
					y2 = self.scaleY(end.dec)
					w=0.5
					if con.name.lower()==self.targetConstellation.lower():
						w=1
					file.write(templates['constellation_line'].format(x1,y1,x2,y2, w))

















