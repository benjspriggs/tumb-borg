#!/usr/bin/python

import sys
from tumb_borg import *
from pprint import pprint

BATCH = "poem, poetry, spilled ink"

def authorize_from_config(filename):
    c = app_config(filename)
    return authorize(c['key'], c['secret'], c['callback'])


def post_poems(auth, ident, poem_generator):
    def queue_text_post(payload):
        return { 'type': 'text',
                'state': 'queue',
                'tags': ', '.join(payload['tags']) + ", " + BATCH,
                'body': '\n'.join(payload['content']),
                'title': '// %s' % payload['title'] }
    for poem in (queue_text_post(p) for p in poem_generator):
        print(poem)
        print(auth.post('blog/%s/post' % ident, \
            params=poem))

def poem_dicts(filename):
    return (to_dictionary(poem) for poem in generate_poems(filename))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('./tumb_borg <blogname> <filename>')
        sys.exit(1)
    # authorize
    print('Found the following poems:')
    for poem in poem_dicts(sys.argv[2]):
        print_poem(poem)
    auth = authorize_from_config('app.secret.yml')
    # store the key for now TODO: implement
    # store(app_config())
    # check that the user can post to this blog TODO: implement
    post_poems(auth, \
            sys.argv[1], \
            poem_dicts(sys.argv[2]))
    print('Finished!')
