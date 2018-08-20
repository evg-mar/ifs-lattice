#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 08:50:52 2018

@author: evgeniy
"""

import numpy as np
import json

from matplotlib.lines import Line2D
from matplotlib.artist import Artist

#import ifs_operators_plot as oper  

#from ifs_properties_plot import PropertiesIFSTopo

from ifs_properties_plot import PropertiesIFS



########################################



class PropertiesIFSInteractive(PropertiesIFS):
    
    def __init__(self, axes=None,
                       holder=None,
                       companions=[],
                       label=None,
                       radius=5,
                       annotations=None,
                       alpha_marker=0.5, 
                       labels_size=12,
                       show_ann=True,
                       hide_ifs=False,
                       showverts=True,
                       showedges=False,
                       showlabels=False):

        super(PropertiesIFSInteractive, self).__init__(
                       label,
                       holder,
                       radius,
                       annotations,
                       alpha_marker, 
                       labels_size,
                       hide_ifs,
                       show_ann,
                       showverts,
                       showedges,
                       showlabels)

        self.idx_active = None
        self.companions = companions
        self.axes = axes

    @classmethod
    def from_properties_ifs(cls, prop_ifs):
        return  cls(prop_ifs.label,
                   prop_ifs.holder,
                   # prop_ifs.topo_const,
                   prop_ifs.radius,
                   prop_ifs.annotations,
                   prop_ifs.alpha_marker, 
                   prop_ifs.labels_size,
                   prop_ifs.hide_ifs,
                   prop_ifs.show_ann,
                   prop_ifs.showverts,
                   prop_ifs.showedges,
                   prop_ifs.showlabels)

    
    def set_animated(self, value):
        super(PropertiesIFSInteractive, self).set_animated(value)
        # self.topo_const.set_animated(value)

    def connect(self):
        canvas = self.axes.figure.canvas
#         self.ciddraw = canvas.mpl_connect('draw_event',
#                                 self.draw_callback)
        self.cidpress = canvas.mpl_connect('button_press_event',
                                self.button_press_callback)
#        self.cidkeypress =  self.canvas.mpl_connect('key_press_event',
#                                 self.key_press_callback)
        self.cidrelease = canvas.mpl_connect('button_release_event',
                                self.button_release_callback)
        self.cidmotion = canvas.mpl_connect('motion_notify_event',
                                self.motion_notify_callback)


    def disconnect(self):
        'disconnect all the stored connection ids'
        canvas = self.axes.figure.canvas

        canvas.mpl_disconnect(self.cidmotion)        
        canvas.mpl_disconnect(self.cidpress)
        canvas.mpl_disconnect(self.cidrelease)
        canvas.mpl_disconnect(self.cidmotion)


    def draw_callback(self, event):

        self.draw_holder_annotations(self.axes)
    
        canvas = self.axes.figure.canvas
        canvas.blit(self.axes.bbox)        
        self.background = canvas.copy_from_bbox(self.axes.figure.bbox)


    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        print('button_pres - event in axis')
        print(event.inaxes)
        print('contains:')
        print(self.holder.contains(event))

        if event.inaxes is None or event.inaxes != self.axes:
            return
        if event.button != 1:
            return

        if not self.holder.get_visible():
            return

        self.idx_active = self.get_ind_under_point(event.xdata,
                                              event.ydata)
        
        if self.idx_active is None:
            return
    
        for prop in self.companions:
            prop.idx_active = self.idx_active
            
        canvas = self.axes.figure.canvas
        axes = self.axes
        
        if self.idx_active > -1:
            if self.show_ann:
                self.set_animated_annotations(True)
            if self.showverts:
                self.holder.set_animated(True)
        else:
            ### self.topo_const.set_animated(True)
            pass

        for prop in self.companions:
            if prop.idx_active > -1:
                if prop.show_ann:
                    prop.set_animated_annotations(True)
                if prop.showverts:
                    prop.holder.set_animated(True)
        
        canvas.draw()
        
        self.background = canvas.copy_from_bbox(self.axes.figure.bbox)

        # now redraw just the rectangle
        if self.idx_active > -1:
            self.draw_holder_annotations(self.axes)
            for prop in self.companions:
                prop.draw_holder_annotations(self.axes)
        else:
            ### self.topo_const.draw_topo_object()
            pass
        # and blit just the redrawn area
        canvas.blit(axes.bbox)
    
        print('button press callback: idx = %d' 
              % -1 if self.idx_active is None else self.idx_active)
        

    def get_ind_under_point(self, xdata, ydata):
        'get the index of the vertex under point if within epsilon tolerance'

        # display coords
#         print(event.inaxes)
        xy = np.asarray(self.get_data_pair())
        print('get the index..')
        print(self.get_data_pair())
        print(xy)
        x0, y0 = xy[0], xy[1]

        x = np.zeros(len(x0), dtype=float)
        x[0:] = x0

        y = np.zeros(len(y0), dtype=float)
        y[0:] = y0

        d = np.sqrt((x - xdata)**2 + (y - ydata)**2)
        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
        ind = indseq[0]
        
        ind = None if (d[ind] >= self.epsilon) else ind
        ind = -1 if ind == len(x0) else ind
        print('ind found: %d' % ind if ind is not None else -5)
        return ind


    def motion_notify_callback(self, event):
#         print('on mouse movement')
        if event.inaxes is None or event.inaxes != self.axes:
            return
        if event.button != 1:
            return
        if not self.holder.get_visible():
            return
        if self.idx_active is None:
#                 print('idx_act %d' % -1 if idx_act is None else idx_act)
            return
                
        # The drop & drag point should stay
        # within the triangular area

        xdata = min(max(0.0, event.xdata), 1.0) 
        ydata = min(max(0.0, event.ydata), 1.0) 
#             print('on mouse movement')
        if self.idx_active > -1:
            self.update_holder_annotation(xdata, ydata)
            self.update_holder_annotation_companions(xdata, ydata)
            print('update holder & annotation')
#                self.update_holder_annotation(prop_ifs_inactive,
#                                              idx_act,
#                                              xdata, ydata)                
            self.axes.figure.canvas.restore_region(self.background)
            self.draw_holder_annotations(self.axes)
        
        elif self.idx_active == -1:
            ### self.update_topo_const(xdata, ydata)
            ### self.axes.figure.canvas.restore_region(self.background)
            ### self.topo_const.draw_topo_object()        
            pass

        self.axes.figure.canvas.blit(self.axes.bbox)

    def button_release_callback(self, event):
        'whenever a mouse button is released'

        if event.button != 1:
            return
        if not self.holder.get_visible():
            return
#             print("active prop %s" % self.ax_active)
#             print("active prop %s" % self.active_lines_idx[self.ax_active][0].label)
            
        self.idx_active = None

        self.set_animated(False)
        self.set_animated_annotations(False)

        self.axes.figure.canvas.draw()

    def update_holder_annotation(self, xdata, ydata):
        print("..in update holder annotations...")
        print(xdata, ydata, self.idx_active)
        if xdata + ydata >= 1.0:
            pos = ((xdata-ydata+1)/2, (ydata-xdata+1)/2)
        else:
            pos = (xdata,ydata)
            
        line_xy = list(zip(*self.get_data_pair()))    
        line_xy[self.idx_active] = pos
        data = list(zip(*line_xy))

        print(data)
        print(data[0])
        print(data[1])
        
        self.set_data(data[0], data[1])     
        
        
        if self.show_ann:
            print("updating the annotation...")
            self.set_data_annotations_single(self.idx_active, pos)
        
        
    def update_holder_annotation_companions(self, xdata, ydata):
        for prop in self.companions:
            prop.idx_active = self.idx_active
            prop.update_holder_annotation(xdata, xdata)

#    @classmethod
#    def update_holder_annotation(cls, prop_ifs, idx_act, xdata, ydata):
##         print("..in update holder annotations...")
#        if xdata + ydata >= 1.0:
#            pos = ((xdata-ydata+1)/2, (ydata-xdata+1)/2)
#        else:
#            pos = (xdata,ydata)
#            
#        line_xy = list(zip(*prop_ifs.get_data_pair()))    
#        line_xy[idx_act] = pos
#        data = list(zip(*line_xy))
#
#        prop_ifs.set_data(data[0], data[1])     
#        
#        
#        if prop_ifs.show_ann:
#            prop_ifs.set_data_annotations_single(idx_act, pos)


#######################################

#
#class TriangularInteractorBasic(object):
#    line_active__  = 0
#    index_active__ = 1
#
#    def __init__(self, ax01, ax02, axlines, widgets,
#                       epsilon=0.02):
#        
#        self._epsilon = epsilon # max pixel distance to count as a vertex hit
#
#
#
#        self.axlines = axlines
#
#        self.ax02 = ax02
#        for prop_ifs in self.axlines[self.ax02]:
#            prop_ifs.init_default(ax02)
#
#        self.ax01 = ax01
#        for prop_ifs in self.axlines[self.ax01]:
#            prop_ifs.init_default(ax01)
#
#        ### (line_number, active idx in that line)
#        self.active_lines_idx = {self.ax01: [self.axlines[self.ax01][0], None],
#                                 self.ax02: [self.axlines[self.ax02][0], None]}
#
#        self.ax_active = self.ax01
#
#        canvas = self.ax01.figure.canvas
#       
#        self.canvas = canvas
#        self.mpl_connect_init()
#        
#
#        self.colors_ifs = { }
#        for ax, properties in self.axlines.items():
#            colors_map = {i: prop.holder.get_color() \
#                                for i, prop in enumerate(properties)}
#            self.colors_ifs[ax] = colors_map 
#
#       
#        self.widgets = widgets
#        self.widgets.canvas = self.canvas 
#        self.recreate_widgets()
#        
#        self.ax01.set_aspect('equal', 'datalim')
#        self.ax02.set_aspect('equal', 'datalim')
#
#    def mpl_connect_init(self):
#        self.canvas.mpl_connect('draw_event',
#                                self.draw_callback)
#        self.canvas.mpl_connect('button_press_event',
#                                self.button_press_callback)
#        self.canvas.mpl_connect('key_press_event',
#                                self.key_press_callback)
#        self.canvas.mpl_connect('button_release_event',
#                                self.button_release_callback)
#        self.canvas.mpl_connect('motion_notify_event',
#                                self.motion_notify_callback)
#
#
#    def draw_callback(self, event):
#
#        for prop_ifs in self.axlines[self.ax01]:
#            prop_ifs.draw_holder_annotations(self.ax01)
#            
#        for prop_ifs in self.axlines[self.ax02]:
#            prop_ifs.draw_holder_annotations(self.ax02)
#
#        if self.ax_active is not None:
#            self.canvas.blit(self.ax_active.bbox)        
#            self.background = \
#                self.canvas.copy_from_bbox(self.ax_active.figure.bbox)
#
#
#    def motion_notify_callback(self, event):
##         print('on mouse movement')
#        if event.inaxes is None:
#            return
#        if event.button != 1:
#            return
#
#        if event.inaxes in self.active_lines_idx.keys():
##             print('on mouse movement')
#            self.ax_active = event.inaxes
#            
#            prop_ifs, idx_act = self.active_lines_idx[self.ax_active]
#        
#            if not prop_ifs.holder.get_visible():
#                return
#            if idx_act is None:
##                 print('idx_act %d' % -1 if idx_act is None else idx_act)
#                return
#
#            ax_inactive = self.ax01 if self.ax01!=self.ax_active else self.ax02
#            prop_ifs_inactive, _ = self.active_lines_idx[ax_inactive]
#                
#            # The drop & drag point should stay
#            # within the triangular area
#
#            xdata = min(max(0.0, event.xdata), 1.0) 
#            ydata = min(max(0.0, event.ydata), 1.0) 
##             print('on mouse movement')
#            if idx_act > -1:
#                self.update_holder_annotation(prop_ifs,
#                                              idx_act,
#                                              xdata, ydata)
##                self.update_holder_annotation(prop_ifs_inactive,
##                                              idx_act,
##                                              xdata, ydata)                
#            elif idx_act == -1:
#                ### prop_ifs.update_topo_const(xdata, ydata)
#                ### prop_ifs_inactive.update_topo_const(xdata, ydata)
#                pass
#
#            self.canvas.restore_region(self.background)
#
#            prop_ifs.draw_holder_annotations(self.ax_active)
#
#        self.canvas.blit(self.ax_active.bbox)
#
#    @classmethod
#    def update_holder_annotation(cls, prop_ifs, idx_act, xdata, ydata):
##         print("..in update holder annotations...")
#        if xdata + ydata >= 1.0:
#            pos = ((xdata-ydata+1)/2, (ydata-xdata+1)/2)
#        else:
#            pos = (xdata,ydata)
#            
#        line_xy = list(zip(*prop_ifs.get_data_pair()))    
#        line_xy[idx_act] = pos
#        data = list(zip(*line_xy))
#
#        prop_ifs.set_data(data[0], data[1])     
#        
#        
#        if prop_ifs.show_ann:
#            prop_ifs.set_data_annotations_single(idx_act, pos)
##             annotation = prop_ifs.annotations[idx_act]
##             annotation.xyann =  pos
##             annotation.xy = pos
##             annotation.xytext = pos
#
#
#    def line_changes(self, line):
#        '''
#        This method is called whenever the line object is called
#        '''
#        pass
#
#    def poly_changed(self, poly):
#        'this method is called whenever the polygon object is called'
#        # only copy the artist props to the line (except visibility)
#        vis = self.line1_01.get_visible()
#        Artist.update_from(self.line1_01, poly)
#        self.line1_01.set_visible(vis)  # don't use the poly visibility state
##         self.line.set_linestyle(' ')
#
#    def get_ind_under_point(self, xdata, ydata, prop_ifs):
#        'get the index of the vertex under point if within epsilon tolerance'
#
#        # display coords
##         print(event.inaxes)
#        xy = np.asarray(prop_ifs.get_data_pair())
#        print('get the index..')
#        # print(prop_ifs.get_data_pair())
#        # print(xy)
#        x0, y0 = xy[0], xy[1]
#
##        x = np.zeros(len(x0)+1, dtype=float)
##        x[0:-1] = x0
##        x[-1] = prop_ifs.topo_const.alpha
##        
##        y = np.zeros(len(y0)+1, dtype=float)
##        y[0:-1] = y0
##        y[-1] = prop_ifs.topo_const.beta
#
#        x = np.zeros(len(x0), dtype=float)
#        x[0:] = x0
#        ### x[-1] = prop_ifs.topo_const.alpha
#        
#        y = np.zeros(len(y0), dtype=float)
#        y[0:] = y0
#        ### y[-1] = prop_ifs.topo_const.beta
#
#        
##         print(x)
##         print(y)
##         print(event.xdata, event.ydata)
##         print(event.x, event.y)
##         print(self.ax01.transData.inverted().transform((event.x, event.y)))
##         print(event.xdata, event.ydata)
#
#        d = np.sqrt((x - xdata)**2 + (y - ydata)**2)
#        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
#        ind = indseq[0]
#        
#        ind = None if (d[ind] >= self._epsilon) else ind
#        ind = -1 if ind == len(x0) else ind
#        return ind
#
#    def recreate_widgets(self):
#        print("in reacreate widgets...")
#        self.widgets.colors_ifs = self.colors_ifs[self.ax_active]
#        prop_ifs, _ = self.active_lines_idx[self.ax_active]
#        idx = self.axlines[self.ax_active].index(prop_ifs)
#        
#        self.widgets.recreate_widgets_(#prop_ifs,
##                                       idx,
##                                       self.axlines[self.ax_active],
#                                      self.active_lines_idx[self.ax_active][0])
#        if prop_ifs != self.widgets.prop_ifs:
#            self.active_lines_idx[self.ax_active] =[self.widgets.active_prop[0],
#                                                    None]
#
#        if not self.widgets.active_prop.holder.get_visible():
#            self.active_lines_idx[self.ax_active][self.index_active__] = None
#
#        print("active prop %s" % self.ax_active)
#        print("active prop %s" % self.active_lines_idx[self.ax_active][0].label)
#        print("widgets prop %s" % self.widgets.prop_ifs.label)
#        print("-------------")
#
#
#    def button_press_callback(self, event):
#        'whenever a mouse button is pressed'
#        print('button_pres - event in axis')
#        print(event.inaxes)
#
#        if event.inaxes is None:
#            return
#        if event.button != 1:
#            return
#
##         if event.inaxes == self.widgets.rax_activeifs:
#        if event.inaxes in self.active_lines_idx.keys():        
#            self.recreate_widgets()
#
#        if event.inaxes in self.active_lines_idx.keys():
#            if self.ax_active != event.inaxes:
#                self.ax_active = event.inaxes
#                self.recreate_widgets()
#            
#
##             self.refresh_widgets()
#            prop_ifs, _ = self.active_lines_idx[self.ax_active]
#
#            if not prop_ifs.holder.get_visible():
#                return
#
#            idx_active = self.get_ind_under_point(event.xdata,
#                                                  event.ydata,
#                                                  prop_ifs)
#            print('button press callback: idx = %d' % -1 if idx_active is None else idx_active)
#            self.active_lines_idx[self.ax_active][self.index_active__] =\
#                                                                 idx_active
#
#
#    def button_release_callback(self, event):
#        'whenever a mouse button is released'
#
#        if event.button != 1:
#            return
#
#        if self.ax_active in self.active_lines_idx.keys():
#            prop_ifs, idx_act = self.active_lines_idx[self.ax_active]
#            
#            if not prop_ifs.holder.get_visible():
#                return
##             print("active prop %s" % self.ax_active)
##             print("active prop %s" % self.active_lines_idx[self.ax_active][0].label)
#            
#            self.active_lines_idx[self.ax_active][self.index_active__] = None
#
#        if self.ax_active == self.ax01:
#            idx = self.axlines[self.ax_active].index(prop_ifs)
#            prop2_ifs = self.axlines[self.ax02][idx]          
#
#            # !!!!!!!!!! mus, nus = prop_ifs.incGeneral()
#            mus, nus = prop_ifs.get_data_pair()
#            #
#            prop2_ifs.set_data(mus,nus)
#            prop2_ifs.set_data_annotations(list(zip(mus,nus)))
#
#
#        self.canvas.draw()
#
#
#
#
#    def key_press_callback(self, event):
#        'whenever a key is pressed'
#        print('## key press callback')
#        print('nothing doing...')
#        print(type(event.inaxes))
#        print(event.inaxes)
#        print(event.xdata, event.ydata)
#        print(event.x, event.y)
#        print(event)
#        
##         if not event.inaxes:
##             return
## 
##         if event.key == 't':
##             self.update_show_components(self._showverts)
##             self.check_components.set_active(0)
## #             self._flip_markers()
##         if event.key == '-':
##             self.update_show_components(self._showedges)
##             self.check_components.set_active(1)
## 
##         if event.key == 'a':
##             self.update_show_components(self._showann)
##             self.check_components.set_active(2)
#
#
#        self.canvas.draw()


###################################################################

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from intuitionistic_fuzzy_set import *
    from universal_set import UniversalSet
    from ifs_2Dplot import *
    # from ifs_operators_topo import *
    
    

#     fig, ax = plt.subplots()

    universe = UniversalSet(set(range(20)))



    fig = plt.figure()
    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    


    ifs01 = IFS.random(universe, 1, randseed=1)

    indices, mus, nus, pis = ifs01.elements_split()
    
    print('mus and nus: ')
    print(mus)
    print(nus)
    
    ax = plt.subplot2grid((4,6), (0,0), rowspan=3, colspan=3)
    ax_01, line2d1_01 = plot_triangular_(ax,
                                    mus, nus, ifs01.get_range(), bins=10,
                                    rotation={'x':45, 'y':0},
                                    alpha=0.3)
    ax_01.set_ylabel(r'$\nu$', fontsize=20)
    ax_01.set_xlabel(r'$\mu$', fontsize=20)
    
    line2d1_01.set_linestyle(' ')
    line2d1_01.set_markersize(15)
    line2d1_01.set_markerfacecolor('b')
    line2d1_01.set_color('b')
#     line2d1_01.set_marker(marker=r'$\odot$')
    line2d1_01.set_marker(marker=r'o')    
    line2d1_01.set_zorder(2)
 
 ########
#     ax_01, line2d1_02 = plot_triangular_(ax,
#                                     mus, nus, ifs01.get_range(), bins=10,
#                                     rotation={'x':45, 'y':0},
#                                     alpha=0.3)
#     ax_01.set_ylabel(r'$\nu$', fontsize=20)
#     ax_01.set_xlabel(r'$\mu$', fontsize=20)
#     
#     line2d1_02.set_linestyle(' ')
#     line2d1_02.set_markersize(15)
#     line2d1_02.set_markerfacecolor('g')
#     line2d1_02.set_color('g')
# #     line2d1_01.set_marker(marker=r'$\odot$')
#     line2d1_02.set_marker(marker=r'v')    
#     line2d1_02.set_zorder(2)
#  
 
 
 ###########
 
# 
#
    ifs02 = IFS.random(universe, 1, randseed=3)
    indices, mus, nus, pis = ifs02.elements_split()
#
#    ax_02 = plt.subplot2grid((4,6), (0,3), rowspan=3, colspan=3)

    ax_01, line2d2_01 = plot_triangular_(ax_01,
                                    mus, nus, ifs02.get_range(), bins=10,
                                    rotation={'x':45, 'y':0},
                                    alpha=0.3)
# 
#    ax02.get_yaxis().tick_right()
#    ax02.get_yaxis().set_label_position("right")
#    ax02.set_ylabel(r'$\nu$', fontsize=20)
#    ax02.set_xlabel(r'$\mu$', fontsize=20)
# 
#    line2d2_01.set_linestyle(' ')
#    line2d2_01.set_markersize(15)
#    line2d2_01.set_markerfacecolor('g')
#    line2d2_01.set_color('g')
#    line2d2_01.set_marker(marker=r'v')

########################

    from widgets_basic import WidgetsSimple

    widgets = WidgetsSimple(None)
    
    json_path = '/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/'

#    axlines = {ax_01:[PropertiesIFS(label='ifs01_ax01', holder=line2d1_01,
#                                        labels_size=15) #,
#                        ],
#               ax02:[PropertiesIFS(label='ifs01_ax02', holder=line2d2_01,
#                                       labels_size=15) #,
#                        ]
#               }
#
#    
#    p = TriangularInteractorBasic(ax_01, ax02, axlines, widgets)

    prop02 = PropertiesIFSInteractive(
                              axes = ax_01,
                             holder=line2d1_01,
                             label='ifs02',
                             labels_size=15)
    prop02.init_default(ax_01) 
    prop02.connect()


    prop_interactive01 = PropertiesIFSInteractive(
                             axes = ax_01,
                             holder=line2d1_01,
                             companions=[prop02],
                             label='ifs01',
                             labels_size=15)
    prop_interactive01.init_default(ax_01)
    
    
    prop_interactive01.connect()
    
#     p = TriangularInteractor(ax_01, line2d_01)

#     json_path = '/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/'    
#     json_prop_name = 'property01.json'
#     prop01 = PropertiesIFS.from_json(json_path + json_prop_name, 
#                                      ax, 
#                                      bins=10, 
#                                      rotation={'x':45, 'y':0})
    
    plt.show()


#    json_path = '/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/'
#    json_prop_name = 'property01.json'
#    axlines[ax_01][0].save_to_json(json_path + json_prop_name,
#                                   json_path + 'topo_const_config.json')
    
    print('Finish and save...')
