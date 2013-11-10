#!/usr/bin/env python
'''
Connect the Dots extension for Inkscape Vector Graphics Editor
Copyright (C) 2013  Manuel Grauwiler (HereticPilgrim)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from random import randint, choice
from math import pi, acos, sqrt, degrees

import inkex
import simplepath
import simplestyle
import gettext
_ = gettext.gettext

class ConnectTheDots(inkex.Effect):
	TOP_RIGHT = 1
	TOP_LEFT = 2
	BOTTOM_LEFT = 3
	BOTTOM_RIGHT = 4
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option('-p', '--hidepath', action = 'store',
									 type = 'string', dest = 'hidepath', default = True,
									 help = 'Hide the original path after completion?')
		self.OptionParser.add_option('-r', '--radius', action = 'store',
									 type = 'string', dest = 'radius', default = 10,
									 help = 'Radius of the dots at every vertex of the path')
		self.OptionParser.add_option('-f', '--fontsize', action = 'store',
									 type = 'string', dest = 'fontsize', default = 10,
									 help = 'Font size of the numbers')


	def effect(self):
		svg = self.document.getroot()

		# create new layers for dots and for numbers
		dotLayer = inkex.etree.SubElement(svg, 'g')
		dotLayer.set(inkex.addNS('label', 'inkscape'), 'ConnectTheDots dotLayer')
		dotLayer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

		numberLayer = inkex.etree.SubElement(svg, 'g')
		numberLayer.set(inkex.addNS('label', 'inkscape'), 'ConnectTheDots numberLayer')
		numberLayer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

		# iterate over every path, start numbering from 1 every time
		for id, path in self.selected.iteritems():
			if path.tag == 'path' or path.tag == inkex.addNS('path','svg'):
				# radius and fontsize as offsets to avoid placing numbers inside dots
				r = float(self.options.radius)
				f = 0.5*int(self.options.fontsize)

				# iterate over vertices and draw dots on each as well as the number next to it
				d = path.get('d')
				vertices = simplepath.parsePath(d)
				for idx, v in enumerate(vertices):
					x,y = self.getXY(v)

					# create dots
					style = {
						'stroke': 'none',
						'stroke-width': '0',
						'fill': '#000000'
					}
					name = 'pbn_%i' % idx
					attributes = {
						'style': simplestyle.formatStyle(style),
						inkex.addNS('cx', 'sodipodi') : str(x),
						inkex.addNS('cy', 'sodipodi') : str(y),
						inkex.addNS('rx', 'sodipodi') : self.options.radius,
						inkex.addNS('ry', 'sodipodi') : self.options.radius,
						inkex.addNS('start', 'sodipodi') : str(0),
						inkex.addNS('end', 'sodipodi') : str(2*pi),
						inkex.addNS('open', 'sodipodi') : 'false',
						inkex.addNS('type', 'sodipodi') : 'arc',
						inkex.addNS('label','inkscape') : name
					}
					dot = inkex.etree.SubElement(dotLayer, inkex.addNS('path', 'svg'), attributes)

					if idx > 0 and idx < len(vertices)-1:
						# block two quadrants, one for the previous and one for the next
						freeQuads = self.findFreeQuadrants((x,y), self.getXY(vertices[idx-1]), self.getXY(vertices[idx+1]))
					else:
						# special case for end nodes, only block one quadrant
						freeQuads = self.findFreeQuadrants((x,y), self.getXY(vertices[idx-1]))

					# randomly place number in one of the free quadrants
					q = choice(freeQuads)
					if q == self.TOP_RIGHT:
						nx = x+2*r
						ny = y+2*r+f
						textAnchor = 'start'
					elif q == self.TOP_LEFT:
						nx = x-2*r
						ny = y+r+f
						textAnchor = 'end'
					elif q == self.BOTTOM_LEFT:
						nx = x-r
						ny = y-r
						textAnchor = 'end'
					else: # BOTTOM_RIGHT
						nx = x+r
						ny = y-r
						textAnchor = 'start'

					# create the number element
					number = inkex.etree.Element(inkex.addNS('text', 'svg'))
					number.text = str(idx+1)
					number.set('x', str(nx))
					number.set('y', str(ny))
					number.set('font-size', self.options.fontsize)
					number.set('text-anchor', textAnchor)
					numberLayer.append(number)

				# hide the original path if specified in options
				if self.options.hidepath == 'true':
					path.set('display', 'none')

	
	def getXY(self, vertex):
		# split vertex info into command and list of parameters
		cmd, params = vertex
		if cmd == 'M' or cmd == 'L':
			'''Not necessary to check for 'm' and/or 'l',
			because pathparser returns only absolute coordinates'''
			x,y = params[0], params[1]
		else:
			'''We are looking at a curved path, or cubic Bezier curve. The last
			coordinate pair in the parameters list determine the point's position,
			see: http://www.w3.org/TR/SVG/paths.html#PathDataCubicBezierCommands'''
			x,y = params[-2:]
		return (x,y)


	def findFreeQuadrants(self, current, previous, next = None):
		'''Determines which quadrants around the current vertex are still available
		for number placement. Returns a list of at least two free quadrants. If next
		is None, the current vertex is treated as a start/end vertex and only one
		vertex is considered for blocking quadrants.'''
		freeQuads = [self.TOP_LEFT, self.TOP_RIGHT, self.BOTTOM_RIGHT, self.BOTTOM_LEFT]
		freeQuads.remove(self.findBlockedQuadrant(current, previous))
		if next != None:
			q = self.findBlockedQuadrant(current, next)
			if q in freeQuads:
				freeQuads.remove(q)
		return freeQuads

		
	def findBlockedQuadrant(self, current, reference):
		'''Determines which quadrant of the current point is blocked for number
		placement by the reference point. E.g. if the reference point is in the
		top right relative to the current point, the TOP_RIGHT quadrant will
		not be allowed for number placement.'''
		x1,y1 = current
		x2,y2 = reference
		if x2 > x1:
			# reference is on the right side
			if y2 > y1:
				return self.TOP_RIGHT
			else:
				return self.BOTTOM_RIGHT
		else:
			# reference is on the right side
			if y2 > y1:
				return self.TOP_LEFT
			else:
				return self.BOTTOM_LEFT



# create effect instance and apply it.
if __name__ == '__main__':
    e = ConnectTheDots()
    e.affect()