import os
from os import listdir
import sys

audiveris_cli_path = "/Users/stephenn/Documents/workspace/audiveris/build/distributions/Audiveris/bin/"

baseFolder = "/Users/stephenn/Documents/workspace/nlsomr/"
inputFolder = baseFolder+"images/"
outputFolder = baseFolder+"xml_out/"
workingFolder = baseFolder+"working/"


if __name__ == '__main__':
    #scan input dir

    #recursive(or at least 2 stage ) loop
    #just assuming folder format of books as top level subdirs containing individual pages as images 
    for book in listdir(inputFolder):
        print "BOOK:"+book
        if not os.path.isfile(inputFolder + book):
            for inputfile in listdir(inputFolder + book):
                print "file:"+inputfile
                #upscale image with imagemagick
                os.system("convert %s%s/%s   -resize 200%%  %s%s" % (inputFolder,book,inputfile, workingFolder, inputfile))
                os.system("%saudiveris -batch -export -output \"%s%s\" -- \"%s%s\"" % (audiveris_cli_path, outputFolder, book, workingFolder, inputfile))
