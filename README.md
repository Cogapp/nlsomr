# nlsomr
National Library of Scotland Optical Music Recognition

tristan to check with NLS

check software licences



Optical musical recognition powered by https://github.com/audiveris n.b installation, required jdk8 did not work with jdk9.

Outputs in musicXml format.

Source data: http://digital.nls.uk/special-collections-of-printed-music/

images require minium 10px between staff lines. This requires upscaling source images x2, which will be accompished by imagemagick.



### Getting Started.
* install imagemagik
* install python3
* pip3 install bs4
* pip3 install elasticsearch
* pip3 install certifi
* pip3 install xmljson
* pip3 install lxml
* install MuseScore (https://musescore.org/en/download)
* git clone https://github.com/audiveris
* update working paths at the top of processor/processor.py
* cd retriever
* python3 get_images.py
* cd processor
* python3 processor.py
* n.b files already existing will not be processed so before running remove from xml\_out to force mxl reprocessing and remove from wav folder to force recreation of wav files 
* cd indexer
* cd searchkit
* npm install
* npm start
* visit localhost:3000 in browser




all items
download mxml link
search on
* title/text extraction
* note sequence

multi-part items index as seperate things linking to single item

output as midi?

find bigger thumbnails

make info page like examples on labs.cogapp.com

move xml_out to searchkit/public/mxml


split lines by octive to extract

replace full extract with title, id of parent. lists of notes/split by octave


