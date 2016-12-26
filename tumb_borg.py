#!/usr/bin/python

import sys, os
from lib import *
from pprint import pprint

def authorize_from_config(filename):
    c = config.app_config(filename)
    return authorize.authorize(c['key'], c['secret'], c['callback'])

def usage():
    print('usage: ./tumb_borg.py <blogname> <filename> [<config-filename>]')
    print('to see what would be posted: ./tumb_borg.py <filenames>')
    sys.exit(1)

def validate_arguments(argv):
    if len(argv) < 3 \
    and not os.path.exists(argv[1]):
        usage()

# generator for poems from a filename
def poems_from_file(filename):
    return (process.to_dictionary(poem) \
            for poem \
            in process.generate_poems(filename))

# ./tumb_borg.py <blogname> <filename> [<config-filename>]
def batch_post_poems(blogname, filename, setting):
    def get_batch_tags(filename):
        c = config.app_config(filename)
        return c['batch-tags']

    batch = get_batch_tags(os.path.realpath(setting))
    auth  = authorize_from_config( \
            os.path.realpath(setting))
    # store the key for now TODO: implement
    # store(app_config())
    # check that the user can post to this blog TODO: implement
    # post poems
    def post_poems(auth,    \
            ident,          \
            poem_generator, \
            BATCH="poem, poetry, spilled ink"):
        def queue_text_post(payload):
            return { 'type': 'text',
                    'state': 'queue',
                    'tags':  ', '.join(payload['tags']) + ", " + BATCH,
                    'body':  '\n'.join(payload['content']),
                    'title': '// %s' % payload['title'] }
        for poem in (queue_text_post(p) for p in poem_generator):
            print(poem)
            print(auth.post('blog/%s/post' % ident, \
                    params=poem))
    post_poems(auth, \
            blogname, \
            poems_from_file(filename), \
            batch
            )


if __name__ == "__main__":
    validate_arguments(sys.argv)

    if len(sys.argv) < 3:
        print('Found the following poems:')
        for poem in poems_from_file( \
                os.path.realpath(sys.argv[1])):
            interactive.print_poem_full(poem)
    else:
        # ./tumb_borg.py <blogname> <filename> [<settings-file>]
        if len(sys.argv) < 4:
            settings = 'app.secret.yml'
        else:
            settings = sys.argv[3]
        batch_post_poems(sys.argv[1], sys.argv[2], settings)

    print('Finished!')
