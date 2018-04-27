"""Definition of the CLI.

"""

import os
import argparse


def parse_args(description:str, args:iter=None) -> dict:
    return cli_parser(description).parse_args(args)

def existant_file(filepath:str) -> str:
    """Argparse type, raising an error if given file does not exists"""
    if not os.path.exists(filepath):
        raise argparse.ArgumentTypeError("file {} doesn't exists".format(filepath))
    return filepath

def writable_file(filepath:str) -> str:
    """Argparse type, raising an error if given file is not writable.
    Will delete the file !

    """
    try:
        with open(filepath, 'a') as fd:
            pass
        os.remove(filepath)
        return filepath
    except (PermissionError, IOError):
        raise argparse.ArgumentTypeError("file {} is not writable.".format(filepath))


def cli_parser(description:str) -> argparse.ArgumentParser:
    # main parser
    parser = argparse.ArgumentParser(description=description.strip())

    parser.add_argument('infile', type=existant_file,
                        help="Name of the input file to compress")
    parser.add_argument('--outfile', '-o', type=writable_file, default='out.bbl',
                        help="Name of the bubble file to produce")


    return parser
