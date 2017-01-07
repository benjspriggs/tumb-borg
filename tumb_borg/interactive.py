#!/usr/bin/python

_POEM_FORMAT_STRING="// %s\n%s\n#%s\n\n"

def print_poem(poem):
    print('Title: \t%s' % poem['title'])
    print('Tags:\t%s' % poem['tags'])

def print_poem_full(poem):
    print_poem(poem)
    print('Body:\r%s' % "\n".join(poem['content']))

def save_poems(filename, poems):
    with open(filename, 'w') as f:
        def save_poem(of, poems):
            of.write( _POEM_FORMAT_STRING % \
                    (poem['title'], \
                    "\n".join(poem['content']), \
                    " #".join(poem['tags']))
                    )

        for poem in poems:
            save_poem(f, poem)
