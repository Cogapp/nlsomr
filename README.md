# nlsomr
National Library of Scotland Optical Music Recognition

A hack day project by [Cogapp](http://www.cogapp.com), September 2017. Takes images of sheet music as input, converts to MusicXML and then WAV audio files, stores some metadata in ElasticSearch and displays the results using [Searchkit](https://github.com/searchkit/searchkit).

Demo version of results online at http://labs.cogapp.com/nls-omr

Optical musical recognition powered by [Audiveris](https://github.com/audiveris) n.b installation, required jdk8 did not work with jdk9. This outputs in musicXml format.

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
* git clone https://github.com/audiveris (requires JVM 8 to run)
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
* To create a production build, use npm run build.
* Upload to labs.cogapp.com
* access at http://labs.cogapp.com/nls-omr


# TODO

* don't index full MusicXML, just title, searchable text, id of parent. lists of notes/split by octave (to allow proper music search)
* output as midi?

