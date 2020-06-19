#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 15:16:20 2018

@author: evgeniy
"""

from ifs_triangular_representation import IfsTriangInteractive, IfsTriang

import collections as cols
#from topo_const_bar import TopoConstBarInteractive

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
    import numpy as np
    

#     fig, ax = plt.subplots()

    universe = UniversalSet(set(range(5)))



    fig = plt.figure()
    plt.subplots_adjust(hspace=0.1, wspace=0.1)

    ifs01 = IFS.random(universe, 1, randseed=1)
    indices, mus, nus, pis = ifs01.elements_split()

    
    ifs02 = IFS.random(universe, 1, randseed=2)
    indices02, mus02, nus02, pis02 = ifs02.elements_split()

    
    axes01 = plt.subplot2grid((5,7), (0,0), rowspan=4, colspan=4)
    
#    _, line2d2_01 = plot_triangular_(axes01,
#                                    mus, nus, ifs02.get_range(), bins=10,
#                                    rotation={'x':45, 'y':0},
#                                    alpha=0.3)    
#    
#    axes01.set_xlim([0,1])
#    axes01.set_ylim([0,1])
    
    axes01.set_aspect('equal', 'datalim')
    
##################

#    ax02 = plt.subplot2grid((5,7), (0,4), rowspan=4, colspan=4)

    
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()    
    
    
    
    from widgets_basic import WidgetsSimple

    widgets = WidgetsSimple(None)
    
#    ax02.set_ylim([0,1])
#    ax02.set_aspect(aspect='auto', adjustable='datalim')

    alpha_beta = (0.3, 0.5)


    ######
#    radia = np.random.uniform(0.0, 0.15, len(mus))
#    prop_bar = IfsBar("editable rects",
#                      EditableRectangleRadius, 
#                      musnus=(radia, [0.0]*len(radia)),
#                      axes=ax02)
#    prop_bar.connect()


#    prop_bar02 = IfsBar("editable rects01",
#                  EditableRectangleRadius, 
#                  musnus=(mus02,nus02),
#                  axes=ax02)
#    prop_bar02.connect()

    #######
    

    
    alpha, beta = 0.25, 0.3
    
    modF = lambda x, y: (x + alpha*(1-x-y), y + beta*(1-x-y))
    modG = lambda x, y: ((1-alpha)*x, (1-beta)*y)
    modH = lambda x, y: ((1-alpha)*x, y + beta*(1-x-y))    
    modJ = lambda x, y: (x + alpha*(1-x-y), (1-beta)*y)
    
    mus_nus_F = tuple(zip(*[modF(m, n) for m,n in zip(mus, nus)]))
    mus_nus_G = tuple(zip(*[modG(m, n) for m,n in zip(mus, nus)]))
    mus_nus_H = tuple(zip(*[modH(m, n) for m,n in zip(mus, nus)]))
    mus_nus_J = tuple(zip(*[modJ(m, n) for m,n in zip(mus, nus)]))
    
    label_id = 'ifs_0000_'

    prop_triangF = IfsTriang(axes01, mus_nus_F,
                                   radius=0.01, #radia,
#                                   companions=[prop_bar.editable_rects],
#                                    companions=None,
                                    label_id=label_id + 'F',
                                   colors = {'mu':'b', 'nu':'g', 'elem':'y'},
                                   alpha_marker=0.5
                                    )

    
    prop_triangG = IfsTriang(axes01, mus_nus_G,
                                   radius=0.01,
                                    label_id=label_id + 'G',
#                                   companions=[prop_bar.editable_rects],
#                                    companions=None,
                                   colors = {'mu':'b', 'nu':'g', 'elem':'orange'},
                                   alpha_marker=0.8
                                    )
    prop_triangH = IfsTriang(axes01, mus_nus_H,
                                   radius=0.01,
#                                   companions=[prop_bar.editable_rects],
#                                    companions=None,
                                    label_id=label_id+'H',
                                   colors = {'mu':'b', 'nu':'g', 'elem':'c'},
                                   alpha_marker=0.5
                                    )
    prop_triangJ = IfsTriang(axes01, mus_nus_J,
                                   radius=0.01,
#                                   companions=[prop_bar.editable_rects],
#                                    companions=None,
                             label_id=label_id+'J',
                                   colors = {'mu':'b', 'nu':'g', 'elem':'g'},
                                   alpha_marker=0.5
                                    )   


    from ifs_operators_plot import incl_i

    
    metrics_binary = \
        cols.OrderedDict([ ('incl_j', 
            lambda musnus1_musnus2: incl_i(musnus1_musnus2[0], musnus1_musnus2[1]))])

#        r' $\varepsilon_{0,\nu}$'
        
    metrics_unary = cols.OrderedDict([ ('Mean_mu', lambda musnus: np.mean(musnus[0])),
                  ('Mean_nu', lambda musnus: np.mean(musnus[1])),                      
                 ('Ind_pi,1', lambda musnus: 
                     (1/len(musnus)*np.sum(1-np.array(musnus[0])-np.array(musnus[1])))),
                ('Ind_pi,infty', lambda musnus: 
                     np.max(1-np.array(musnus[0])-np.array(musnus[1]))),
                   ])

    
    
    prop_triang = IfsTriangInteractive(axes01, 
                                       axes_metrics=axes01,
                                       label_id=label_id+'original',
                                       metrics_unary=metrics_unary,
                                       metrics_binary=metrics_binary,
                                       musnus=(mus, nus),
                                   radius=.01,
#                                   companions=[prop_bar.editable_rects],
        companions=cols.OrderedDict([('F', (modF, prop_triangF)),
                         ('G', (modG, prop_triangG)),
                         ('H', (modH, prop_triangH)),
                         ('J', (modJ, prop_triangJ))
                         ]),
                                    colors = {'mu':'b', 'nu':'g', 'elem':'blue'},
                                    alpha_marker=1,
                                    init_flag=False)

    
#    
#    for er, companion1 in zip(prop_bar.editable_rects, 
#                              prop_triang02.holder):
#        er.companions = [companion1]    
#      
 
    axes01.legend().set_visible(False)
    #interaction = InteractorBasic(prop_triang, prop_bar)
#    prop_bar.connect()

  
    prop_triang.connect()

    from widgets_operators import WidgetsSimpleOperator

    
    widgets = WidgetsSimpleOperator(active_prop=prop_triang, 
                                    canvas=prop_triang.canvas)
    
    widgets.recreate_widgets_(prop_triang)    
    
    
#    prop_triang02.connect()

    plt.show()
    
    prop_triang.update_tables()