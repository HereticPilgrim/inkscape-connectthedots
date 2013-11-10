inkscape-connectthedots
======================

An extension for Inkscape to create a "Connect the Dots" picture.

## What is Connect the Dots?
An image where you have numbered dots which you need to connect to reveal the hidden image. It is a fun activity for kids and grown-ups as well.

Note: Currently, Connect the Dots extension places not all the numbers optimally, so some manual adjustment may be necessary.


## Installation
1. Copy *connectthedots.inx* and *connectthedots.py* into your share/inkscape/extension folder (may require admin rights.)
2. (re)-start Inkscape.
3. You will find a new entry in Extensions > Generate from Path > Create Connect the Dots.


## Usage
1. Import the image you want to make into a Connect the Dots picture into Inkscape.
2. Draw a path using *Draw Bezier Curves and Straight Lines* (Shift+F6) on the outline of the desired image part (Hint: Lock layer with the image in it.)
3. Select one or more paths.
4. Go to Extensions > Generate from Path > Create Connect the Dots. Note: the Connect the Dots extension will enumerate the dots starting at 1 for each path separately!
5. Adjust Options and click **Apply** - Use *Live preview* if you are unsure about some options.
6. Hide all parts of the image you don't want included in your Connect the Dots picture.
7. Optional: Adjust position of vertices and numbers if desired.
8. Export image to a raster graphics.
9. Print and have fun!