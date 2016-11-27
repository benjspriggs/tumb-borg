#!/usr/bin/env python3

import process

if __name__ == "__main__":
    print('Hello world!')
    for poem in process.generate_poems('test.txt'):
        print(poem)
