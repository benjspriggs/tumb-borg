#!/usr/bin/python

import sys, os
from tumb_borg import *
from pprint import pprint

BATCH = "poem, poetry, spilled ink"

def authorize_from_config(filename):
    c = config.app_config(filename)
    return authorize.authorize(c['key'], c['secret'], c['callback'])

def get_batch(filename):
    c = config.app_config(filename)
    return c['batch-tags']

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

def poem_dicts(filename):
    return (process.to_dictionary(poem) \
            for poem \
            in process.generate_poems(filename))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('./tumb_borg <blogname> <filename> [<config-filename>]')
        sys.exit(1)
    print('Found the following poems:')
    for poem in poem_dicts( \
            os.path.realpath(sys.argv[2])):
        interactive.print_poem(poem)

    blogname = sys.argv[1]
    filename = sys.argv[2]
    setting  = None

    # authorize
    if len(sys.argv) >= 4:
        setting = sys.argv[3]
    else:
        setting = 'app.secret.yml'

    batch = get_batch(os.path.realpath(setting))
    auth  = authorize_from_config( \
            os.path.realpath(setting))
    # store the key for now TODO: implement
    # store(app_config())
    # check that the user can post to this blog TODO: implement
    # post poems
    post_poems(auth, \
            blogname, \
            poem_dicts(filename), \
            batch
            )
    print('Finished!')
