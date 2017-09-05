#!/usr/bin/env python3
'''
    Cli utility for searching books from amazon.com
'''
from bs4 import BeautifulSoup
from pprint import pprint

import bottlenose
import os
import requests
import sys


def init():
    try:
        keys = ('AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_ASSOCIATE_TAG')
        aws_ids = {key: os.environ[key] for key in keys}
    except KeyError:
        print('You should set the environment variables for accessing Amazon')
        sys.exit(-1)

    amazon = bottlenose.Amazon(
        aws_ids['AWS_ACCESS_KEY_ID'],
        aws_ids['AWS_SECRET_ACCESS_KEY'],
        aws_ids['AWS_ASSOCIATE_TAG'],
        Parser=lambda text: BeautifulSoup(text, 'xml')
    )
    return amazon

def lookup(amazon, id):
    return amazon.ItemLookup(
        ItemId=id, ResponseGroup="Large",
        SearchIndex="Books", IdType="ISBN")

def get_item_data(result):
    reviews_url = result.find('IFrameURL').text
    reviews_page = requests.get(reviews_url).text

    reviews = BeautifulSoup(reviews_page, 'html.parser')
    attributes = result.find('ItemAttributes')

    item = {
        'title': attributes.find('Title').text,
        'author': attributes.find('Author').text,
        'publisher': attributes.find('Manufacturer').text,
        'release': attributes.find('ReleaseDate').text,
        'rating': reviews.find_all('img')[1]['title'].split()[0],
        'reviews': reviews.find('b').text.split()[0]
    }
    return item

def find(id=None):
    if id:
        client = init()
        result = lookup(client, id)
        item = get_item_data(result)
        pprint(item)


if __name__ == '__main__':
    find(sys.argv[1])
