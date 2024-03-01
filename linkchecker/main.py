import os
from sys import exit
from pprint import pprint
from cli import handle_args
from markdown_file import MarkdownFile


def main():
    cl_args = handle_args()
    path = cl_args.path
    debug = cl_args.debug

    # note: is "md_file" vs "md_files" confusing??
    if os.path.isfile(path):
        md_file = MarkdownFile(path, debug)
        md_file.print_results()

    elif os.path.isdir(path):
        md_filepaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.md')]

        md_files = list(map(lambda path: MarkdownFile(path, debug), md_filepaths))
        # for md_file in md_files:
        #     print(md_file)

        for md_file in md_files:
            md_file.print_results()
            print('\n')

    else:
        exit(f"'{path}' is not a valid file/folder")

    return


if __name__ == '__main__':
    main()
