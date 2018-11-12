"""PowerGrASP package.

"""

from . import cli
from .routines import compress_by_cc
from .constants import print_config


def run_cli():
    args = cli.parse_args(__doc__)

    if args.show_config:
        print_config()
        exit()
    elif args.infile:
        with open(args.outfile, 'w') as fd:
            for line in compress_by_cc(args.infile, args.recipe):
                fd.write(line + '\n')
    else:
        print('Nothing to do.')


if __name__ == "__main__":
    run_cli()
