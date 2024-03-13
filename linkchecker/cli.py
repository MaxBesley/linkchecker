from argparse import ArgumentParser


def handle_args():
    parser = ArgumentParser(prog='linkchecker',
                            description='Checks links in markdown files',
                            epilog='this is the epilog')
    parser.add_argument(
        'path', type=str, help='relative path to a .md file or a directory')
    parser.add_argument(
        '-r', '--recurse', action='store_true', help='')
    parser.add_argument(
        '--debug', action='store_true', help='print out debug information')
    return parser.parse_args()
