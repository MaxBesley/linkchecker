from argparse import ArgumentParser


def handle_args():
    parser = ArgumentParser(prog='linkchecker',
                            description='Checks links in markdown files',
                            epilog='this is the epilog')
    parser.add_argument('filepath', type=str, help='Relative path to .md file')
    # parser.add_argument('')
    return parser.parse_args()
