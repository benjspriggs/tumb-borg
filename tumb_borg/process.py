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
            line = line.rstrip()
            if line.startswith( delineator ) and g:
                yield g
                g = []
            if line:
                g.append(line)
        yield g

# convert a list of strings
# into a poem dictionary
def to_dictionary(poem_lines):
    d = {}
    d['content'] = []
    d['tags'] = []
    tags = []
    for line in poem_lines:
        if line.startswith( delineator ):
            d['title'] = line.lstrip( delineator ).strip()
        elif line.startswith( hashtag ):
            tags.append(line)
        else:
            d['content'].append(line) # do not strip to preserve indentation
    for line in tags:
        for tag in \
            (t.strip() for t in line.split( hashtag ) if t):
            d['tags'].append(tag)
    return d
