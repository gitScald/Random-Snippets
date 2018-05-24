import argparse

HEADER = '''<!DOCTYPE html>

<html lang="en">

<head>
    <meta charset="UTF-8"/>
    <title>{0}</title>
    <style>
        p {{
            margin: 0px;
            padding: 0px;
        }}
    </style>
</head>

<body>
    <form action="">'''

FOOTER = '''</body>

</html>
'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BFF file editor')
    parser.add_argument('file', help='File to edit')

    args = parser.parse_args()

    if len(args.file) < 5 or args.file[-3:] != 'bff':
        raise RuntimeError('Invalid file')

    content = []
    with open(args.file, 'r') as file:
        content = file.readlines()

    line_index = 0
    section_id = 0
    sections = []
    for line in content:
        if line[0:3] == '// ':
            section_title = line[3:].strip('\r').strip('\n')
            sections.append(section_title)
            content[line_index] = '<p id="section{0}">{1}</p>'.format(section_id, sections[section_id])
            section_id = section_id + 1
        else:
            content[line_index] = '<p>{0}</p>'.format(line.strip('\r').strip('\n'))
        line_index = line_index + 1

    with open(args.file + ".html", 'w') as file:
        file.write(HEADER.format(args.file))
        for section_id in range(0, len(sections)):
            file.write('\n        <a href="#section{0}">{1}</a>'.format(section_id, sections[section_id]))
        file.write('\n    </form>\n')
        for line in content:
            file.write('            ' + line + '\n')
        file.write(FOOTER)
