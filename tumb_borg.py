#!/usr/bin/python

from process import *
from config import *
from authorize import *
from pprint import pprint

if __name__ == "__main__":
    print('Poems are:')
    for poem in map(to_dictionary, generate_poems('example.txt')):
        print('Title is %s'% poem['title'])
        print('Tags are %s'% poem['tags'])
        # pprint(config())
    # authorize
    c = config()
    auth = authorize(c['key'], c['secret'], c['callback'])
    pprint(auth.post('user/info'))
