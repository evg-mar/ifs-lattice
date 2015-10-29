import argparse
import logging
import os
import sys

from intuitionistic_fuzzy_set import *


def main():

    universe = UniversalSet(set(range(20)))

    ifs00 = IFS(universe, 30)
    ifs01 = IFS.random(universe, 30)



    a = 10
    # args = parse_arguments()
    #
    # logging.basicConfig(level=getattr(logging, args.log[0].upper()))
    # logging.info('Files matching script starting...')

    return

if __name__ == "__main__":
    main()
