#!/usr/bin/python

import yaml

def read_yaml(filename, readf=yaml.load):
    with open(filename, 'r') as f:
        return readf(f)
    
def config(filename='app.secret.yml'):
    def filtered_dict(d):
        return { key: d[key] for key in 
                ['key', 'secret', 'callback'] }
    return filtered_dict(read_yaml(filename))

