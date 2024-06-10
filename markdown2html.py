#!/usr/bin/python3
from sys import argv, stderr
from os import path


def parseLine(line):
    if line.startswith('#'):
        count = 0
        buffer = ''
        
        for ch in line:
            if ch == '#':
                count = count + 1
            else:
                buffer = buffer + ch

        match count:
            case 1:
                return(f'<h1>{buffer}</h1>')
            case 2:
                return(f'<h2>{buffer}</h2>')
            case 3:
                return(f'<h3>{buffer}</h3>')
            case 4:
                return(f'<h4>{buffer}</h4>')
            case 5:
                return(f'<h5>{buffer}</h5>')
            case 6:
                return(f'<h6>{buffer}</h6>')


if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage: ./markdown2html.py README.md README.html', file=stderr)
        exit(1)
        
    mdFile = argv[1]
    htmlFile = argv[2]
    htmlContent = ''

    if (not path.isfile(mdFile)):
        print('Missing <filename>')
        exit(1)

    with open(mdFile, 'r') as readme:
        lines = readme.readlines()
        for line in lines:
            htmlContent = htmlContent + parseLine(line)
            
    print(htmlContent)
    
    with open(htmlFile, 'w') as html:
        pass

    exit(0)
