from urllib.parse import urlparse
from pprint import pprint
from link import Link
import re


class MarkdownFile:
    def __init__(self, path, debug):
        self.path = path                             # assumed to be relative
        self.links = self.find_links(path, debug)    # a list of Link objects


    def find_links(self, path, debug):
        """Takes the filepath of markdown file and returns a list
        of Link objects. This function will need to change
        a lot in the future to deal with line and column info."""
        try:
            text = open(path).read()
        except Exception as e:
            print(e) ; exit(1)

        urls = self.parse_out_urls(text, debug)

        # filter out all invalid urls
        urls = list(filter(lambda url: urlparse(url).scheme != '', urls))
        # remove duplicate urls
        urls = list(dict.fromkeys(urls))

        link_objs = list(map(lambda url: Link(url), urls))

        if debug:
            print('~~~~~~~~~~~~~~~ FOR DEBUGGING ~~~~~~~~~~~~~~~')
            print('file =', path)
            print('link count is', len(link_objs))
            for i in range(len(link_objs)):
                print(link_objs[i])
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', end='\n\n')

        return link_objs


    # maybe put all ths code in "find_links"?
    def parse_out_urls(self, text, debug):
        # adapted from https://stackoverflow.com/questions/6718633/python-regular-expression-again-match-url
        regex = r'((https?):((//)|(\\\\))+([\w\d:#@%/;$~_?\+-=\\\.&](#!)?)*)'
        urls = [tup[0] for tup in re.findall(regex, text)]
        if debug:
            print('~~~~~~~~~~~~~~~ After parsing ~~~~~~~~~~~~~~~')
            pprint(urls)
            print('\t\tlen(urls) is', len(urls))
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', end='\n\n')
        return urls


    def print_results(self):
        if not self.links:
            print('No links found')
            return

        print(f"<> Checking links in {self.path}")
        print(f"   {len(self.links)} unique link{'s' if len(self.links) != 1 else ''} found")

        # note: currently for large files the program stalls here
        print('   Doing networking stuff...\n')
        for l in self.links:
            l.find_status()

        alive_links = [] ; dead_links = []
        for l in self.links:
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

        return


    def __str__(self):
        pass
