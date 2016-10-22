import argparse
import logging
import os
import sys

from intuitionistic_fuzzy_set import *
from ifs_plot import *
from ifs_3Dplot import *
  

def main():

    universe = UniversalSet(set(range(500)))

    ifs01 = IFS.random(universe, 1, randseed=2)

#     plot_ifs(ifs01, typ="interval_valued")
#     plot_stack(ifs01)
#     plot_bar_intValued(ifs01)
#     plot_bar_Intuitionistic(ifs01)
#     plot_together_intValued(ifs01)
#     plot_together_Intuitionistic(ifs01)
    plot_triangular(ifs01, bins=19)
    test_legend()

#    plot_triangular_with_arrows(ifs01)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
#   
    plot_membership_3Dhistogram(ifs01,ax, bins=10, typs=['mu','nu'])
#      
#     plot_3D_histogramm(ifs01, bins=10)
    plt.show()
    a = 10
    # args = parse_arguments()
    #
    # logging.basicConfig(level=getattr(logging, args.log[0].upper()))
    # logging.info('Files matching script starting...')



    print("Inside...")

if __name__ == "__main__":
    main()

