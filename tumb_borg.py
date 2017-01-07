#!/usr/bin/python

import sys, os
from tumb_borg import *
from pprint import pprint

def usage():
    print('usage: ./tumb_borg.py <blogname> <filename> [<config-filename>]')
    print('To see what would be queued: ./tumb_borg.py <filenames>')
    sys.exit(1)

def validate_arguments(argv):
    try:
        if len(argv) < 3 \
        and (len (argv) is 1 \
            and not os.path.exists(argv[1])):
            usage()
    except Exception:
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
    c = config.app_config(setting)
    a = {}

    def get_batch_tags():
        return c['batch-tags']
    # returns if the keys exist in the config dictionary
    def config_has_stored_tokens():
        return 'oauth_token' in c and 'oauth_token_secret' in c
    def authorize_from_config():
        # attempt to authorize from config
        if config_has_stored_tokens():
            return authorize.authorized_t(c['key'], c['secret'], c)
        else:
            a = authorize.authorize(c['key'], c['secret'], c['callback'])
            return authorize.authorized_t(c['key'], c['secret'], a)

    setting = os.path.realpath(setting)
    batch   = get_batch_tags()
    auth    = authorize_from_config()

    if not config_has_stored_tokens():
        # store the key for now TODO: implement
        c['oauth_token'] = a['oauth_token']
        c['oauth_token_secret'] = a['oauth_token_secret']
        config.store(c, setting)
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
            print(auth.post('post'. blog_url=ident, \
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
        if len(sys.argv) < 4:
            settings = secret_path()
        else:
            settings = sys.argv[3]
        batch_post_poems(sys.argv[1], sys.argv[2], settings)


    print('Finished!')
