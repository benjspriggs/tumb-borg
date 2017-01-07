#!/usr/bin/python

import sys, yaml

def read_yaml(filename, readf=yaml.load):
    try:
        with open(filename, 'r') as f:
            return readf(f)
    except IOError:
        print("File '%s' not found." % filename)
        sys.exit(1)

def app_config(filename='app.secret.yml'):
    return read_yaml(filename)

def store(yaml_obj, filename):
    with open(filename, 'wb') as f:
        yaml.dump(yaml_obj, f, \
                default_flow_style=False,\
                explicit_start=True)

def user_config(filename='user.secret.yml'):
    return read_yaml(filename)

