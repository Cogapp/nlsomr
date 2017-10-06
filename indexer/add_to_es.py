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

es = Elasticsearch(["https://search-cogapp-x7o3xw2klqvyv7arrujtmzljpi.eu-west-1.es.amazonaws.com:443"])

BASE_XML_PATH = '../xml_out'

def document_from_xml(book_id,page_id):
    dirname = '{}/{}/{}'.format(BASE_XML_PATH, book_id, page_id)
    file_list = os.listdir(dirname)
    for f in file_list:
        if f[-8:] == '_extract':
            filename = '{}/{}/{}.xml'.format(dirname, f, page_id)

            print(filename)
            with open(filename, 'r') as myfile:
                print(myfile)
            #    xml_string = myfile.read()

    tree = etree.parse(filename)
    print(etree.tostring(tree, pretty_print=True))

    page = etree.Element("page")
    id_node = etree.Element("page_id")
    id_node.text = page_id
    # add ID
    page.append(id_node)
    # add musicXML
    page.append(deepcopy(tree.getroot()))

    print(etree.tostring(page, pretty_print=True))

    page_string = etree.tostring(page)


    json_string = dumps(bf.data(fromstring(page_string)))
    print(json_string)
    return json_string

def insert_into_elasticsearch(book_id, id, json):
    doc_id = id
#    doc = {
#      'test': 'test',
#      'doc_id': 'doc_id',
#    }
    doc = json
    res = es.index(index="nls-omr", doc_type='page', id=doc_id, body=doc)
    print("ID: {} {}".format(res['_id'], res['result']))

# Request exception handler:
def except_handler(request, exception):
    print("Request failed : " + request.url)
    print(exception)
    pass


if __name__ == "__main__":
    json = document_from_xml('91386487','91386636')
    insert_into_elasticsearch('91386487','91386636', json)