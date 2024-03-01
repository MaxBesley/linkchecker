import os
from sys import exit
from cli import handle_args
from markdown_file import MarkdownFile


def main():
    cl_args = handle_args()
    path = cl_args.path
    debug = cl_args.debug

    if os.path.isfile(path):
        md_file = MarkdownFile(path, debug)
        md_file.print_results()

    else:
        # not implemented
        print("It's a directory") ; exit(1)

    return


if __name__ == '__main__':
    main()
