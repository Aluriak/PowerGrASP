"""PowerGrASP package.

"""

from . import cli
from .routines import compress_by_cc


def run_cli():
    args = cli.parse_args(__doc__)

    with open(args.outfile, 'w') as fd:
        for line in compress_by_cc(args.infile):
            fd.write(line + '\n')


if __name__ == "__main__":
    run_cli()
