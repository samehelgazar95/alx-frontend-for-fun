#!/usr/bin/python3
"""
TODO: Handle h, ul, ol, li, p together as they
    have space between them and the text,
    so splitting them can divide them into two parts
TODO: Handle ** b, __ em, [[]], (()) together as
    they don't have space between them and the text
"""
from sys import argv, stderr
from os import path


def parse_h(line):
    markD = {"#": "h1", "##": "h2", "###": "h3",
             "####": "h4", "#####": "h5", "######": "h6"}
    lineSplitted = line.split(' ')
    hashes = lineSplitted[0]
    tag = markD[hashes]
    buffer = line.replace(hashes, f'<{tag}>')
    buffer = buffer[:-1] + f'</{tag}>\n'
    return buffer


if __name__ == '__main__':
    if len(argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=stderr)
        exit(1)

    mdFile = argv[1]
    htmlFile = argv[2]
    htmlContent = ''

    if (not path.isfile(mdFile)):
        print(f'Missing {mdFile}', file=stderr)
        exit(1)

    with open(mdFile, 'r') as readme:
        lines = readme.readlines()
        in_ul = in_ol = in_para = False

        for i, line in enumerate(lines):
            # Handling Headings
            if line.startswith('#'):
                htmlContent += parse_h(line)

            # Handling Unordered List
            elif line.startswith('-'):
                if not in_ul:
                    in_ul = True
                    htmlContent += '<ul>\n'
                htmlContent += f'<li>{line[1:].strip()}</li>\n'
                if i < len(lines) - 1 and not lines[i + 1][0].startswith('-'):
                    htmlContent += '</ul>\n'
                    in_ul = False

            # Handling Ordered List
            elif line.startswith('*'):
                if not in_ol:
                    in_ol = True
                    htmlContent += '<ol>\n'
                htmlContent += f'<li>{line[1:].strip()}</li>\n'
                if i < len(lines) - 1 and not lines[i + 1][0].startswith('*'):
                    htmlContent += '</ol>\n'
                    in_ol = False

            # Empty line
            elif line == '' or line == '\n':
                pass

            # Handling Para and br
            elif line:
                if in_para is False:
                    in_para = True
                    htmlContent += '<p>\n'

                htmlContent += f'{line}'
                if (i < len(lines) - 1 and (lines[i + 1][0] == '\n' or
                                            lines[i + 1][0].startswith((
                                                '#', '-', '*')))):
                    in_para = False
                    htmlContent += f'</p>\n'
                elif (i < len(lines) - 1 and
                        not lines[i + 1][0].startswith(('#', '-', '*'))):
                    htmlContent += f'<br/>\n'

        # Handling the EOF > End Of File
        if in_ul or in_ol:
            htmlContent += '</ul>\n' if in_ul else '</ol>\n'
            in_ul = in_ol = False
        if in_para is True:
            in_para = False
            htmlContent += '</p>\n'

    with open(htmlFile, 'w') as html:
        html.write(htmlContent)

    exit(0)
