#!/usr/bin/python3
from sys import argv, stderr
from os import path


if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage: ./markdown2html.py README.md README.html', file=stderr)
        exit(1)

    if (not path.isfile(argv[1])):
        print('Missing <filename>')
        exit(1)

    exit(0)
