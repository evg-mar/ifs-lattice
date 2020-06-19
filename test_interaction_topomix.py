import numpy as np
import json

from matplotlib.lines import Line2D
from matplotlib.artist import Artist

#import ifs_operators_plot as oper  

#from ifs_properties_plot import PropertiesIFSTopo

from ifs_properties_topo import PropertiesIFSTopo, TopoConst

class TriangularInteractorBasic(object):
    line_active__  = 0
    index_active__ = 1

    def __init__(self, ax01, ax02, axlines, widgets,
                       epsilon=0.02):
        
        self._epsilon = epsilon # max pixel distance to count as a vertex hit



        self.axlines = axlines

        self.ax02 = ax02
        for prop_ifs in self.axlines[self.ax02]:
            prop_ifs.init_default(ax02)

        self.ax01 = ax01
        for prop_ifs in self.axlines[self.ax01]:
            prop_ifs.init_default(ax01)

        ### (line_number, active idx in that line)
        self.active_lines_idx = {self.ax01: [self.axlines[self.ax01][0], None],
                                 self.ax02: [self.axlines[self.ax02][0], None]}

        self.ax_active = self.ax01

        canvas = self.ax01.figure.canvas
       
        self.canvas = canvas
        self.mpl_connect_init()
        

        self.colors_ifs = { }
        for ax, properties in self.axlines.items():
            colors_map = {i: prop.holder.get_color() \
                                for i, prop in enumerate(properties)}
            self.colors_ifs[ax] = colors_map 

       
        self.widgets = widgets
        self.widgets.canvas = self.canvas 
        self.recreate_widgets()
        
        self.ax01.set_aspect('equal', 'datalim')
        self.ax02.set_aspect('equal', 'datalim')

    def mpl_connect_init(self):
        self.canvas.mpl_connect('draw_event',
                                self.draw_callback)
        self.canvas.mpl_connect('button_press_event',
                                self.button_press_callback)
        self.canvas.mpl_connect('key_press_event',
                                self.key_press_callback)
        self.canvas.mpl_connect('button_release_event',
                                self.button_release_callback)
        self.canvas.mpl_connect('motion_notify_event',
                                self.motion_notify_callback)


    def draw_callback(self, event):

        for prop_ifs in self.axlines[self.ax01]:
            prop_ifs.draw_holder_annotations(self.ax01)
            
        for prop_ifs in self.axlines[self.ax02]:
            prop_ifs.draw_holder_annotations(self.ax02)

        if self.ax_active is not None:
            self.canvas.blit(self.ax_active.bbox)        
            self.background = \
                self.canvas.copy_from_bbox(self.ax_active.figure.bbox)


    def motion_notify_callback(self, event):
#         print('on mouse movement')
        if event.inaxes is None:
            return
        if event.button != 1:
            return

        if event.inaxes in self.active_lines_idx.keys():
#             print('on mouse movement')
            self.ax_active = event.inaxes
            
            prop_ifs, idx_act = self.active_lines_idx[self.ax_active]
        
            if not prop_ifs.holder.get_visible():
                return
            if idx_act is None:
#                 print('idx_act %d' % -1 if idx_act is None else idx_act)
                return

            ax_inactive = self.ax01 if self.ax01!=self.ax_active else self.ax02
            prop_ifs_inactive, _ = self.active_lines_idx[ax_inactive]
                
            # The drop & drag point should stay
            # within the triangular area

            xdata = min(max(0.0, event.xdata), 1.0) 
            ydata = min(max(0.0, event.ydata), 1.0) 
#             print('on mouse movement')
            if idx_act > -1:
                self.update_holder_annotation(prop_ifs,
                                              idx_act,
                                              xdata, ydata)
#                self.update_holder_annotation(prop_ifs_inactive,
#                                              idx_act,
#                                              xdata, ydata)                
            elif idx_act == -1:
                prop_ifs.update_topo_const(#self.ax_active,
                                           xdata, ydata)
                prop_ifs_inactive.update_topo_const(#ax_inactive,
                                                    xdata, ydata)
            self.canvas.restore_region(self.background)

            prop_ifs.draw_holder_annotations(self.ax_active)

        self.canvas.blit(self.ax_active.bbox)

    @classmethod
    def update_holder_annotation(cls, prop_ifs, idx_act, xdata, ydata):
#         print("..in update holder annotations...")
        if xdata + ydata >= 1.0:
            pos = ((xdata-ydata+1)/2, (ydata-xdata+1)/2)
        else:
            pos = (xdata,ydata)
            
        line_xy = list(zip(*prop_ifs.get_data_pair()))    
        line_xy[idx_act] = pos
        data = list(zip(*line_xy))

        prop_ifs.set_data(data[0], data[1])     
        
        
        if prop_ifs.show_ann:
            prop_ifs.set_data_annotations_single(idx_act, pos)
#             annotation = prop_ifs.annotations[idx_act]
#             annotation.xyann =  pos
#             annotation.xy = pos
#             annotation.xytext = pos


    def line_changes(self, line):
        '''
        This method is called whenever the line object is called
        '''
        pass

    def poly_changed(self, poly):
        'this method is called whenever the polygon object is called'
        # only copy the artist props to the line (except visibility)
        vis = self.line1_01.get_visible()
        Artist.update_from(self.line1_01, poly)
        self.line1_01.set_visible(vis)  # don't use the poly visibility state
#         self.line.set_linestyle(' ')

    def get_ind_under_point(self, xdata, ydata, prop_ifs):
        'get the index of the vertex under point if within epsilon tolerance'

        # display coords
#         print(event.inaxes)
        xy = np.asarray(prop_ifs.get_data_pair())
        print('get the index..')
        # print(prop_ifs.get_data_pair())
        # print(xy)
        x0, y0 = xy[0], xy[1]

        x = np.zeros(len(x0)+1, dtype=float)
        x[0:-1] = x0
        x[-1] = prop_ifs.topo_const.alpha
        
        y = np.zeros(len(y0)+1, dtype=float)
        y[0:-1] = y0
        y[-1] = prop_ifs.topo_const.beta
        
#         print(x)
#         print(y)
#         print(event.xdata, event.ydata)
#         print(event.x, event.y)
#         print(self.ax01.transData.inverted().transform((event.x, event.y)))
#         print(event.xdata, event.ydata)

        d = np.sqrt((x - xdata)**2 + (y - ydata)**2)
        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
        ind = indseq[0]
        
        ind = None if (d[ind] >= self._epsilon) else ind
        ind = -1 if ind == len(x0) else ind
        return ind

    def recreate_widgets(self):
        print("in reacreate widgets...")
        self.widgets.colors_ifs = self.colors_ifs[self.ax_active]
        prop_ifs, _ = self.active_lines_idx[self.ax_active]
        idx = self.axlines[self.ax_active].index(prop_ifs)
        
        self.widgets.recreate_widgets_(#prop_ifs,
#                                       idx,
#                                       self.axlines[self.ax_active],
                                      self.active_lines_idx[self.ax_active][0])
        if prop_ifs != self.widgets.prop_ifs:
            self.active_lines_idx[self.ax_active] =[self.widgets.active_prop[0],
                                                    None]

        if not self.widgets.active_prop.holder.get_visible():
            self.active_lines_idx[self.ax_active][self.index_active__] = None

        print("active prop %s" % self.ax_active)
        print("active prop %s" % self.active_lines_idx[self.ax_active][0].label)
        print("widgets prop %s" % self.widgets.prop_ifs.label)
        print("-------------")


    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        print('button_pres - event in axis')
        print(event.inaxes)

        if event.inaxes is None:
            return
        if event.button != 1:
            return

#         if event.inaxes == self.widgets.rax_activeifs:
        if event.inaxes in self.active_lines_idx.keys():        
            self.recreate_widgets()

        if event.inaxes in self.active_lines_idx.keys():
            if self.ax_active != event.inaxes:
                self.ax_active = event.inaxes
                self.recreate_widgets()
            

#             self.refresh_widgets()
            prop_ifs, _ = self.active_lines_idx[self.ax_active]

            if not prop_ifs.holder.get_visible():
                return

            idx_active = self.get_ind_under_point(event.xdata,
                                                  event.ydata,
                                                  prop_ifs)
            print('button press callback: idx = %d' % -1 if idx_active is None else idx_active)
            self.active_lines_idx[self.ax_active][self.index_active__] =\
                                                                 idx_active


    def button_release_callback(self, event):
        'whenever a mouse button is released'

        if event.button != 1:
            return

        if self.ax_active in self.active_lines_idx.keys():
            prop_ifs, idx_act = self.active_lines_idx[self.ax_active]
            
            if not prop_ifs.holder.get_visible():
                return
#             print("active prop %s" % self.ax_active)
#             print("active prop %s" % self.active_lines_idx[self.ax_active][0].label)
            
            self.active_lines_idx[self.ax_active][self.index_active__] = None

        if self.ax_active == self.ax01:
            idx = self.axlines[self.ax_active].index(prop_ifs)
            prop2_ifs = self.axlines[self.ax02][idx]          

            mus, nus = prop_ifs.incGeneral()
#             mus, nus = oper.incGeneral(prop_ifs.get_data_pair(),
#                                  0.6, 0.2, 0.5)

#             prop2_ifs01 = self.axlines[self.ax02][0]
            prop2_ifs.set_data(mus,nus)
            prop2_ifs.set_data_annotations(list(zip(mus,nus)))


        self.canvas.draw()




    def key_press_callback(self, event):
        'whenever a key is pressed'
        print('## key press callback')
        print('nothing doing...')
        print(type(event.inaxes))
        print(event.inaxes)
        print(event.xdata, event.ydata)
        print(event.x, event.y)
        print(event)
        
#         if not event.inaxes:
#             return
# 
#         if event.key == 't':
#             self.update_show_components(self._showverts)
#             self.check_components.set_active(0)
# #             self._flip_markers()
#         if event.key == '-':
#             self.update_show_components(self._showedges)
#             self.check_components.set_active(1)
# 
#         if event.key == 'a':
#             self.update_show_components(self._showann)
#             self.check_components.set_active(2)


        self.canvas.draw()


###################################################################

if __name__ == '__main__':
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
    
    print('mus and nus: ')
    print(mus)
    print(nus)
    
    ax = plt.subplot2grid((4,6), (0,0), rowspan=3, colspan=3)
    ax_01, line2d1_01 = plot_triangular_(ax,
                                    mus, nus, ifs01.get_range(), bins=10,
                                    rotation={'x':45, 'y':0},
                                    alpha=0.3)
    print(type(line2d1_01))
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
 
 
    ifs02 = IFS.random(universe, 1, randseed=3)
    indices, mus, nus, pis = ifs02.elements_split()
#  
    ax02 = plt.subplot2grid((4,6), (0,3), rowspan=3, colspan=3)
#     
# 
#      
    _, line2d2_01 = plot_triangular_(ax02,
                                    mus, nus, ifs02.get_range(), bins=10,
                                    rotation={'x':45, 'y':0},
                                    alpha=0.3)
 
    ax02.get_yaxis().tick_right()
    ax02.get_yaxis().set_label_position("right")
    ax02.set_ylabel(r'$\nu$', fontsize=20)
    ax02.set_xlabel(r'$\mu$', fontsize=20)
 
    line2d2_01.set_linestyle(' ')
    line2d2_01.set_markersize(15)
    line2d2_01.set_markerfacecolor('g')
    line2d2_01.set_color('g')
    line2d2_01.set_marker(marker=r'v')

########################

    from widgets_basic import WidgetsSimpleTopo, WidgetsSimple

    widgets = WidgetsSimpleTopo(None)
    
    topo_c0101 = TopoConst(ax_01, 0.4, 0.3, 0.4, 0.65, label="topo_const01")
#    topo_c0102 = TopoConst(ax_01, 0.6, 0.2, 0.5)
    
    topo_c0201 = TopoConst(ax02, 0.4, 0.3, 0.4, 0.65, label="topo_const02")
    json_path = '/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/'
    json_name = 'topo_const_config.json'

    #topo_c0201.save_to_json(json_path + json_name)
    
    #topo_c0201 = TopoConst.from_json(ax=ax02, 
    #                                 json_path=json_path+json_name)
        
#     topo_c0202 = TopoConst(ax02, 0.6, 0.2, 0.5)        
    
#     prop_bar = PropertiesBar("prop_bar01", mus, nus, ax02)

    axlines = {ax_01:[PropertiesIFSTopo(label='ifs01_ax01', holder=line2d1_01,
                                        labels_size=15,
                                        topo_const=topo_c0101) #,
                      #PropertiesIFSTopo(label='ifs02_ax01', holder=line2d1_02)
                                        #topo_const_triang=topo_c0102)
                        ],
               ax02:[PropertiesIFSTopo(label='ifs01_ax02', holder=line2d2_01,
                                       labels_size=15,
                                        topo_const=topo_c0201) #,
#                      PropertiesIFSTopo(label='ifs02_ax01', holder=line2d1_02,
#                                        topo_const_triang=topo_c0102)
                        ]
               }

    
    p = TriangularInteractorBasic(ax_01, ax02, axlines, widgets)
    
#     p = TriangularInteractor(ax_01, line2d_01)

#     json_path = '/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/'    
#     json_prop_name = 'property01.json'
#     prop01 = PropertiesIFS.from_json(json_path + json_prop_name, 
#                                      ax, 
#                                      bins=10, 
#                                      rotation={'x':45, 'y':0})
    
    plt.show()


    json_path = '/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/'
    import os
    json_path = os.path.join( os.getcwd(), 'ifsholder')
    json_prop_name = 'property01.json'
    axlines[ax_01][0].save_to_json( os.path.join(json_path + json_prop_name),
                                                 os.path.join( json_path ,'topo_const_config.json')
                                    )
    
    print('Finish and save...')
