#!/usr/bin/python3
from sys import argv, stderr
from os import path
"""
TODO: Handle h, ul, ol, li, p together as they are have space between them and the text,
    so splitting them can divide them into two parts
TODO: Handle ** b, __ em, [[]], (()) together as they don't have space between them and the text

# Heading level 1   <h1>Heading level 1</h1>
## Heading level 2  <h2>Heading level 1</h2>
### Heading level 3 <h3>Heading level 1</h3>

- Hello
- Bye
<ul>
    <li>Hello</li>
    <li>Bye</li>
</ul>

* Hello
* Bye
<ol>
    <li>Hello</li>
    <li>Bye</li>
</ol>

Hello

I'm a text
with 2 lines
<p>
    Hello
</p>
<p>
    I'm a text
        <br />
    with 2 lines
</p>
"""

def parse_h(line):
    count = 0
    buffer = ''
    for idx in range(len(line)):
        if line[idx] == '#':
            count = count + 1
        else:
            buffer = buffer + line[idx]

    buffer = buffer.strip()
    match count:
        case 1:
            buffer = f'<h1>{buffer}</h1>\n'
        case 2:
            buffer = f'<h2>{buffer}</h2>\n'
        case 3:
            buffer = f'<h3>{buffer}</h3>\n'
        case 4:
            buffer = f'<h4>{buffer}</h4>\n'
        case 5:
            buffer = f'<h5>{buffer}</h5>\n'
        case 6:
            buffer = f'<h6>{buffer}</h6>\n'
    return buffer

def parse_li(line):
    return f'<li>{line[1:].strip()}</li>\n'


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
        in_ul = in_ol = in_p = False

        for line in lines:
            if line.startswith('#'):
                if in_ul or in_ol:
                    htmlContent += '</ul>\n' if in_ul else '</ol>\n'
                    in_ul = in_ol = False
                    if in_p:
                        htmlContent += '</p>\n'
                        in_p = False
                htmlContent += parse_h(line)

            elif line.startswith('-'):  # ul
                if not in_ul:
                    in_ul = True
                    htmlContent += '<ul>\n'
                    if in_p:
                        htmlContent += '</p>\n'
                        in_p = False
                htmlContent += parse_li(line)
                
            elif line.startswith('*'):  # ol
                if not in_ol:
                    in_ol = True
                    htmlContent += '<ol>\n'
                    if in_p:
                        htmlContent += '</p>\n'
                        in_p = False
                htmlContent += parse_li(line)
                
            elif line == '':
                if in_ul or in_ol:
                    htmlContent += '</ul>\n' if in_ul else '</ol>\n'
                    in_ul = in_ol = False
                if in_p:
                    htmlContent += '</p>\n'
                    in_p = False
                    
            else:
                if in_ul or in_ol:
                    htmlContent += '</ul>\n' if in_ul else '</ol>\n'
                    in_ul = in_ol = False
                if not in_p:
                    in_p = True
                    htmlContent += f'<p>'
                htmlContent += f'{line}'
                # else:
                #     in_p = True
                #     htmlContent += f'<br/><p>{line}</p>'

            # Handling the EOF > End Of File
            if in_ul or in_ol:
                htmlContent += '</ul>\n' if in_ul else '</ol>\n'
                in_ul = in_ol = False              
            if in_p:
                htmlContent += '</p>\n'

    with open(htmlFile, 'w') as html:
        html.write(htmlContent)

    exit(0)
