#!/usr/bin/python

import yaml

def read_yaml(filename, readf=yaml.load):
    with open(filename, 'r') as f:
        return readf(f)
    
def config(filename='app.secret.yml'):
    return read_yaml(filename)

