#!/usr/bin/python
from tumblpy import Tumblpy as T
try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

def authorize(KEY, SECRET, CALLBACK):
    def get_authorization_properties():
        t = T(KEY, SECRET)
        return t \
            .get_authentication_tokens(
                        callback_url=CALLBACK)

    auth_p = get_authorization_properties()

    def get_auth_url():
        print('Please connect with Tumblr via: \n%s' \
                % auth_p['auth_url'])
        result_url = \
            raw_input("Copy and paste the accepting url: ") 
        return result_url

    def query_string(url):
        return { k: v[0] for k, v in 
                parse_qs(urlparse(url).query).items() }

    def query_string_auth():
        return query_string(get_auth_url())

    def authorized_tokens():
        q = query_string_auth()
        t = T(KEY, SECRET,
                q['oauth_token'],
                auth_p['oauth_token_secret'])
        return t.get_authorized_tokens(q['oauth_verifier'])

    def authorized_t():
        a = authorized_tokens()
        return T(KEY, SECRET, 
                a['oauth_token'], 
                a['oauth_token_secret'])
  
    return authorized_t()
