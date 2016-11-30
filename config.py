#!/usr/bin/python

import yaml

def read_yaml(filename, readf=yaml.load):
    with open(filename, 'r') as f:
        return readf(f)
    
def app_config(filename='app.secret.yml'):
    return read_yaml(filename)

def store(yaml_obj, filename):
    with open(filename, 'wb') as f:
        yaml.dump(yaml_obj, f)

def user_config(filename='user.secret.yml'):
    return read_yaml(filename)

