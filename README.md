inkscape-paintbynumber
======================

An extension for Inkscape to create a "Paint by Number" picture.

## What is Paint by Numbers?
An image where you have numbered dots which you need to connect to reveal the hidden image. It is a fun activity for kids and grown-ups as well.

Currently, Paint by Numbers extension places not all the numbers optimally, so some manual adjustment may be necessary.


## Installation
1. Copy *paintbynumbers.inx* and *paintbynumbers.py* into your share/inkscape/extension folder (may require admin rights.)
2. (re)-start Inkscape.
3. You will find a new entry in Extensions > Generate from Path > Paint by Numbers.


## Usage
1. Import the image you want to make into a Paint by Numbers picture into Inkscape.
2. Draw a path using *Draw Bezier Curves and Straight Lines* (Shift+F6) on the outline of the desired image part (Hint: Lock layer with the image in it.)
3. Select one or more paths.
4. Go to Extensions > Generate from Path > Paint by Numbers. Note: the Paint by Numbers Extension will enumerate the dots starting at 1 for every path separately!
5. Adjust Options and click **Apply** - Use *Live preview* if you are unsure about some options.
6. Hide all parts of the image you don't want included in your Paint By Numbers picture.
7. Optional: Adjust position of vertices and numbers if desired.
8. Export image to a raster graphics.
9. Print and have fun!