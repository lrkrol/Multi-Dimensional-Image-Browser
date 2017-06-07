#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Multi-Dimensional Image Browser 1.01
Copyright 2015 Laurens R Krol
Noctifer.net

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
"""

"""
Rather than browsing through files in alphabetical order, this script
allows files to be browsed through in a multi-dimensional fashion.

The alphabetical ordering of e.g.

    apple-brown.jpg     banana-brown.jpg     pear-brown.jpg
    apple-green.jpg     banana-green.jpg     pear-green.jpg
    apple-yellow.jpg    banana-yellow.jpg    pear-yellow.jpg

would have you browse first through all apples, colour by colour, then
through the bananas, colour by colour, and then the pears.
These files, however, contain two dimensions: fruit type, and colour.
This script makes it possible to jump from the green banana to the
green apple with one button, and from the green apple to the yellow apple
with another.

The script takes a directory, where the images are located, and a pattern,
to parse the file names. File names should be consistent except for the
variable parts, and the variable parts should be separated somehow.
A variable part of the file names representing one dimension is indicated
using an asterisk (*). For the above example, the pattern would be

    *-*.jpg

The script then allows you to browse through the available dimensions
using the keyboard. The keys for the first dimension are under the "1",
i.e. "q" for one up in this dimension, and "a" for one down. "w" and "e"
increase and decrease the second dimension, respectively, and "o" and "l"
represent the ninth dimension. The first two dimensions can additionally
be controlled by the arrow keys.

Dimensions are numbered in the order that they appear in the file names.

Keyboard shortcuts include shift+D to set the directory, and shift+P for
the pattern. Enter applies, escape exits.
"""

import glob
import os
import re
import tkFileDialog
import tkSimpleDialog
from Tkinter import *
from PIL import ImageTk, Image

class mdib():

    def __init__(self):
        self.root = Tk(className = "mdib")

        # setting default directory and file pattern
        self.dir = os.getcwd()
        self.filepattern = "*"

        # adding gui elements
        self.root.config(bg = "white")

        browseButton = Button(self.root, text = "Directory", command = self.setDir)
        browseButton.grid(row = 0, column = 0, sticky = W+E)
        self.dirLabel = Label(self.root, text = self.dir, bg = "white")
        self.dirLabel.grid(row = 0, column = 1, sticky = W)

        patternButton = Button(self.root, text = "Pattern", command = self.setPattern)
        patternButton.grid(row = 1, column = 0, sticky = W+E)
        self.patternLabel = Label(self.root, text = self.filepattern, bg = "white")
        self.patternLabel.grid(row = 1, column = 1, sticky = W)

        updateButton = Button(self.root, text = "Apply", command = self.update)
        updateButton.grid(row = 0, column = 2, rowspan = 2, sticky = W+E+N+S)

        self.infoLabel = Label(self.root, text = "No images loaded")
        self.infoLabel.grid(row = 2, column = 0, columnspan = 3, sticky = W+E)

        self.canvas = Canvas(self.root, width = 0, height = 0)
        self.canvas.grid(row = 4, column = 0, columnspan = 3, sticky = W+E+N+S)
        self.ci = self.canvas.create_image(0, 0, anchor = NW)

        # accepting keyboard input
        self.root.bind("<Right>", lambda x: self.changeDim(0, +1))
        self.root.bind("<Left>", lambda x: self.changeDim(0, -1))
        self.root.bind("<Up>", lambda x: self.changeDim(1, +1))
        self.root.bind("<Down>", lambda x: self.changeDim(1, -1))

        self.root.bind("q", lambda x: self.changeDim(0, +1))
        self.root.bind("a", lambda x: self.changeDim(0, -1))
        self.root.bind("w", lambda x: self.changeDim(1, +1))
        self.root.bind("s", lambda x: self.changeDim(1, -1))
        self.root.bind("e", lambda x: self.changeDim(2, +1))
        self.root.bind("d", lambda x: self.changeDim(2, -1))
        self.root.bind("r", lambda x: self.changeDim(3, +1))
        self.root.bind("f", lambda x: self.changeDim(3, -1))
        self.root.bind("t", lambda x: self.changeDim(4, +1))
        self.root.bind("g", lambda x: self.changeDim(4, -1))
        self.root.bind("y", lambda x: self.changeDim(5, +1))
        self.root.bind("h", lambda x: self.changeDim(5, -1))
        self.root.bind("u", lambda x: self.changeDim(6, +1))
        self.root.bind("j", lambda x: self.changeDim(6, -1))
        self.root.bind("i", lambda x: self.changeDim(7, +1))
        self.root.bind("k", lambda x: self.changeDim(7, -1))
        self.root.bind("o", lambda x: self.changeDim(8, +1))
        self.root.bind("l", lambda x: self.changeDim(8, -1))

        self.root.bind("D", lambda x: self.setDir())
        self.root.bind("P", lambda x: self.setPattern())
        self.root.bind("<Return>", lambda x: self.update())
        self.root.bind("<Escape>", lambda x: self.root.destroy())

        self.root.mainloop()


    def setDir(self):
        self.dir = tkFileDialog.askdirectory()
        self.dirLabel.config(text = self.dir)


    def setPattern(self):
        self.filepattern = tkSimpleDialog.askstring("Pattern", "Indicate a pattern, using * where the file names vary", initialvalue = self.filepattern)
        self.patternLabel.config(text = self.filepattern)
        self.update()


    def update(self):
        # getting files
        self.files = glob.glob(os.path.normpath(self.dir + os.sep + self.filepattern))

        if len(self.files) == 0:
            print "No files matching", self.filepattern, "found in", self.dir
            return

        # extracting dimension values
        regexpattern = self.filepattern.replace('*', '(.*)')
        expression = re.compile(regexpattern)
        self.ndims = re.compile(regexpattern).groups

        self.dimvalues = [[] for i in range(self.ndims)]
        for file in self.files:
            file = file.split(os.sep)[-1]
            match = expression.match(file)
            if match:
                for i in range(1, self.ndims+1):
                    self.dimvalues[i-1].append(match.group(i))

        # keeping only unique values, sorted
        for i in range(self.ndims):
            self.dimvalues[i] = sorted(list(set(self.dimvalues[i])))

        # updating info
        dimsize = str(len(self.dimvalues[0]))
        for d in range(1, self.ndims):
            dimsize += "x" + str(len(self.dimvalues[d]))
        self.info = str(len(self.files)) + " images in " + str(self.ndims) + " (" + dimsize + ") dimensions. "

        # setting current position at the lowest value in all dimensions
        self.current = [0] * self.ndims

        # changing to current position
        self.changeDim(0, 0)


    def changeDim(self, dim, change):
        if self.ndims - 1 < dim:
            print "There are only", self.ndims, "dimensions (attempting to change dimension", str(dim+1) + ")"
            return
        else:
            # changing current position
            self.current[dim] += change
            if self.current[dim] < 0:
                self.current[dim] = 0
            elif self.current[dim] > len(self.dimvalues[dim]) - 1:
                self.current[dim] = len(self.dimvalues[dim]) - 1

        # generating current position's file name
        parts = self.filepattern.split('*')
        file = parts[0]
        for i in range(self.ndims):
            file += self.dimvalues[i][self.current[i]]
            file += parts[i+1]

        # displaying image
        try:
            image = Image.open(os.path.normpath(self.dir + os.sep + file))
            width, height = image.size
            self.canvasImage = ImageTk.PhotoImage(image)
            self.canvas.itemconfig(self.ci, image = self.canvasImage)
            self.canvas.config(width = width, height = height)
        except:
            print "Error for position", file

        # updating info label
        current = "Current position: (" + str(self.current[0])
        for d in range(1, self.ndims):
            current += "," + str(self.current[d])
        current += ") = (" + self.dimvalues[0][self.current[0]]
        for d in range(1, self.ndims):
            current += "," + self.dimvalues[d][self.current[d]]
        current += ")"
        self.infoLabel.config(text = self.info + current)

        self.root.title(file)


if __name__ == "__main__":
    mdib()