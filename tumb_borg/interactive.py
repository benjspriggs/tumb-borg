#!/usr/bin/python

def print_poem(poem):
    print('Title: \t%s' % poem['title'])
    print('Tags:\t%s' % ", ".join(poem['tags']))

def print_poem_full(poem):
    print_poem_info(poem)
    print('Body:\r%s' % "\n".join(poem['content']))

