import numpy as np
from matplotlib.lines import Line2D
from matplotlib.artist import Artist

from ifs_operators_plot import *

from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

import copy

def annotate_points_draw(ax_, line2d_):
    linepoints = zip(*line2d_.get_data())
    for idx, pt in enumerate(linepoints):
        artist_ann = ax_.annotate(str(idx), pt)
        ax_.draw_artist(artist_ann)


class PropertiesIFS(object):
    def __init__(self, label=None,
                       line=None,
                       radius=5,
                       annotations=None,
                       alpha_marker=0.5, 
                       labels_size=12,
                       show_ann=True,
                       showverts=True,
                       showedges=False,
                       showlabels=False):
        self.label = label
        self.line = line
        self.annotations = annotations
        self.radius = radius
        self.alpha_marker = alpha_marker 
        self.labels_size = labels_size

        self.show_ann = show_ann
        
        self.showverts = self.line.get_visible() if showverts is None else showverts 
        self.showedges = showedges
        self.showlabels = showlabels

    def init_default(self, ax):
        self.line.set_visible(True)
        self.line.set_animated(True)

        self.create_annotations(ax)
        self.set_visible_annotations(True)
        self.set_animated_annotations(True)

    def create_annotations(self, ax):
        linepoints = list(zip(*self.line.get_data()))
        self.annotations = [ax.annotate(str(idx), pt, fontsize=10) 
                           for idx, pt in enumerate(linepoints) ]

    def set_visible_annotations(self, value=True):
        for a in self.annotations:
            a.set_visible(value)

    def set_animated_annotations(self, value=True):
        for a in self.annotations:
            a.set_animated(value)

    def draw_annotations(self, ax):
        for a in self.annotations:
            if self.show_ann:
                ax.draw_artist(a)

    def draw_line_annotations(self, ax):
        self.draw_annotations(ax)
        if self.line.get_visible():
            ax.draw_artist(self.line)


class TriangularInteractor(object):
    """
    A line editor.

    Key-bindings

      't' toggle vertex markers on and off.  When vertex markers are on,
          you can move them, delete them


    """
    # labels for the active line and the corresponding
    # active index in that line
    line_active__  = 0
    index_active__ = 1

    def __init__(self, ax01, ax02, axlines,
                       epsilon=0.02,
                       show_ifs=True, show_edges=True, show_ann=True):

        self._showverts = show_ifs
        self._showedges = show_edges
        self._showann = show_ann
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
       
        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('key_press_event', self.key_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        self.canvas = canvas

        self.recreate_widgets()


    def colorfunc(self, label):
        idx = int(label)
        prop_ifs_active = self.axlines[self.ax_active][idx]
        self.active_lines_idx[self.ax_active] = [prop_ifs_active,
                                                 None]
        self.w_rad_active_ifs.activecolor = prop_ifs_active.line.get_color()
#         self._recreate_active_ifs_radiobutton()
        self._recreate_radius_slider()
        self._recreate_show_lines_check_button()
#           l.set_color(label)
        self.canvas.draw()

    @property
    def _prop_idx_active(self):
        return self.active_lines_idx.get(self.ax_active, [None,None])

    def recreate_widgets(self):
        self._recreate_active_ifs_radiobutton()
        self._recreate_radius_slider()
        self._recreate_show_lines_check_button()

    def _recreate_radius_slider(self):

        '''
        rax = plt.axes([0.75, 0.7, 0.15, 0.15], axisbg=axcolor)
        radio = RadioButtons(rax, ('2 Hz', '4 Hz', '8 Hz'))
        '''
        if self.ax_active not in self.active_lines_idx.keys():
            return None
        
        axcolor = 'lightgoldenrodyellow'        
        if hasattr(self, 'radius_slax'):
            self.radius_slax.cla()
        self.radius_slax = plt.axes([0.05, 0.05, 0.1, 0.015], axisbg=axcolor)
        
        self.w_sl_radius = Slider(self.radius_slax, ' ', 10, 100,
                        valinit=self._prop_idx_active[self.line_active__].line\
                                                        .get_markersize())
        self.w_sl_radius.label = self.radius_slax.text(0.02, 1.5, 
                             label='Radius marker',
                             s='radius: %.f-%.f' %(10,100), 
                             transform=self.radius_slax.transAxes,
                             verticalalignment='center',
                             horizontalalignment='left')
        
        self.w_sl_radius.on_changed(self.update_radius)
        return self.w_sl_radius

    def _recreate_show_lines_check_button(self):
        if self.ax_active not in self.active_lines_idx.keys():
            return None

        axcolor = 'lightgoldenrodyellow'
        if hasattr(self, 'rax_showlines'):
            self.rax_showlines.cla()
        self.rax_showlines = plt.axes([0.2, 0.05, 0.15, 0.10], axisbg=axcolor)
        prop_ifs = self._prop_idx_active[self.line_active__]
        visible = prop_ifs.line.get_visible()
        linestyle = prop_ifs.line.get_linestyle()
        print(linestyle is not None)
        print(linestyle)
        
        self.w_check_components = CheckButtons(self.rax_showlines, 
                        ('markers', 'edges', 'labels'),
                        (visible, linestyle not in ['None', None], prop_ifs.show_ann))
        self.w_check_components.on_clicked(self.update_show_components)
        return self.w_check_components

    def _recreate_active_ifs_radiobutton(self):
        if self.ax_active not in self.active_lines_idx.keys():
            return None

        axcolor = 'lightgoldenrodyellow'
        if hasattr(self, 'rax_activeifs'):
            self.rax_activeifs.cla()
        self.rax_activeifs = plt.axes([0.37, 0.05, 0.15, 0.07], axisbg=axcolor)

        self.colors_ifs = { }
        for ax, properties in self.axlines.items():
            colors_map = {i: prop.line.get_color() \
                                for i, prop in enumerate(properties)}
            self.colors_ifs[ax] = colors_map 
 
        prop_ifs = self.active_lines_idx[self.ax_active][self.line_active__]
        idx = self.axlines[self.ax_active].index(prop_ifs)
        activecolor = prop_ifs.line.get_color()
        self.w_rad_active_ifs = \
                RadioButtons(self.rax_activeifs,
                             sorted(self.colors_ifs[self.ax_active].keys()),
                             active=idx,
                             activecolor=activecolor)
        self.w_rad_active_ifs.on_clicked(self.colorfunc)
        return self.w_rad_active_ifs

    def update_show_components(self, label):
        if label == 'markers':
            self._flip_markers()
        elif label == 'edges':
            self._flip_edges()
        elif label == 'labels':
            self._flip_labels()
        self.canvas.draw()


    def update_radius(self, val=None):
        value = self.sl_radius.val if (val is None) else val
        self._prop_idx_active[self.line_active__].line.set_markersize(value)
        self.canvas.draw()
    

    def draw_callback(self, event):
#         print(vars(event))
#        
                    #self.ax01.draw_artist(self.poly)
#         map(lambda ann: self.ax01.draw_artist(ann), self.marker_ann)

        for prop_ifs in self.axlines[self.ax01]:
            prop_ifs.draw_line_annotations(self.ax01)
            
        for prop_ifs in self.axlines[self.ax02]:
            prop_ifs.draw_line_annotations(self.ax02)

# 
#         for ann in self.marker_ann:
#             self.ax01.draw_artist(ann)
# #         self.ax01.draw_artist(self.ann)
#         self.ax01.draw_artist(self.line1_01)
#         
#         self.ax02.draw_artist(self.line2)
#         
#         self.canvas.blit(self.ax02.bbox)
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
                    
            if not prop_ifs.line.get_visible():
                return
            if idx_act is None:
                return

            # The drop & drag point should stay
            # within the triangular area

            xdata = min(max(0.0, event.xdata), 1.0) 
            ydata = min(max(0.0, event.ydata), 1.0) 

            self.update_line_annotation(prop_ifs, idx_act, xdata, ydata)
            self.canvas.restore_region(self.background)

            prop_ifs.draw_line_annotations(self.ax_active)

        self.canvas.blit(self.ax_active.bbox)


    def update_line_annotation(self, prop_ifs, idx_act, xdata, ydata):
        
        if xdata + ydata >= 1.0:
            pos = ((xdata-ydata+1)/2, (ydata-xdata+1)/2)
        else:
            pos = (xdata,ydata)
            
        line_xy = list(zip(*prop_ifs.line.get_data()))    
        line_xy[idx_act] = pos

        prop_ifs.line.set_data(zip(*line_xy))     
        
        
        if prop_ifs.show_ann:
            annotation = prop_ifs.annotations[idx_act]
            annotation.xyann =  pos
            annotation.xy = pos
            annotation.xytext = pos


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

    def get_ind_under_point(self, xdata, ydata, line):
        'get the index of the vertex under point if within epsilon tolerance'

        # display coords
#         print(event.inaxes)
        xy = np.asarray(line.get_data())
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


    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        print('button_pres - event in axis')
        print(event.inaxes)

        if event.inaxes is None:
            return
        if event.button != 1:
            return

        if event.inaxes in self.active_lines_idx.keys():
            self.ax_active = event.inaxes

            self.recreate_widgets()
#             self.refresh_widgets()

            prop_ifs, _ = self.active_lines_idx[self.ax_active]

            if not prop_ifs.line.get_visible():
                return

            idx_active = self.get_ind_under_point(event.xdata,
                                                  event.ydata,
                                                  prop_ifs.line)

            self.active_lines_idx[self.ax_active][self.index_active__] =\
                                                                 idx_active

    def button_release_callback(self, event):
        'whenever a mouse button is released'

        if event.button != 1:
            return

        if self.ax_active in self.active_lines_idx.keys():
            prop_ifs, idx_act = self.active_lines_idx[self.ax_active]
            
            if not prop_ifs.line.get_visible():
                return
        
#         self.ann.xy = self._released_pos
#         self.ann.xytext = self._released_pos
#         self.ann.xyann = self._released_pos
#         
            self.active_lines_idx[self.ax_active][self.index_active__] = None

        self.canvas.draw()


    def _flip_edges(self):
        if self.ax_active in self.active_lines_idx.keys():
            prop_ifs, _ = self.active_lines_idx[self.ax_active]
            linestyle = prop_ifs.line.get_linestyle()
#             prop_ifs.showedges = not prop_ifs.showedges

            style = '-' if linestyle in ['None', None] else ' '
            prop_ifs.line.set_linestyle(style)
            return prop_ifs.line.get_linestyle() 
        # If the active axes is not ax01 or ax02
        return None


    def _flip_markers(self):
        if self.ax_active in self.active_lines_idx.keys():
            prop_ifs = self.active_lines_idx[self.ax_active][self.line_active__]
#             prop_ifs.showverts = not prop_ifs.showverts
            prop_ifs.line.set_visible(not prop_ifs.line.get_visible())

#             prop_ifs.line.set_visible(prop_ifs.showverts)
            if not prop_ifs.line.get_visible():
                self.active_lines_idx[self.ax_active][self.index_active__] = None

            return prop_ifs.line.get_visible()
        # If the active axes is not ax01 or ax02
        return None


    def _flip_labels(self):
        if self.ax_active in self.active_lines_idx.keys():
            prop_ifs, _ = self.active_lines_idx[self.ax_active]       
            prop_ifs.show_ann = not prop_ifs.show_ann
            prop_ifs.set_visible_annotations(prop_ifs.show_ann)
            return prop_ifs.show_ann
        # If the active axes is not ax01 or ax02
        return None


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



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from intuitionistic_fuzzy_set import *
    from universal_set import UniversalSet
    from ifs_2Dplot import *
    from ifs_operators_topo import *
    
    

#     fig, ax = plt.subplots()

    universe = UniversalSet(set(range(10)))



    fig = plt.figure()
    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    


    ifs01 = IFS.random(universe, 1, randseed=1)

    indices, mus, nus, pis = ifs01.elements_split()
    
    ax = plt.subplot2grid((4,6), (0,0), rowspan=3, colspan=3)
    ax_01, line2d1_01 = plot_triangular_(ax,
                                    mus, nus, ifs01.get_range(), bins=19,
                                    rotation={'x':45, 'y':0})

    line2d1_01.set_linestyle(' ')
    line2d1_01.set_markersize(20)
    line2d1_01.set_markerfacecolor('r')
    line2d1_01.set_color('r')
    line2d1_01.set_marker(marker=r'$\odot$')



    ifs01 = IFS.random(universe, 1, randseed=2)

    indices, mus, nus, pis = ifs01.elements_split()

    colors={'mu':'b', 'nu':'g', 'elem':'r'}
    ax_01, line2d1_02 = plot_triangular_(ax,
                                    mus, nus,
                                    ifs01.get_range(),
                                    colors=colors,
                                    bins=19,
                                    rotation={'x':45, 'y':0})

    line2d1_02.set_linestyle(' ')
    line2d1_02.set_markersize(5)
    line2d1_02.set_markerfacecolor('g')
    line2d1_02.set_color('g')
    line2d1_02.set_marker(marker=r'o')


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
    

     
    _, line2d2_02 = plot_triangular_(ax02,
                                    mus, nus, ifs02.get_range(), bins=19,
                                    rotation={'x':45, 'y':0})

    ax02.get_yaxis().tick_right()
    ax02.set_ylabel('')

    line2d2_02.set_linestyle('-')
    line2d2_02.set_markersize(5)
    line2d2_02.set_markerfacecolor('c')
    line2d2_02.set_color('c')
    line2d2_02.set_marker(marker=r'o')

#     line2d_01.set_markersize(20)
#     line2d_01.set_markerfacecolor('r')
#     line2d_01.set_marker(marker=r'$\odot$')

    axlines = {ax_01:[PropertiesIFS(label='ifs01', line=line2d1_01),
                     PropertiesIFS(label='ifs02', line=line2d1_02)],
               ax02:[PropertiesIFS(label='ifs01', line=line2d2_02)]
               }

    
    p = TriangularInteractor(ax_01, ax02, axlines)
    
#     p = TriangularInteractor(ax_01, line2d_01)
    
    plt.show()
    
    a =10
