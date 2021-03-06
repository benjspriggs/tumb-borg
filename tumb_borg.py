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
    c = config.app_config(setting) # load auth settings

    def get_batch_tags():
        try:
            return c['batch-tags']
        except KeyError:
            return ""
    # returns if the keys exist in the config dictionary
    def config_has_stored_tokens():
        return 'oauth_token' in c and 'oauth_token_secret' in c
    def authorize_from_config():
        def renew_tokens():
            a = authorize.authorize(c['key'], c['secret'], c['callback'])
            a_t = authorize.authorized_t(c['key'], c['secret'], a)
            c['oauth_token'] = a_t.oauth_token
            c['oauth_token_secret'] = a_t.oauth_token_secret
            return a_t
        # attempt to authorize from config
        if config_has_stored_tokens():
            auth_t = authorize.authorized_t(c['key'], \
                    c['secret'], \
                    c)
            # now to validate the tokens
            if not authorize.has_valid_tokens(auth_t, blogname): # check
                # renew the tokens
                return renew_tokens()
            else:
                # nothing needs to be renewed
                return auth_t
        else:
            return renew_tokens()

    setting = os.path.realpath(setting)
    auth    = authorize_from_config()
    batch   = get_batch_tags()
    config.store(c, setting)
    if not authorize.has_posting_permissions(auth, blogname):
        raise Exception( \
                "The currently authorized user does not have permission to post to the blog: '%s'" \
                % blogname)

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
                    'body':  '<br/>\n'.join(payload['content']),
                    'title': '// %s' % payload['title'] }
        for poem in (queue_text_post(p) for p in poem_generator):
            interactive.print_poem(poem)
            print(auth.post('post', blog_url=ident, \
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
