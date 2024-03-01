from link import Link
from cli import *
import sys
import re
from pprint import pprint
from urllib.parse import urlparse
from textwrap import *


def parse_out_urls(text, debug):
    # adapted from https://stackoverflow.com/questions/6718633/python-regular-expression-again-match-url
    regex = r'((https?):((//)|(\\\\))+([\w\d:#@%/;$~_?\+-=\\\.&](#!)?)*)'
    urls = [tup[0] for tup in re.findall(regex, text)]
    if debug:
        print('~~~~~~~~~~~~~~~ After parsing ~~~~~~~~~~~~~~~')
        pprint(urls)
        print("\t\tlen(urls) is", len(urls))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', end='\n\n')
    return urls


def get_links(filepath, debug):
    """Takes the filepath of markdown file and returns a list
    of Link objects. This function will need to change
    a lot in the future to deal with line and column info."""
    try:
        text = open(filepath).read()
    except Exception as e:
        print(e)
        sys.exit(1)

    urls = parse_out_urls(text, debug)

    # filter out all invalid urls
    urls = list(filter(lambda url: urlparse(url).scheme != '', urls))
    # remove duplicate urls
    urls = list(dict.fromkeys(urls))

    link_objs = list(map(lambda url: Link(url), urls))

    if debug:
        print('~~~~~~~~~~~~~~~ FOR DEBUGGING ~~~~~~~~~~~~~~~')
        print('file =', filepath)
        print('link count is', len(link_objs))
        for i in range(len(link_objs)):
            print(link_objs[i])
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', end='\n\n')

    return link_objs


def main():
    cl_args = handle_args()
    filepath = cl_args.filepath
    debug = cl_args.debug

    links = get_links(filepath, debug)

    print(f"<> Checking links in {filepath}")
    print(f"   {len(links)} link{'s' if len(links) != 1 else ''} found")

    # note: currently for large files the program stalls here
    print('   Doing networking stuff...')
    for l in links:
        l.find_status()

    alive_links = [] ; dead_links = []
    for l in links:
        if l.is_alive:
            alive_links.append(l)
        else:
            dead_links.append(l)

    if alive_links:
        print('Alive links:')
        for l in alive_links:
            print(f"- ({l.status}) {l.url}")

    if dead_links:
        print('Dead links:')
        for l in dead_links:
            print(f"- ({l.status}) {l.url}")


if __name__ == '__main__':
    main()
