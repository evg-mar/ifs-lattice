#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 10:27:00 2018

@author: evgeniy
"""

from editable_rectangle import EditableRectangle, RectangleBasic
from topo_const_bar import TopoConstBarInteractive
from matplotlib.patches import Rectangle
import numpy as np

class IfsBar(object):
    
    def __init__(self, label,
                       bar_type, # EditableRectangle or RectangleBasic
                       musnus,
                       axes=None,
                       color_mu='blue',
                       color_nu='green',
                       alpha=0.5, 
                       hide_ifs=False,
                       showlabels=False,
                       companion=None):
        assert(len(musnus[0])==len(musnus[0]))
        self.label = label
        self.axes = axes

        self.mus = np.asarray(musnus[0])
        self.nus = np.asarray(musnus[1])
        self.indices = np.arange(len(self.mus)) 
        self.pis = 1.0 - self.nus - self.mus

        self.bar = axes.bar(self.indices, [1.0]*len(self.indices))
        
        self.axes.set_aspect(aspect='auto', adjustable='datalim')
        self.axes.set_ylim([0,1])

        self.companion = companion
                 

        self.editable_rects = [Rectangle((0,0), 1, 1)] * len(self.indices)

        for idx, (rect, mu, nu) in enumerate(zip(self.bar, self.mus, self.nus)):
            rect.set_facecolor("white")
            er = bar_type(rect, mu, nu, color_mu, color_nu, alpha)
#             er.connect()
            self.editable_rects[idx] = er
            if self.companion is not None:
                er.companion = self.companion[idx]
                er.on_release(None)
                er.companion.on_release(None)

        self.alpha = alpha 
        self.hide_ifs = hide_ifs


    def draw_blit(self):
        for er in self.editable_rects:
            er.draw_blit()
            
    @property
    def get_size(self):
        return len(self.indices)
    
    def set_companion(self, companion):
        self.companion = companion
        for er, comp in zip(self.editable_rects, self.companion):
            er.companion = comp
            comp.on_release(None)
            er.on_release(None)
               
    def connect(self):
        for er in self.editable_rects:
            er.connect()

    def disconnect(self):
        for er in self.editable_rects:
            er.disconnect()

    # Setters
    def set_x(self, mus):
        for mu, er in zip(mus, self.editable_rects):
            er.set_mu(mu)
            
    def set_y(self, nus):
        for nu, er in zip(nus, self.editable_rects):
            er.set_mu(nu)
            
    def set(self, mus, nus):
        for mu, nu, er in zip(mus, nus, self.editable_rects):
            er.set_munu((mu, nu))       
    
    # Getters
    def get_x(self):
        return np.array([rect.get_mu() for rect in self.editable_rects])
    
    def get_y(self):
        return np.array([rect.get_nu() for rect in self.editable_rects])

    def get_data_pair(self):
        return (self.get_x(), self.get_y())
    
    def get_data(self):
        return np.array([(r.get_mu(), r.get_nu()) for r in self.editable_rects])


class IfsBarTopoConst(IfsBar):
    def __init__(self, label,
                       bar_type, # EditableRectangle or RectangleBasic
                       musnus,
                       topo_const_type, # TopoConstBarInteractive
                       alpha_beta,
                       axes=None,
                       color_mu='blue',
                       color_nu='green',
                       alpha=0.5, 
                       hide_ifs=False,
                       showlabels=False,
                       companion=None):
        super(IfsBarTopoConst, self).__init__(label, bar_type, musnus,
                                              axes, color_mu, color_nu, alpha,
                                              hide_ifs, showlabels,
                                              companion=companion)
        start_xlim, end_xlim = self.axes.get_xlim()
        print('start: ' + str(start_xlim))
        print('end: ' + str(end_xlim))
        
        width = 0.1
        height = 1.0
        #self.axes.set_xlim([start_xlim, end_xlim + width])
        rect = Rectangle((end_xlim-width, 0.0), width, height,
                         fc='white')
        
        self.axes.add_patch(rect)
        self.topo_const_bar = topo_const_type(rect, 
                                          alpha_beta[0],
                                          alpha_beta[1])

        

    def connect(self):
        super(IfsBarTopoConst, self).connect()
        self.topo_const_bar.connect()
        
    def disconnect(self):
        super(IfsBarTopoConst, self).disconnect()
        self.topo_const_bar.disconnect()


if __name__ == '__main__':
    
    import matplotlib.pyplot as plt

    fig = plt.figure()

    axes1 = plt.subplot2grid((1,2), (0,0), rowspan=1, colspan=1)
    # rects = ax.bar(range(10), [1]*10)
    
#     prop1 = IfsBar("proba01", EditableRectangle,  
#                    ([0.1, 0.4, 0.6],[0.6, 0.4, 0.4]), axes=axes1)
#     prop1.connect()


    prop1 = IfsBar("proba01", EditableRectangle,  
                   ([0.1, 0.4, 0.6, 0.2, 0.4, 0.5],[0.6, 0.4, 0.4, 0.4, 0.3, 0.2]),
                   #topo_const_type=TopoConstBarInteractive,
                   #alpha_beta = (0.3, 0.5),
                    axes=axes1)
    prop1.connect()


#
#    prop1 = IfsBarTopoConst("proba01", EditableRectangle,  
#                   ([0.1, 0.4, 0.6, 0.2, 0.4, 0.5],[0.6, 0.4, 0.4, 0.4, 0.3, 0.2]),
#                   topo_const_type=TopoConstBarInteractive,
#                   alpha_beta = (0.3, 0.5),
#                    axes=axes1)
#    prop1.connect()
    

#    prop01 = IfsBar("proba001", EditableRectangle,  
#                   ([0.3, 0.2, 0.1, 0.6, 0.1, 0.5],[0.3, 0.7, 0.7, 0.2, 0.8, 0.3]),
#                   #topo_const_type=TopoConstBarInteractive,
#                   #alpha_beta = (0.2, 0.9),
#                    axes=axes1,
#                    alpha=0.3)
#    prop01.connect()


    
    axes2 = plt.subplot2grid((1,2), (0,1), 
                             sharey=axes1, sharex=axes1,
                             rowspan=1, colspan=1)
#    axes2.set_axis_bgcolor("red")
    axes2.yaxis.set_label_position("left")
    prop2 = IfsBar("proba02", EditableRectangle,  
                   ([0.3, 0.2, 0.1, 0.6, 0.1, 0.5],[0.3, 0.7, 0.7, 0.2, 0.8, 0.3]),
                    color_mu='blue',
                    color_nu='black',
                   #topo_const_type=TopoConstBarInteractive,
                   #alpha_beta = (0.3, 0.5),
                    axes=axes2,
                    companion=prop1.editable_rects)
    prop2.connect()

    prop1.set_companion(prop2.editable_rects)
    # prop2.set_companion(prop1.editable_rects)
    
    plt.show()
