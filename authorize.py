#!/usr/bin/python3
from tumblpy import Tumblpy as T

def authorize(KEY, SECRET, CALLBACK):
    # out : (authorization url, oauth secret)
    def get_authorization_properties():
        t = T(KEY, SECRET)
        return t.get_authentication_tokens(callback_url=CALLBACK)

    auth_p = get_authorization_properties()

    def authorized_tokens():
        t = T(KEY, SECRET,
                auth_p['oauth_token'],
                auth_p['oauth_token_secret'])
        return t.get_authorized_tokens(auth_p['oauth_verifier'])

    def authorized_t():
        a = authorized_tokens()
        return T(KEY, SECRET, 
                a['oauth_token'], 
                a['oauth_token_secret'])

    return authorized_t()
