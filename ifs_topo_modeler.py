#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 15:16:20 2018

@author: evgeniy
"""

#import numpy as np
#import copy
#from matplotlib.lines import Line2D

#from topo_const_triang import TopoConstTriangInteractive
#from ifs_properties_topo import PropertiesIFSTopo,\
#     PropertiesIFSTopoInteractive, TopoConst, TopoConstInteractive

#from ifs_bar_representation import IfsBar #IfsBarTopoConst
#from editable_rectangle import EditableRectangle #, EditableRectangleRadius
from ifs_triangular_representation import IfsTriangInteractive, IfsTriang
from ifs_operators_plot import incGeneral, incGeneral2, clGeneral, clGeneral2
from ifs_operators_topo import clGeneral_single, incGeneral_single

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

    # def clGeneral(ifset, alpha, beta, gamma_a, gamma_b):

    # def incGeneral2(ifset,alpha0, beta0,
    #                 alpha, beta,
    #                 gamma_a, gamma_b):

    alpha0, alpha = 0.1,  0.4
    gamma_a = 0.3

    beta0, beta = 0.25,  0.45
    gamma_b = 0.6

    # def modCl(x, y):
    #     res = clGeneral(([x], [y]), alpha, beta, gamma_a, gamma_b)
    #     res_x, res_y = res[0][0], res[1][0]
    #     return res_x, res_y

    modCl2 = clGeneral_single('spike', 'continuous', 'mu', alpha0, alpha, gamma_a, beta0, beta, gamma_b)

    modInc2 = incGeneral_single('continuous', 'spike', 'nu', alpha0, alpha, gamma_a, beta0, beta, gamma_b)

    # def modCl2(x, y):
    #     res = clGeneral2(([x], [y]), alpha0, beta0, alpha, beta, gamma_a, gamma_b)
    #     res_x, res_y = res[0][0], res[1][0]
    #     return res_x, res_y
    #
    #
    # def modInc(x, y):
    #     res = incGeneral(([x], [y]), alpha, beta, gamma_a, gamma_b)
    #     res_x, res_y = res[0][0], res[1][0]
    #     return res_x, res_y
    #
    # def modInc2(x, y):
    #     res = incGeneral2(([x], [y]), alpha0, beta0, alpha, beta, gamma_a, gamma_b)
    #     res_x, res_y = res[0][0], res[1][0]
    #     return res_x, res_y


    #
    # modF = lambda x, y: (x + alpha*(1-x-y), y + beta*(1-x-y))
    # modG = lambda x, y: ((1-alpha)*x, (1-beta)*y)
    # modH = lambda x, y: ((1-alpha)*x, y + beta*(1-x-y))
    # modJ = lambda x, y: (x + alpha*(1-x-y), (1-beta)*y)

    # mus_nus_cl = tuple(zip(*[modCl(m, n) for m,n in zip(mus, nus)]))
    mus_nus_cl2 = tuple(zip(*[modCl2(m, n) for m,n in zip(mus, nus)]))
    # mus_nus_inc = tuple(zip(*[modInc(m, n) for m,n in zip(mus, nus)]))
    mus_nus_inc2 = tuple(zip(*[modInc2(m, n) for m,n in zip(mus, nus)]))

    label_id = 'ifs_0000_'


    original_color = 'blue'
    closure_color = 'orange'
    interior_color = 'magenta'

    # prop_triangCl = IfsTriang(axes01, mus_nus_cl,
    #                          radius=0.01, #radia,
    #                          #                                   companions=[prop_bar.editable_rects],
    #                          #                                    companions=None,
    #                          label_id=label_id + 'cl',
    #                          colors = {'mu':'b', 'nu':'g', 'elem':'y'},
    #                          alpha_marker=0.5
    #                          )


    prop_triangCl2 = IfsTriang(axes01, mus_nus_cl2,
                             radius=0.01,
                             label_id=label_id + 'cl2',
                             #                                   companions=[prop_bar.editable_rects],
                             #                                    companions=None,
                             colors = {'mu':'b', 'nu':'g', 'elem':closure_color},
                             alpha_marker=0.8
                             )
    # prop_triangInc = IfsTriang(axes01, mus_nus_inc,
    #                          radius=0.01,
    #                          #                                   companions=[prop_bar.editable_rects],
    #                          #                                    companions=None,
    #                          label_id=label_id+'inc',
    #                          colors = {'mu':'b', 'nu':'g', 'elem':'c'},
    #                          alpha_marker=0.5
    #                          )
    prop_triangInc2 = IfsTriang(axes01, mus_nus_inc2,
                             radius=0.01,
                             #                                   companions=[prop_bar.editable_rects],
                             #                                    companions=None,
                             label_id=label_id+'inc2',
                             colors = {'mu':'b', 'nu':'g', 'elem':interior_color},
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
                                       companions=cols.OrderedDict([
                                                                    # ('Cl', (modCl, prop_triangCl)),
                                                                    ('Cl2', (modCl2, prop_triangCl2)),
                                                                    # ('Inc', (modInc, prop_triangInc)),
                                                                    ('Inc2', (modInc2, prop_triangInc2))
                                                                    ]),
                                       colors = {'mu':'b', 'nu':'g', 'elem':original_color},
                                       alpha_marker=1,
                                       init_flag=False)

    from ifs_properties_topo import TopoConstGeneral
    import os
    #
    # json_topoconst = 'topo_const_config_general.json'
    # json_path = os.path.join(os.getcwd(),'ifsholder')
    # topo_const = TopoConstGeneral.from_json(os.path.join(json_path, json_topoconst), axes01)

    topo_const = TopoConstGeneral(ax=axes01,
                                            alpha=alpha,
                                            beta=beta,
                                            gamma_a=gamma_a,
                                            gamma_b=gamma_b,
                                            alpha0=alpha0,
                                            beta0=beta0)


    topo_const.fill_fixed()

    #
    #    for er, companion1 in zip(prop_bar.editable_rects,
    #                              prop_triang02.holder):
    #        er.companions = [companion1]
    #
    from matplotlib import lines

    original_line = lines.Line2D([0],[0], linestyle="none",
                               c=original_color, marker = 'o')
    closure_line = lines.Line2D([0],[0], linestyle="none",
                               c=closure_color, marker = 'o')
    interior_line = lines.Line2D([0],[0], linestyle="none",
                               c=interior_color, marker = 'o')

    # nuBinsLabel = lines.Line2D([0],[0], linestyle="none",
    #                            c=, marker = 0)
    # elemMapsLabel = lines.Line2D([0],[0], linestyle="none",
    #                              c=colors['elem'], marker = 'o')
    # histBars = plt.Rectangle((0, 0), 1, 1, fc=colors['hist'])


    axes01.legend([original_line, closure_line, interior_line],
              ['Original IFS',
               'Closure IFS',
               'Interior IFS',
               # "Map of the elements from the Universe"
               ],
              numpoints = 2)

    # axes01.legend().set_visible(True)
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