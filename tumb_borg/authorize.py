#!/usr/bin/python
from tumblpy import Tumblpy as T
from builtins import input
try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

# obtain authorization token info from Tumblr
def authorize(KEY, SECRET, CALLBACK):
    # STEP 1: Obtain the authorization properties
    # Returns a dict containing the following keys:
    #   'auth_url'
    #   'oauth_token_secret'
    def get_authorization_properties():
        t = T(KEY, SECRET)
        return t \
            .get_authentication_tokens(
                        callback_url=CALLBACK)

    auth_p = get_authorization_properties()

    # STEP 2: Requesting Permission
    # Prompts the user to grant permission for
    # the app to access their account,
    # then returns the resulting url as a string
    def get_auth_url():
        print('Please connect with Tumblr via: \n%s' \
                % auth_p['auth_url'])
        result_url = \
            input("Copy and paste the accepting url: ") 
        return result_url

    # Returns the query string in a 
    # HTTP URL as a dict
    def query_string(url):
        return { k: v[0] for k, v in 
                parse_qs(urlparse(url).query).items() }

    # Returns the query string as a dict
    # from the resulting url of the user
    # granting or denying permission
    def query_string_auth():
        return query_string(get_auth_url())

    # STEP 3: Handling the Callback
    # Returns a dictionary of tokens authorized (or not)
    # by the user as a dictionary
    def authorized_tokens():
        q = query_string_auth()
        t = T(KEY, SECRET,
                q['oauth_token'],
                auth_p['oauth_token_secret'])
        return t.get_authorized_tokens(q['oauth_verifier'])

    return authorized_tokens()

# returns an authorized TumblPy instance
# :param: auth
#   Must contain the following keys:
#   'oauth_token'
#   'oauth_token_secret'
def authorized_t(KEY, SECRET, auth):
    return T(KEY, SECRET,
            auth['oauth_token'], 
            auth['oauth_token_secret'])
