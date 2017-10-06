import os
from os import listdir
import sys

audiveris_cli_path = "/Users/stephenn/Documents/workspace/audiveris/build/distributions/Audiveris/bin/"
mscore_path = "/Applications/MuseScore\ 2.app/Contents/MacOS/" 

baseFolder = "/Users/stephenn/Documents/workspace/nlsomr/"
inputFolder = baseFolder+"images/"
outputFolder = baseFolder+"xml_out/"
workingFolder = baseFolder+"working/"
wavFolder = baseFolder+"searchkit/public/wavs/"


if __name__ == '__main__':
    #scan input dir
    #just assuming folder format of books as top level subdirs containing individual pages as images 
    for book in listdir(inputFolder):
        print "BOOK:"+book
        if not os.path.isfile(inputFolder + book):
            for inputfile in listdir(inputFolder + book):
                if os.path.isfile(inputFolder+book+"/"+inputfile) and (inputfile != ".DS_Store"):
                    print "file:"+inputfile
                    #upscale image with imagemagick
                    if not os.path.isfile(workingFolder + inputfile): #hacky method of skipping files we have alreay processed
                        os.system("convert %s%s/%s   -resize 200%%  %s%s > /dev/null" % (inputFolder,book,inputfile, workingFolder, inputfile))
                        os.system("%saudiveris -batch -export -output \"%s%s\" -- \"%s%s\" > /dev/null" % (audiveris_cli_path, outputFolder, book, workingFolder, inputfile))
                    for outputItem in listdir(outputFolder + book +"/"+ os.path.splitext(inputfile)[0]):
                        print outputItem+": "+ os.path.splitext(outputItem)[1]
                        if os.path.splitext(outputItem)[1] == ".mxl": #there may be multiple mxl files generated so we skip
                            print "DEBUG"
                            os.system("unzip -o -d %s%s/%s/%s_extract %s%s/%s/%s" % (outputFolder, book, os.path.splitext(inputfile)[0],os.path.splitext(outputItem)[0], outputFolder, book, os.path.splitext(inputfile)[0],outputItem))
                            for extractFile in listdir(outputFolder + book +"/"+ os.path.splitext(inputfile)[0]+"/"+os.path.splitext(outputItem)[0]+"_extract"):
                                if os.path.splitext(extractFile)[1] == ".xml":
                                    os.system("%smscore %s%s/%s/%s_extract/%s -o %s$s.wav" (mscore_path, outputFolder, book, os.path.splitext(inputfile)[0],os.path.splitext(outputItem)[0],extractFile, wavFolder, os.path.splitext(extractFile)[0]))