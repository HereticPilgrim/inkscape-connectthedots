#!/usr/bin/env python
'''
Paint by Number extension for Inkscape Vector Graphics Editor
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

from random import randint
from math import pi, acos, sqrt, degrees

import inkex
import simplepath
import simplestyle
import gettext
_ = gettext.gettext

class PaintByNumber(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option('-p', '--hidepath', action = 'store',
									 type = 'string', dest = 'hidepath', default = True,
									 help = 'Hide the original path after completion?')
		self.OptionParser.add_option('-r', '--radius', action = 'store',
									 type = 'string', dest = 'radius', default = 10,
									 help = 'Radius of the dots at every vertex of the path')


	def effect(self):
		svg = self.document.getroot()

		# create new layers for dots and for numbers
		dotLayer = inkex.etree.SubElement(svg, 'g')
		dotLayer.set(inkex.addNS('label', 'inkscape'), 'PaintByNumber dotLayer')
		dotLayer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

		numberLayer = inkex.etree.SubElement(svg, 'g')
		numberLayer.set(inkex.addNS('label', 'inkscape'), 'PaintByNumber numberLayer')
		numberLayer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

		for id, path in self.selected.iteritems():
			if path.tag == 'path' or path.tag == inkex.addNS('path','svg'):
				d = path.get('d')
				
				vertices = simplepath.parsePath(d)
				r = float(self.options.radius)
				h = inkex.unittouu(svg.get('height'))

				# iterate over vertices and draw dots on each as well as the number next to it
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

					# draw numbers
					token = randint(0,3)
					if token == 0:
						# place number left of the dot
						nx = x-2*r
						ny = y
					elif token == 1:
						# place number above dot
						nx = x
						ny = y+2*r
					elif token == 2:
						# place number to the right
						nx = x+2*r
						ny = y
					else:
						# place number below dot
						nx = x
						ny = y-2*r
						
					## place numbers according in largest available angle of vectors - BUGGY
					# if idx > 0 and idx < len(vertices)-1:
						# x1,y1 = self.getXY(vertices[idx-1])
						# x2,y2 = x,y
						# x3,y3 = self.getXY(vertices[idx+1])

						# u1,v1 = x2-x1,y2-y1
						# u2,v2 = x3-x2,y3-y2

						# alpha = degrees(acos((u1*u2 + v1*v2)/(sqrt((u1**2+v1**2)*(u2**2+v2**2)))))
						# msg = '%i %f' % (idx, alpha)
						# inkex.errormsg(msg)

						# if alpha >= 0 and alpha <= 45:
						# 	# place number left of the dot
						# 	nx = x-3*r
						# 	ny = y
						# elif alpha > 45 and alpha <= 180:
						# 	# place number above dot
						# 	nx = x
						# 	ny = y+3*r
						# elif alpha > 180 and alpha <= 315:
						# 	# place number to the right
						# 	nx = x+3*r
						# 	ny = y
						# elif alpha > 315:
						# 	# place number below dot
						# 	nx = x
						# 	ny = y-3*r
					# else:
						# special case for the first number
						# nx,ny = 5,5

					number = inkex.etree.Element(inkex.addNS('text', 'svg'))
					number.text = str(idx+1)
					number.set('x', str(nx))
					number.set('y', str(ny))

					numberLayer.append(number)


				# hide the original path if specified in options
				if self.options.hidepath == 'true':
					path.set('display', 'none')

	
	def getXY(self, vertex):
		c, (x, y) = vertex
		return x,y


# create effect instance and apply it.
if __name__ == '__main__':
    e = PaintByNumber()
    e.affect()