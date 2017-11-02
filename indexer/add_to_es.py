import sys
import os
import re
#import json
from elasticsearch import Elasticsearch
from pprint import pprint
import certifi
import subprocess # Allows us to make many concurrent requests.
#from xmljson import badgerfish as bf - adds $s
from xmljson import abdera as bf
from json import dumps
from lxml import etree
from xml.etree.ElementTree import fromstring
from xml.etree.ElementTree import tostring
from io import StringIO, BytesIO
from copy import deepcopy
from os import listdir

es = Elasticsearch(["https://search-cogapp-x7o3xw2klqvyv7arrujtmzljpi.eu-west-1.es.amazonaws.com:443"])

BASE_XML_PATH = '../xml_out'

def document_from_xml(book_id,page_id):
    json_string = '';
    dirname = '{}/{}/{}'.format(BASE_XML_PATH, book_id, page_id)
    file_list = os.listdir(dirname)
    for f in file_list:
        if f[-8:] == '_extract':
            filename = '{}/{}/{}.xml'.format(dirname, f, f[:-8])

            #print(filename)
            #with open(filename, 'r') as myfile:
            #    print(myfile)
            #    xml_string = myfile.read()

            tree = etree.parse(filename)
            #print(etree.tostring(tree, pretty_print=True))

            page = etree.Element("page")
            id_node = etree.Element("page_id")
            id_node.text = page_id
            # add ID
            page.append(id_node)
            # add musicXML
            page.append(deepcopy(tree.getroot()))

            #print(etree.tostring(page, pretty_print=True))

            page_string = etree.tostring(page)


            json_string = dumps(bf.data(fromstring(page_string)))
            #print(json_string)
    return json_string

def insert_into_elasticsearch(book_id, id, json):
    doc_id = id
#    doc = {
#      'test': 'test',
#      'doc_id': 'doc_id',
#    }
    doc = json
    try:
        res = es.index(index="nls-omr", doc_type='page', id=doc_id, body=doc)
    except:
        res = {'_id' : id, 'result': 'failed'}
    print("ID: {} {}".format(res['_id'], res['result']))

# Request exception handler:
def except_handler(request, exception):
    print("Request failed : " + request.url)
    print(exception)
    pass


if __name__ == "__main__":
    for book in listdir(BASE_XML_PATH):
        print ("BOOK:"+book)
        if not os.path.isfile(BASE_XML_PATH +"/"+ book): #we have a directory
            for page in listdir(BASE_XML_PATH +"/"+ book):
                if not os.path.isfile(BASE_XML_PATH+"/"+book+"/"+page):
                    print ("PAGE:"+page)
                    json = document_from_xml(book, page)
                    if json != '':
                        insert_into_elasticsearch(book, page, json)
