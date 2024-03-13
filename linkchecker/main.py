from os import listdir
from os.path import isfile, isdir, join
from sys import exit
from pprint import pprint
from cli import handle_args
from markdown_file import MarkdownFile


def main():
    cl_args = handle_args()
    path = cl_args.path
    recurse = cl_args.recurse
    debug = cl_args.debug

    # note: is "md_file" vs "md_files" confusing??
    if isfile(path):
        md_file = MarkdownFile(path, debug)
        md_file.print_results()

    elif isdir(path):
        print_folder_results(path, recurse, debug)

    else:
        exit(f"'{path}' is not a valid file/folder")

    return


# the control flow here needs more work
def print_folder_results(path, recurse, debug):
    md_filepaths = [join(path, f) for f in listdir(path) if f.endswith('.md')]
    md_files = [MarkdownFile(path, debug) for path in md_filepaths]

    if md_files:
        if recurse:
            print(f"Looking in `{path}` directory")
        for md_file in md_files:
            md_file.print_results()
            print('\n')

    if recurse:
        subfolders = [join(path, f) for f in listdir(path) if isdir(join(path, f))]
        for s in subfolders:
            print_folder_results(s, recurse, debug)

    return


if __name__ == '__main__':
    main()
