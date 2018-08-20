from intuitionistic_fuzzy_set import IFS
from universal_set import UniversalSet

# from ifs_lattice import piOrd, stdOrd
from ifs_2Dplot import plot_triangular, plot_bar_Intuitionistic
from ifs_3Dplot import plot_3D_histogramm
import matplotlib.pyplot as plt
  
from collections import OrderedDict
from openpyxl import load_workbook

import sys
import argparse


parser = argparse.ArgumentParser(
    description='Plot ICA arguments handler',
)


parser.add_argument('-input_file', action="store",
                    type=str,
                    help = 'Input file name')
parser.add_argument('-sheet', action="store",
                    type=str,
                    help = 'Name of the sheet in the file')
parser.add_argument('-format', action="store",
                    type=str,
                    help = 'Format of input file: row or matrix')
parser.add_argument('-start', action="store",
                    dest="start", type=int)
parser.add_argument('-end', action="store",
                    dest="end", type=int)
parser.add_argument('--number_bins', action="store", default=15,
                    dest="number_bins", type=int)
parser.add_argument('-plot', action='append',
                    #dest='collection',
                    default=[],
                    help='What to plot: 2dHistogram, 2dHistogram, stackbars')


#evgeniy@evgeniy-TravelMate-P238-M:~$ python -input_file file_name -format 'row' 
#-step_size 20  start 2 end 560 3dHistogram triangular stackbars 

#  python ica_plot.py -input_file ./ifsholder/SecondOrderICA_mutr_Dafi.xlsx 
# -sheet GASeries_00030_MuNu -format row -start 2 -end 562 -plot 3dHistogram


main_path = "/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/"
file_name = "Mutr_ICA_Evgeni.xlsx"
file_name ="SecondOrderICA_mutr_Dafi.xlsx"
sheet = "GASeries_00030_MuNu"

parsed = parser.parse_args(['-input_file', main_path + file_name, '-sheet', sheet,
                            '-format', 'row',
                            '-start', '2',
                            '-end', '562',
                            '-plot', ['2dHistogram','2DHistogram','stackbars']])
#
# main_path + file_name
# sheet = "GASeries_00030_MuNu"


start = 1 # 2
end = 561 # 562


def get_ifs(parsed):

    def get_pair(str_pair):
        lst = str_pair.strip(')(').split(',')
        mu = lst[0].strip()
        nu = lst[1].strip()
        return float(mu), float(nu)

    wb = load_workbook(parsed.input_file, read_only=True)
    ws = wb[parsed.sheet]
        
    start = parsed.start - 1 
    end = parsed.end -1    
        
    rows = list(ws.rows)    
    result = OrderedDict([(row[0].value, get_pair(row[1].value)) \
                          for row in rows[start:end]])
    return result

'''
ws = wb["Res_Dian-full"]


def get_holder(start, end, data_generator):
    
    rows = list(data_generator)[start:end]    
    
    holder = np.zeros((100,100), dtype=float)
    
    for h, row in zip(holder, rows[0:100]):
        h[:] = [r.value for r in row[1:101]]
    return holder


def generate_universum_values(holder):
    result = OrderedDict()
    for idx, row in enumerate(holder):
        for i in range(idx+1, len(holder)):
            label = "G"+str(idx+1)+","+str(i+1)
            #print(label)
            #print(row[i])
            result[label] = row[i]
    return result

start_mu = 1
end_mu = 101

start_nu = 103
end_nu = 203

holder_mu = get_holder(start_mu, end_mu, ws.rows)

holder_nu = get_holder(start_nu, end_nu, ws.rows)
    
res_mu = generate_universum_values(holder_mu)

res_nu = generate_universum_values(holder_nu)


r = [(k1, (v1, v2)) for ((k1,v1),(k2,v2)) in zip(res_mu.items(), res_nu.items())]

result = OrderedDict(r)
'''

#for k, (v1,v2) in result.items():
#    print(v1+v2)
#    assert(v1+v2 <= 1.0001)

def main():

 
    parsed = parser.parse_args(sys.argv[1:])
    result = get_ifs(parsed)
    #######################################
    ######################################
    universe = UniversalSet(result.keys())
    
    ifsG = IFS(universe, 1)
    
    for k, value in result.items():
        ifsG.set_bykey(k, value)

    ifs01 = ifsG
    
    ####################################
    ####################################   
    
        
    plotbar = True
    if 'stackbars' in parsed.plot:
        plot_bar_Intuitionistic(ifs01)
#     plot_together_Intuitionistic(ifs01)
  
    indices, mus, nus, pis = ifs01.elements_split()

    
    triangular = True
    if '2dHistogram' in parsed.plot:
        plot_triangular(mus, nus, ifs01.get_range(), bins=parsed.number_bins)

#     test_legend()


#    plot_triangular_with_arrows(ifs01)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
#   
#     plot_membership_3Dhistogram(ifs01,ax, bins=10, typs=['mu','nu'])
#   
    plot3D = True
    if '3dHistogram' in parsed.plot:   
        plot_3D_histogramm(ifs01, bins=parsed.number_bins)
    #plt.axes().set_aspect('equal', 'datalim')
    plt.show()
    a = 10


    print("Inside...")

if __name__ == "__main__":
    main()

