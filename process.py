#!/usr/bin/env python3

delineator = "//"
hashtag = "#"

# generate poems from a file
# out: list of poem lines
def generate_poems(filename):
    g = []
    # get to the first poem in the file
    with open(filename, 'rb') as f:
        for line in f:
            if line.startswith( delineator ) and g:
                yield g
                g = []
            g.append(line)
        yield g
