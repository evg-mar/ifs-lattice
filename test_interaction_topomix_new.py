import numpy as np
from matplotlib.lines import Line2D


from ifs_properties_plot import PropertiesIFSTopo,\
     PropertiesIFSTopoInteractive, TopoConst

from editable_rectangle import PropertiesBar
from editable_circle import PropertiesTriang

from widgets_basic import WidgetsSimple


class InteractorBasic(object):
    line_active__  = 0
    index_active__ = 1

    def __init__(self, prop_triang, prop_bar):
        
        self.prop_triang = prop_triang
        self.prop_triang.connect()
#         self.prop_triang.set_animated(False)
#         self.prop_triang.disconnect()
        
        self.prop_bar = prop_bar
        self.prop_bar.connect()





if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from intuitionistic_fuzzy_set import *
    from universal_set import UniversalSet
    from ifs_2Dplot import *
    from ifs_operators_topo import *
    
    

#     fig, ax = plt.subplots()

    universe = UniversalSet(set(range(20)))



    fig = plt.figure()
    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    


    ifs01 = IFS.random(universe, 1, randseed=1)

    indices, mus, nus, pis = ifs01.elements_split()
    
    ax = plt.subplot2grid((4,6), (0,0), rowspan=3, colspan=3)
    
    
    
    
##################
    ax02 = plt.subplot2grid((4,6), (0,3), rowspan=3, colspan=3)
    
    from widgets_basic import WidgetsSimple

    widgets = WidgetsSimple(None)
    
#     topo_c0101 = TopoConst(ax_01, 0.7, 0.2, 0.5)
    
    
    prop_bar = PropertiesBar("prop_bar01", mus, nus, ax02)
#     prop_triang = PropertiesTriang()
#     prop_bar.connect()
#     prop_triang = PropertiesIFSTopoInteractive(label='ifs01_ax01', holder=line2d1_01,
#                                         topo_const=topo_c0101)
#     
    prop_triang = PropertiesTriang(ax, (mus, nus),radius=.01, 
                                   companions=prop_bar.editable_rects)
    
    for er, companion in zip(prop_bar.editable_rects, prop_triang.holder):
        er.companion = companion
        er.prop_triang = prop_triang
    
    interaction = InteractorBasic(prop_triang, prop_bar)
    
    plt.show()