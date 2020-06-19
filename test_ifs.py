from intuitionistic_fuzzy_set import IFS
from universal_set import UniversalSet
# import numpy as np
from ifs_lattice import piOrd, stdOrd
from ifs_2Dplot import *
from ifs_3Dplot import *
  


from collections import OrderedDict

from openpyxl import load_workbook
import os
import sys

import argparse


parser = argparse.ArgumentParser(
    description='Plot IFS representations'
)


# parser.add_argument('-input_file', action="store",
#                     type=str,
#                     help = 'Input file name')
# parser.add_argument('-sheet', action="store",
#                     type=str,
#                     help = 'Name of the sheet in the file')
# parser.add_argument('-format', action="store",
#                     type=str,
#                     help = 'Format of input file: row or matrix')
# parser.add_argument('-start', action="store",
#                     dest="start", type=int)
# parser.add_argument('-end', action="store",
#                     dest="end", type=int)
# parser.add_argument('--number_bins', action="store", default=15,
#                     dest="number_bins", type=int)
parser.add_argument('-plot', action='append',
                    #dest='collection',
                    default=[],
                    help='What to plot: 2dHistogram, 2dHistogram, stackbars')


#
#evgeniy@evgeniy-TravelMate-P238-M:~$ python -input_file file_name -format 'row' 
#-step_size 20  start 2 end 560 3dHistogram triangular stackbars 



main_path = "/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/"
main_path = os.getcwd()
import os
main_path = os.getcwd() + '/ifsholder/'
file_name = "Mutr_ICA_Evgeni.xlsx"
file_name ="SecondOrderICA_mutr_Dafi.xlsx"

wb = load_workbook(filename=main_path + file_name, read_only=True)


ws = wb["GASeries_00030_MuNu"]


start = 1
end = 561


def get_pair(str_pair):
    lst = str_pair.strip(')(').split(',')
    mu = lst[0].strip()
    nu = lst[1].strip()
    return float(mu), float(nu)
    
rows = list(ws.rows)    
result = OrderedDict([(row[0].value, get_pair(row[1].value)) for row in rows[start:end]])


for k, (v1,v2) in result.items():
    print(v1+v2)
    assert(v1+v2 <= 1.0001)

def main():

    args = sys.argv[1:]

    arguments = [ ]
    for arg in args:
        print(arg)
        arguments.append( args.strip() )

    ######################################
    universe = UniversalSet(result.keys())
    
    ifsG = IFS(universe, 1)
    
    for k, value in result.items():
        ifsG.set_bykey(k, value)

    ifs01 = ifsG
    
    ####################################
    ####################################   


    if 'type_2' in arguments:
        # plot_ifs(ifs01, typ="interval_valued")

        # plot_stack(ifs01)
        plot_bar_type_2(ifs01)
        #
        # plot_together_intValued(ifs01)
    
    plotbar = True
    if 'type_1' in arguments:
        plot_bar_type_1(ifs01)
        # plot_together_Intuitionistic(ifs01)
  
    indices, mus, nus, pis = ifs01.elements_split()

    
    triangular = True
    if 'triangular' in arguments:
        plot_triangular(mus, nus, ifs01.get_range(), bins=20)

#     test_legend()


#    plot_triangular_with_arrows(ifs01)

    plot3D_membership = True
    if 'plot3D_2D' in arguments:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        # ax.set_aspect(aspect='equal')
        plot_membership_3Dhistogram(ifs01,ax, bins=10, typs=['mu','nu'])

    plot3D = True
    if 'plot3D' in arguments:
        plot_3D_histogramm(ifs01, bins=20)
    #plt.axes().set_aspect('equal', 'datalim')
    plt.show()

    print("Inside...")

if __name__ == "__main__":
    main()

