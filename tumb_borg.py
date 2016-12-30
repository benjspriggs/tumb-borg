#!/usr/bin/python

import sys, os
from lib import *
from pprint import pprint

def usage():
    print('usage: ./tumb_borg.py <blogname> <filename> [<config-filename>]')
    print('to see what would be posted: ./tumb_borg.py <filenames>')
    sys.exit(1)

def validate_arguments(argv):
    if len(argv) < 3 \
    and (len (argv) is 1 \
        and not os.path.exists(argv[1])):
        usage()

# returns a generator for poems from a filename
def poems_from_file(filename):
    return (process.to_dictionary(poem) \
            for poem \
            in process.generate_poems(filename))


# ./tumb_borg.py <blogname> <filename> [<config-filename>]
# Post all poems contained in <filename>
# queued to <blogname>
# according to settings contained in optional <config-filename>
def batch_post_poems(blogname, filename, setting):
    def get_batch_tags(filename):
        c = config.app_config(filename)
        return c['batch-tags']
    def authorize_from_config(filename):
        c = config.app_config(filename)
        return authorize.authorize(c['key'], c['secret'], c['callback'])


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

# Helpfully display all of the poems
# that are contained in a file
def display_poems_in_file(filename):
    print('Found the following poems:')
    poems = poems_from_file(os.path.realpath(filename))
    for poem in poems:
        interactive.print_poem_full(poem)

if __name__ == "__main__":
    validate_arguments(sys.argv)

    def secret_path(secret_fn='app.secret.yml'):
        dirname = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dirname, secret_fn)

    if len(sys.argv) < 3:
        display_poems_in_file(sys.argv[1])
    else:
        # ./tumb_borg.py <blogname> <filename> [<settings-file>]
        if len(sys.argv) < 4: # TODO: Make this default argument-able
            settings = secret_path()
        else:
            settings = sys.argv[3]
        batch_post_poems(sys.argv[1], sys.argv[2], settings)

    print('Finished!')
