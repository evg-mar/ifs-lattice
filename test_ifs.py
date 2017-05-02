from intuitionistic_fuzzy_set import IFS
from universal_set import UniversalSet
# import numpy as np
from ifs_lattice import piOrd, stdOrd
from ifs_2Dplot import *
from ifs_3Dplot import *
  
import numpy as np

from collections import OrderedDict

from openpyxl import load_workbook

#
#evgeniy@evgeniy-TravelMate-P238-M:~$ python -input_file file_name -format 'row' 
#-step_size 20  start 2 end 560 3dHistogram triangular stackbars 



main_path = "/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/"
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

for k, (v1,v2) in result.items():
    print(v1+v2)
    assert(v1+v2 <= 1.0001)

def main():



    ###################
#     universe = UniversalSet(set(range(100)))
# 
#     ifs00 = IFS(universe, 1)
#     ifs00[1] = (1,0)
#     ifs00[2] = (0.25,0.35)
#     ifs00[3] = (0.3,0.7)
#     print(ifs00)
#     print(ifs00.neg)
#     ifs02 = IFS(universe, 1)
#     ifs02[0] = (0,1)
#     ifs02[1] = (0.3,0.4)
#     ifs02[2] = (0.4,0.35)
#     ifs02[3] = (0.3/2,0.7/2)
#     ifs02[4] = (0,0)
# #     print(ifs02)
#     
# #     inter = piOrd.sup(ifs00, ifs02)
# #     print(inter)
# #     
#  
#     ifs01 = IFS.random(universe, 1, randseed=2)
#     id,mu,nu,_ = ifs01.elements_split()
#   
#     import pandas as pd
#     df = pd.DataFrame({'label':id,'mu':mu, 'nu':nu}, index=id)
#     print(df.columns)
#     df.to_csv('/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/ifs_holder.csv',
#               index=True,
#               index_col='id',
#               header=True)
#     
    
    #######################################
    ######################################
    universe = UniversalSet(result.keys())
    
    ifsG = IFS(universe, 1)
    
    for k, value in result.items():
        ifsG.set_bykey(k, value)

    ifs01 = ifsG
    
    ####################################
    ####################################   
    
    if False:
        plot_ifs(ifs01, typ="interval_valued")
        plot_stack(ifs01)
        plot_bar_intValued(ifs01)
        
        plot_together_intValued(ifs01)
    
    plotbar = True
    if plotbar == True:
        plot_bar_Intuitionistic(ifs01)
#     plot_together_Intuitionistic(ifs01)
  
    indices, mus, nus, pis = ifs01.elements_split()

    
    triangular = True
    if triangular == True:
        plot_triangular(mus, nus, ifs01.get_range(), bins=20)

#     test_legend()


#    plot_triangular_with_arrows(ifs01)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
#   
#     plot_membership_3Dhistogram(ifs01,ax, bins=10, typs=['mu','nu'])
#   
    plot3D = True
    if plot3D == True:   
        plot_3D_histogramm(ifs01, bins=20)
    #plt.axes().set_aspect('equal', 'datalim')
    plt.show()
    a = 10
    # args = parse_arguments()
    #
    # logging.basicConfig(level=getattr(logging, args.log[0].upper()))
    # logging.info('Files matching script starting...')



    print("Inside...")

if __name__ == "__main__":
    main()

