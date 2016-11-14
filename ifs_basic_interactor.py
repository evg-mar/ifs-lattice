import numpy as np
from matplotlib.lines import Line2D
from matplotlib.artist import Artist

from ifs_operators_plot import * 

from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

from ifs_properties_plot import PropertiesIFS, PropertiesPath


class TriangularInteractorBasic(object):
    line_active__  = 0
    index_active__ = 1
#     
#     slider_length__ = 0.1
#     slider_hight__  = 0.015
#     
#     button_length__ = 0.1
#     button_height__ = 0.1

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
            colors_map = {i: prop.get_color() \
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

# 
#     @property
#     def _prop_idx_active(self):
#         return self.active_lines_idx.get(self.ax_active, [None,None])



    def draw_callback(self, event):
#         print(vars(event))
#        
                    #self.ax01.draw_artist(self.poly)
#         map(lambda ann: self.ax01.draw_artist(ann), self.marker_ann)

        for prop_ifs in self.axlines[self.ax01]:
            prop_ifs.draw_holder_annotations(self.ax01)
            
        for prop_ifs in self.axlines[self.ax02]:
            prop_ifs.draw_holder_annotations(self.ax02)

        if self.ax_active is not None:
            self.canvas.blit(self.ax_active.bbox)        
            self.background = \
                self.canvas.copy_from_bbox(self.ax_active.figure.bbox)


    def motion_notify_callback(self, event):
        'on mouse movement'
        if event.inaxes is None:
            return
        if event.button != 1:
            return

        if event.inaxes in self.active_lines_idx.keys():
            self.ax_active = event.inaxes
            
            prop_ifs, idx_act = self.active_lines_idx[self.ax_active]
                    
            if not prop_ifs.holder.get_visible():
                return
            if idx_act is None:
                return

            # The drop & drag point should stay
            # within the triangular area

            xdata = min(max(0.0, event.xdata), 1.0) 
            ydata = min(max(0.0, event.ydata), 1.0) 

            self.update_holder_annotation(prop_ifs, idx_act, xdata, ydata)
            self.canvas.restore_region(self.background)

            prop_ifs.draw_holder_annotations(self.ax_active)

        self.canvas.blit(self.ax_active.bbox)


    def update_holder_annotation(self, prop_ifs, idx_act, xdata, ydata):
        
        if xdata + ydata >= 1.0:
            pos = ((xdata-ydata+1)/2, (ydata-xdata+1)/2)
        else:
            pos = (xdata,ydata)
            
        line_xy = list(zip(*prop_ifs.get_data()))    
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
        xy = np.asarray(prop_ifs.get_data())
        x, y = xy[0], xy[1]
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
        return ind

    def recreate_widgets(self):
        print("in reacreate widgets...")
        self.widgets.colors_ifs = self.colors_ifs[self.ax_active]
        prop_ifs, _ = self.active_lines_idx[self.ax_active]
        idx = self.axlines[self.ax_active].index(prop_ifs)
        
        self.widgets.recreate_widgets(#prop_ifs,
                                      idx,
                                      self.axlines[self.ax_active],
                                      self.active_lines_idx[self.ax_active])
        if prop_ifs != self.widgets.prop_ifs:
            self.active_lines_idx[self.ax_active] =[self.widgets.active_prop[0],
                                                    None]

        if not self.widgets.active_prop[0].holder.get_visible():
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

        if event.inaxes == self.widgets.rax_activeifs:
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
            prop1_ifs01 = self.axlines[self.ax01][0]
            prop1_ifs02 = self.axlines[self.ax01][1]
            
#             mus, nus = supStd(prop1_ifs01.line.get_data(),
#                               prop1_ifs02.line.get_data())
#             print(prop1_ifs01.holder.get_data())
            mus, nus = incGeneral(prop1_ifs01.holder.get_data(),
                                 0.6, 0.2, 0.5)

            prop2_ifs01 = self.axlines[self.ax02][0]
            prop2_ifs01.holder.set_data(mus,nus)
            prop2_ifs01.set_data_annotations(list(zip(mus,nus)))


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

    universe = UniversalSet(set(range(50)))



    fig = plt.figure()
    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    


    ifs01 = IFS.random(universe, 1, randseed=1)

    indices, mus, nus, pis = ifs01.elements_split()
    
    ax = plt.subplot2grid((4,6), (0,0), rowspan=3, colspan=3)
    line2d1_01 = plot_triangular_scatter(ax,
                                    mus, nus, ifs01.get_range(), bins=19,
                                    rotation={'x':45, 'y':0})

#     line2d1_01.set_linestyle(' ')
    line2d1_01.set_linestyle([None,None])    
#     line2d1_01.set_markersize(5)

    line2d1_01.set_facecolor('r')
    line2d1_01.set_edgecolor('r')
#     line2d1_01.set_marker(marker=r'$\odot$')
#     line2d1_01.set_marker(marker=r'o')    
    line2d1_01.set_zorder(15)


    ifs01 = IFS.random(universe, 1, randseed=2)

    indices, mus, nus, pis = ifs01.elements_split()

    colors={'mu':'b', 'nu':'g', 'elem':'r'}
#     plot_triangular_scatter
    line2d1_02 = plot_triangular_scatter(ax,
                                    mus, nus,
                                    ifs01.get_range(),
                                    colors=colors,
                                    bins=19,
                                    rotation={'x':45, 'y':0})

#     line2d1_02.set_linestyle(' ')
    line2d1_02.set_linestyle([None,None])
#     line2d1_02.set_markersize(5)
#     line2d1_02.set_markerfacecolor('g')
#     line2d1_02.set_color('g')
    line2d1_02.set_facecolor('r')
    line2d1_02.set_edgecolor('r')
#     line2d1_02.set_marker(marker=r'o')
    line2d1_02.set_zorder(15)


#     line2d_01.set_alpha(0.5)
#     fontsize = 12
#     linepoints = list(zip(*line2d_01.get_data())) 
#     marker_ann = [ax_01.annotate(str(idx), pt, fontsize=fontsize) 
#                            for idx, pt in enumerate(linepoints) ]
# 
#  
#     prop_ifs01 = PlotPropertiesIFS( ifsname='ifs01',
#                        line=line2d_01.copy(),
#                        annotations=marker_ann.copy(),
#                        radius=5,
#                        alpha_marker=0.5, 
#                        labels_size=12, 
#                        show_ifs=True, show_edges=True, show_ann=True)
#     
# #     
    ifs02 = IFS.random(universe, 1, randseed=3)
    indices, mus, nus, pis = ifs02.elements_split()
 
    ax02 = plt.subplot2grid((4,6), (0,3), rowspan=3, colspan=3)
    

     
    line2d2_02 = plot_triangular_scatter(ax02,
                                    mus, nus, ifs02.get_range(), bins=19,
                                    rotation={'x':45, 'y':0})

    ax02.get_yaxis().tick_right()
    ax02.set_ylabel('')

#     line2d2_02.set_linestyle('-')
    line2d2_02.set_linestyle([None,None])
#     line2d2_02.set_markersize(5)
#     line2d2_02.set_markerfacecolor('c')
#     line2d2_02.set_color('c')
#     line2d2_02.set_marker(marker=r'o')

#     line2d_01.set_markersize(20)
#     line2d_01.set_markerfacecolor('r')
#     line2d_01.set_marker(marker=r'$\odot$')
    from widgets_basic import WidgetsBasic

    widgets = WidgetsBasic(None)

    axlines = {ax:[PropertiesPath(label='ifs01_ax01', holder=line2d1_01),
                     PropertiesPath(label='ifs02_ax01', holder=line2d1_02)],
               ax02:[PropertiesPath(label='ifs01_ax02', holder=line2d2_02)]
               }

    
    p = TriangularInteractorBasic(ax, ax02, axlines, widgets)
    
#     p = TriangularInteractor(ax_01, line2d_01)
    
    plt.show()
    
    a =10
