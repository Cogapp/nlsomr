import os
import sys

audiveris_cli_path = "/Users/stephenn/Documents/workspace/audiveris/build/distributions/Audiveris/bin/"

inputfolder = "/Users/stephenn/Documents/workspace/nlsomr/images/91386487/"
outputfolder = "/Users/stephenn/Documents/workspace/nlsomr/xml_out"

inputfile = "91386960.jpg"
workingfile = "%stmp.jpg" % (inputfolder)


if __name__ == '__main__':
    #scan input dir

    #recursive(or at least 2 stage ) loop

    #upscale image with imagemagick
    print workingfile 
    #print "convert %s%s" % (inputfolder, inputfile)
    os.system("convert %s%s   -resize 200%%  %s" % (inputfolder, inputfile, workingfile))

    #run omr
    os.system("%saudiveris -batch -export -output \"%s\" -- \"%s\"" % (audiveris_cli_path, outputfolder, workingfile))