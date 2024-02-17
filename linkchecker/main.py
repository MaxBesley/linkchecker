from link import Link
from cli import *
import sys
import markdown
import re
from pprint import pprint
from urllib.parse import urlparse
from textwrap import *

# Globals
TESTING = True


# from https://github.com/andrewp-as-is/markdown-link-extractor.py
# will change in the future since I thinks it's wasteful to convert to html
def parse_out_urls(string):
    """Return a list with markdown links"""
    html = markdown.markdown(string, output_format='html')
    links = list(set(re.findall(r'href=[\'"]?([^\'" >]+)', html)))
    links = list(filter(lambda l: l[0] != "{", links))
    return links

def get_links(filepath):
    """Takes the filepath of markdown file and returns a list
       of Link objects. This function will need to change
       a lot in the future to deal with line and column info."""
    try:
        text = open(filepath).read()
    except Exception as e:
        print(e)
        sys.exit(1)

    urls = parse_out_urls(text)

    # filter out all invalid urls
    urls = list(filter(lambda url: urlparse(url).scheme != "", urls))

    link_objs = list(map(lambda url: Link(url), urls))

    if TESTING:
        print("~~~~~~~~~~~~~~~ FOR TESTING ~~~~~~~~~~~~~~~")
        print(f"file = ", filepath)
        print("link count is", len(link_objs))
        for i in range(len(link_objs)): print(link_objs[i])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",end='\n\n')

    return link_objs


def main():
    cl_args = handle_args()

    links = get_links(cl_args.filepath)

    print(f"<> Checking links in {cl_args.filepath}")
    print(f"{len(links)} link{'s' if len(links) != 1 else ''} found")

    print("Doing networking stuff...")
    for l in links:
        l.find_status()

    alive_links = [] ; dead_links = []
    for l in links:
        if l.is_alive:
            alive_links.append(l)
        else:
            dead_links.append(l)

    if alive_links:
        print("Alive links:")
        for l in alive_links:
            print(f"- ({l.status}) {l.url}")

    if dead_links:
        print("Dead links:")
        for l in dead_links:
            print(f"- ({l.status}) {l.url}")


if __name__ == "__main__":
    main()
