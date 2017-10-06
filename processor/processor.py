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
    #just assuming folder format of books as top level subdirs containing individual pages as images 
    for book in listdir(inputFolder):
        print "BOOK:"+book
        if not os.path.isfile(inputFolder + book):
            for inputfile in listdir(inputFolder + book):
                if os.path.isfile(inputFolder+book+"/"+inputfile) and inputfile != ".DS_Store"
                    print "file:"+inputfile
                    #upscale image with imagemagick
                    if not os.path.isfile(inputFolder + book): #hacky method of skipping files we have alreay processed
                        os.system("convert %s%s/%s   -resize 200%%  %s%s > /dev/null" % (inputFolder,book,inputfile, workingFolder, inputfile))
                        os.system("%saudiveris -batch -export -output \"%s%s\" -- \"%s%s\" > /dev/null" % (audiveris_cli_path, outputFolder, book, workingFolder, inputfile))
                    for outputItem in listdir(outputFolder + book + os.path.splitext(inputfile)[0]):
                        if os.path.splitext(inputfile)[0] == "mxl": #there may be multiple mxl files generated so we skip
