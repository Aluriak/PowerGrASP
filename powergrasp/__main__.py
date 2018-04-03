"""PowerGrASP package.

"""

from . import cli
from .routines import compress_by_cc


if __name__ == "__main__":
    args = cli.parse_args(__doc__)

    with open(args.outfile, 'w') as fd:
        for line in compress_by_cc(args.infile):
            fd.write(line + '\n')

