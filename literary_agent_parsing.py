#!/bin/python

import argparse

def cleanup(line):
    line = line.strip()
    line = line.replace('  ', ' ')
    line = line.replace('&nbsp;', ' ')
    line = line.replace('&amp;', '&')
    return line

if __name__ == '__main__':
    # Parse the prgram arguments
    parser = argparse.ArgumentParser(('Parses the text file containing newline separated agent, agency, represented '
                                      'genres, and represented authors'))
    parser.add_argument('--input-file', help='The input text file')
    args = parser.parse_args()

    # Read the input file
    with open(args.input_file) as f:
        # Cleanup each line
        lines = [cleanup(line) for line in f.readlines()]


    # Maps authors to agents
    author_mapping = {}

    # Reads the input file lines to extract authors, genres, agencies, and agents
    while lines:
        authors = lines.pop()
        genres = lines.pop()
        agency = lines.pop().replace(',', '')
        agent = lines.pop()

        # Parse the authors
        for author in authors.split(', '):
            if author not in author_mapping:
                author_mapping[author] = []
            author_mapping[author].append((agent, agency))

    for author in author_mapping:
        for agent, agency in author_mapping[author]:
            print('{},{},{}'.format(author, agent, agency))

