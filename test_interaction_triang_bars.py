#import numpy as np
#from matplotlib.lines import Line2D

from topo_const_triang import TopoConstTriangInteractive
#from ifs_properties_topo import PropertiesIFSTopo,\
#     PropertiesIFSTopoInteractive, TopoConst, TopoConstInteractive

from ifs_bar_representation import IfsBar #IfsBarTopoConst  
from editable_rectangle import EditableRectangle
from ifs_triangular_representation import IfsTriangInteractive #IfsTriangTopoConstInteractive #,\
                                            #IfsTriangInteractive
    
from topo_const_bar import TopoConstBarInteractive

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
    from intuitionistic_fuzzy_set import IFS
    from universal_set import UniversalSet
#    from ifs_2Dplot import *
#    from ifs_operators_topo import *
    
    

#     fig, ax = plt.subplots()

    universe = UniversalSet(set(range(20)))



    fig = plt.figure()
    plt.subplots_adjust(hspace=0.1, wspace=0.1)

    ifs01 = IFS.random(universe, 1, randseed=1)

    indices, mus, nus, pis = ifs01.elements_split()

    axes01 = plt.subplot2grid((4,6), (0,0), rowspan=3, colspan=3)

##################

    ax02 = plt.subplot2grid((4,6), (0,3), rowspan=3, colspan=3)

    from widgets_basic import WidgetsSimple

    widgets = WidgetsSimple(None)
    
#     topo_c0101 = TopoConst(ax_01, 0.7, 0.2, 0.5)
    ax02.set_ylim([0,1])
    ax02.set_aspect(aspect='auto', adjustable='datalim')
#     prop_bar = IfsBar("editable rects",
#                       EditableRectangle, 
#                       (mus,nus), 
#                       ax02)
    alpha_beta = (0.3, 0.5)
#    prop_barT = IfsBarTopoConst("editable rects",
#                      EditableRectangle, 
#                      musnus=(mus,nus),
#                       topo_const_type=TopoConstBarInteractive,
#                      alpha_beta=alpha_beta, 
#                      axes=ax02)
#    prop_barT.connect()

    prop_bar = IfsBar("editable rects",
                      EditableRectangle, 
                      musnus=(mus,nus),
                      #alpha_beta=alpha_beta, 
                      axes=ax02)
    prop_bar.connect()

    
    
#     axes01.set_aspect('equal', 'datalim')
#     prop_triang = IfsTriangInteractive(axes01, (mus, nus),radius=.01,
#                                        companions=prop_bar.editable_rects)
    
#    topoconst = TopoConstTriangInteractive(axes01, 0.6, 0.2, 0.5)
#    topoconst.companion = prop_bar.topo_const_bar
#    prop_bar.topo_const_bar.companion = topoconst
    axes01.set_aspect('equal', 'datalim')
    prop_triang = IfsTriangInteractive(axes01, musnus= (mus, nus),
                                   # topo_const_triang=topoconst,             
                                   radius=.01,
                                   companions=[prop_bar.editable_rects])
#                                    companion_topo_const=prop_bar.topo_const_bar)

    for er, companion in zip(prop_bar.editable_rects, prop_triang.holder):
        er.companion = companion
        # er.prop_triang = prop_triang
 
    
    interaction = InteractorBasic(prop_triang, prop_bar)

    plt.show()
