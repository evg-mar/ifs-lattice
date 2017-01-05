from intuitionistic_fuzzy_set import IFS
from universal_set import UniversalSet
# import numpy as np
from ifs_lattice import piOrd, stdOrd
from ifs_2Dplot import *
from ifs_3Dplot import *
  

def main():

    universe = UniversalSet(set(range(100)))

    ifs00 = IFS(universe, 1)
    ifs00[1] = (1,0)
    ifs00[2] = (0.25,0.35)
    ifs00[3] = (0.3,0.7)
    print(ifs00)
    print(ifs00.neg)
    ifs02 = IFS(universe, 1)
    ifs02[0] = (0,1)
    ifs02[1] = (0.3,0.4)
    ifs02[2] = (0.4,0.35)
    ifs02[3] = (0.3/2,0.7/2)
    ifs02[4] = (0,0)
#     print(ifs02)
    
#     inter = piOrd.sup(ifs00, ifs02)
#     print(inter)
#     
 
    ifs01 = IFS.random(universe, 1, randseed=2)
    id,mu,nu,_ = ifs01.elements_split()
  
    import pandas as pd
    df = pd.DataFrame({'label':id,'mu':mu, 'nu':nu}, index=id)
    print(df.columns)
    df.to_csv('/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/ifs_holder.csv',
              index=True,
              index_col='id',
              header=True)
    
    plot_ifs(ifs01, typ="interval_valued")
    plot_stack(ifs01)
    plot_bar_intValued(ifs01)
    plot_bar_Intuitionistic(ifs01)
    plot_together_intValued(ifs01)
#     plot_together_Intuitionistic(ifs01)
  
    indices, mus, nus, pis = ifs01.elements_split()

    
    plot_triangular(mus, nus, ifs01.get_range(), bins=19)

#     test_legend()


#    plot_triangular_with_arrows(ifs01)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
#   
#     plot_membership_3Dhistogram(ifs01,ax, bins=10, typs=['mu','nu'])
#      
    plot_3D_histogramm(ifs01, bins=10)
    plt.show()
    a = 10
    # args = parse_arguments()
    #
    # logging.basicConfig(level=getattr(logging, args.log[0].upper()))
    # logging.info('Files matching script starting...')



    print("Inside...")

if __name__ == "__main__":
    main()

