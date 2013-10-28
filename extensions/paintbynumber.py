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

from math import pi

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

				# iterate over vertices and draw dots on each as well as the number next to it
				for idx, v in enumerate(vertices):
					c, (x, y) = v


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
					### TODO

				# hide the original path if specified in options
				if self.options.hidepath == 'true':
					path.set('display', 'none')

# create effect instance and apply it.
if __name__ == '__main__':
    e = PaintByNumber()
    e.affect()