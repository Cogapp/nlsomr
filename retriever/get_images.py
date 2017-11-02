from bs4 import BeautifulSoup
import urllib.request
import os
import sys

"""gets images from the NLS site, and saves them to /images/"""

BASE_URL = 'http://digital.nls.uk/special-collections-of-printed-music/archive/'

book_id = '91386487'


#scan html for "pages" select input and step through options to retrieve urls of individual pages
def get_pages_for_book(book_id):
    book_url = "%s%s" % (BASE_URL, book_id)
    print("retrieving book %s" % book_url, file=sys.stderr)
    response = urllib.request.urlopen(book_url)
    data = response.read()  # a `bytes` object
    html_page = data.decode('utf-8')
    soup = BeautifulSoup(html_page, "html.parser")
    for select in soup.findAll('select', id='page_url'):
        for option in select.findAll('option',{"value":True}):
            url = option['value']
            page_id = url.split('/')[-1]
            get_image_for_page(book_id, page_id)

def get_image_for_page(book_id, page_id):
    page_url = "%s%s" % (BASE_URL, page_id)
    print("retrieving page %s" % page_url, file=sys.stderr)
    response = urllib.request.urlopen(page_url)
    data = response.read()  # a `bytes` object
    html_page = data.decode('utf-8')
    soup = BeautifulSoup(html_page, "html.parser")
    for div in soup.findAll('div', id='image_area'):
        for img in div.findAll('img', id='main_image'):
            small_img = str(img['src'])
            large_img = small_img.replace('dcn3/', 'dcn30/')
            large_img = large_img.replace('3.jpg', '30.jpg')
            print("found large image %s" % large_img, file=sys.stderr)

            # create large directory if necessary
            directory = '../images/%s' % book_id
            if not os.path.exists(directory):
                os.makedirs(directory)
            # write image
            file_name = '../images/%s/%s.jpg' % (book_id, page_id)
            with urllib.request.urlopen(large_img) as response, open(file_name, 'wb') as out_file:
                data = response.read() # a `bytes` object
                out_file.write(data)

            thumb_img = small_img.replace('dcn3/', 'dcn4/')
            thumb_img = thumb_img.replace('3.jpg', '4.jpg')

            # create thumb directory if necessary
            directory = '../searchkit/public/images/%s' % book_id
            if not os.path.exists(directory):
                os.makedirs(directory)
            # write image
            file_name = '../searchkit/public/images/%s/%s.jpg' % (book_id, page_id)
            with urllib.request.urlopen(thumb_img) as response, open(file_name, 'wb') as out_file:
                data = response.read()  # a `bytes` object
                out_file.write(data)

if __name__ == '__main__':
    #get_image_for_page(book_id, book_id)
    get_pages_for_book(book_id)