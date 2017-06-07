# Multi-Dimensional-Image-Browser
Python script (Python 2.7, uses PIL and TKinter) to allow image browsing across multiple dimensions indicated in the images' file names.

![Screenshot](/mdib.png)

This has made the analysis of some visual data a little easier for me. Rather than browsing through image files in alphabetical order, this script allows them to be browsed through in a multi-dimensional fashion. Take for example the following files:

```
apple-brown.jpg     banana-brown.jpg      pear-brown.jpg
apple-green.jpg     banana-green.jpg      pear-green.jpg
apple-yellow.jpg    banana-yellow.jpg     pear-yellow.jpg
```

Regular alphabetical ordering would have you browse first through all apples, colour by colour, then through the bananas, colour by colour, and then the pears. These files, however, contain two dimensions: fruit type, and fruit colour. This script makes it possible to jump from the green banana to the green apple with one button, and from the green apple to the yellow apple with another.

Simply supply it with a directory and a file pattern, and the script automatically extracts and orders all dimension values. 

File names should be consistent except for the variable parts, and the variable parts should be separated somehow. A variable part of the file names representing one dimension is indicated using an asterisk (*). For the above example, the pattern would be

```
*-*.jpg
```

The script then allows you to browse through the available dimensions using the keyboard. The keys for the first dimension are under the "1", i.e. on a QWERTY keyboard, "q" for one up in this dimension, and "a" for one down. "w" and "e" increase and decrease the second dimension, respectively, and "o" and "l" represent the ninth dimension. The first two dimensions can additionally
be controlled by the arrow keys.

Dimensions are numbered in the order that they appear in the file names.

Keyboard shortcuts include shift+D to set the directory, and shift+P for the pattern. Enter applies, escape exits.
