#!/usr/bin/env python3

from process import *

if __name__ == "__main__":
    print('Hello world!')
    for poem in map(to_dictionary, generate_poems('example.txt')):
        print('Title is %s'% poem['title'])
