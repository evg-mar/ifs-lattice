import numpy as np
from matplotlib.lines import Line2D
from matplotlib.artist import Artist

from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

import copy

def annotate_points_draw(ax_, line2d_):
    linepoints = zip(*line2d_.get_data())
    for idx, pt in enumerate(linepoints):
        artist_ann = ax_.annotate(str(idx), pt)
        ax_.draw_artist(artist_ann)


class PlotPropertiesIFS(object):
    def __init__(self, ifsname=None,
                       line=None,
                       annotations=None,
                       radius=5,
                       alpha_marker=0.5, 
                       labels_size=12, 
                       show_ifs=False, show_edges=False, show_ann=False):
        self.ifsname = ifsname
        self.line = line
        self.annotations = annotations
        
        self.radius = radius  # radius of the circles/markers -> for Slider
        self.alpha_marker = alpha_marker
        self.labels_size = labels_size# fontsize of the annotation -> for Slider
        
        self.show_ifs = show_ifs
        self.show_edges = show_edges
        self.show_ann = show_ann 


class TriangularInteractor(object):
    """
    A line editor.

    Key-bindings

      't' toggle vertex markers on and off.  When vertex markers are on,
          you can move them, delete them

      'd' delete the vertex under point

      'i' insert a vertex at point.  You must be within epsilon of the
          line connecting two existing vertices

    """


    def __init__(self, ax, ifs_line2d, ax02=None, ifs_line2d_02=None, epsilon=0.02,
                 show_ifs=True, show_edges=True, show_ann=True):



        self._showverts = show_ifs
        self._showedges = show_edges
        self._showann = show_ann
        self._epsilon = epsilon # max pixel distance to count as a vertex hit
        
        
#         self.ax02 = ax02
#         self.line2 = ifs_line2d_02
#         self.line2.set_animated(True)
#         self.ax02.add_artist(self.line2)
        
        
        self.ax01 = ax
        canvas = self.ax01.figure.canvas        
        
#         print(ifs_line2d)
        self.line = ifs_line2d
        
        
#         self.line = Line2D(*mus_nus,
#                            marker='o', markerfacecolor='r',
#                            linestyle=' ', animated=True)
        self.line.set_animated(True)
        linepoints = list(zip(*self.line.get_data())) 
        
        self.marker_ann = [self.ax01.annotate(str(idx), pt, fontsize=20) 
                           for idx, pt in enumerate(linepoints) ]

        for a in self.marker_ann:
            a.set_visible(self._showann)
#             a.set_animated(True)

        self.line.set_linestyle('-' if self._showedges else ' ')

#         cid = self.poly.add_callback(self.poly_changed)
        self._ind = None  # the active vert
        self._released_pos = (0,0)

        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('key_press_event', self.key_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        self.canvas = canvas

           
        axcolor = 'lightgoldenrodyellow'
        '''
        rax = plt.axes([0.75, 0.7, 0.15, 0.15], axisbg=axcolor)
        radio = RadioButtons(rax, ('2 Hz', '4 Hz', '8 Hz'))
        '''
        radius_slax = plt.axes([0.05, 0.05, 0.1, 0.015], axisbg=axcolor)
        
        self.sl_radius = Slider(radius_slax, ' ', 
                                10, 100, valinit=self.line.get_markersize())
        self.sl_radius.label = radius_slax.text(0.02, 1.5, 
                             label='Radius marker',
                             s='radius: %.f-%.f' %(10,100), 
                             transform=radius_slax.transAxes,
                             verticalalignment='center',
                             horizontalalignment='left')
        
        self.sl_radius.on_changed(self.update_radius)
             
        rax = plt.axes([0.2, 0.05, 0.15, 0.10], axisbg=axcolor)
        self.check_components = CheckButtons(rax, 
                        ('markers', 'edges', 'labels'),
                        (self._showverts, self._showedges, self._showann))
        self.check_components.on_clicked(self.update_show_components)

    def update_show_components(self, label):
        if label == 'markers':
            self._flip_markers()
        elif label == 'edges':
            self._flip_edges()
        elif label == 'labels':
            self._flip_labels()
        self.canvas.draw()



    def update_radius(self, val):
        value = self.sl_radius.val
        self.line.set_markersize(val)
        self.canvas.draw()
    

    def draw_callback(self, event):
#         print(event)
        self.background = self.canvas.copy_from_bbox(self.ax01.bbox)
        #self.ax01.draw_artist(self.poly)
#         map(lambda ann: self.ax01.draw_artist(ann), self.marker_ann)
        for ann in self.marker_ann:
            self.ax01.draw_artist(ann)
#         self.ax01.draw_artist(self.ann)
        self.ax01.draw_artist(self.line)
        
#         self.ax02.draw_artist(self.line2)
        
        self.canvas.blit(self.ax01.bbox)
        
#         self.canvas.draw()
        

    def line_changes(self, line):
        '''
        This method is called whenever the line object is called
        '''
        pass

    def poly_changed(self, poly):
        'this method is called whenever the polygon object is called'
        # only copy the artist props to the line (except visibility)
        vis = self.line.get_visible()
        Artist.update_from(self.line, poly)
        self.line.set_visible(vis)  # don't use the poly visibility state
#         self.line.set_linestyle(' ')

    def get_ind_under_point(self, event):
        'get the index of the vertex under point if within epsilon tolerance'

        # display coords
        xy = np.asarray(self.line.get_data())
        x, y = xy[0], xy[1]
#         print(x)
#         print(y)
#         print(event.x, event.y)
#         print(self.ax01.transData.inverted().transform((event.x, event.y)))
#         print(event.xdata, event.ydata)
#         xyt = self.poly.get_transform().transform(xy)
#         xyt = self.line.get_transform().transform(xy)
#         xt, yt = xyt[:, 0], xyt[:, 1]
#         print(xt)
#         print(yt)
        d = np.sqrt((x - event.xdata)**2 + (y - event.ydata)**2)
        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
        ind = indseq[0]
        
        ind = None if (d[ind] >= self._epsilon) else ind
        return ind

    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        if not self._showverts:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self._ind = self.get_ind_under_point(event)

    def _return_button_release(self, event):
        return (not self._showverts or event.button != 1)


    def button_release_callback(self, event):
        'whenever a mouse button is released'
        if self._return_button_release(event):
            return
        
#         self.ann.xy = self._released_pos
#         self.ann.xytext = self._released_pos
#         self.ann.xyann = self._released_pos
#         
        self.canvas.draw()
        self._ind = None

    
    def _flip_edges(self):
        self._showedges = not self._showedges
        if self._showedges:
            self.line.set_linestyle('-')
#                 self._showverts = True
#                 self.line.set_visible(True)
        else:
            self.line.set_linestyle(' ')


    def _flip_markers(self):
        self._showverts = not self._showverts
        self.line.set_visible(self._showverts)
        if not self._showverts:
#                 self._showedges = False
            self._ind = None

    def _flip_labels(self):
        self._showann = not self._showann
        for ann in  self.marker_ann:
            ann.set_visible(self._showann)


    def key_press_callback(self, event):
        'whenever a key is pressed'
        print('## key press callback')
        print(type(event.inaxes))
        print(event.inaxes)
        print(event.xdata, event.ydata)
        print(event.x, event.y)
        print(event)
        
        if not event.inaxes:
            return

        if event.key == 't':
            self.update_show_components(self._showverts)
            self.check_components.set_active(0)
#             self._flip_markers()
        if event.key == '-':
            self.update_show_components(self._showedges)
            self.check_components.set_active(1)

        if event.key == 'a':
            self.update_show_components(self._showann)
            self.check_components.set_active(2)

#         elif event.key == 'd':
#             ind = self.get_ind_under_point(event)
#             if ind is not None:
#                 self.poly.xy = [tup for i, tup in enumerate(self.poly.xy) if i != ind]
#                 self.line.set_data(zip(*self.poly.xy))
#         elif event.key == 'i':
#             xys = self.poly.get_transform().transform(self.poly.xy)
#             p = event.x, event.y  # display coords
#             for i in range(len(xys) - 1):
#                 s0 = xys[i]
#                 s1 = xys[i + 1]
#                 d = dist_point_to_segment(p, s0, s1)
#                 if d <= self._epsilon:
#                     self.poly.xy = np.array(
#                         list(self.poly.xy[:i]) +
#                         [(event.xdata, event.ydata)] +
#                         list(self.poly.xy[i:]))
#                     self.line.set_data(zip(*self.poly.xy))
#                     break
        self.canvas.draw()


    def motion_notify_callback(self, event):
        'on mouse movement'
        if not self._showverts:
            return
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        
#         print('##')
#         print(type(event.inaxes))
#         print(event.inaxes)
#         print(event.xdata, event.ydata)
#         print(event.x, event.y)
#         print(event)

        # The drop & drag point should stay
        # within the triangular area
        x = min(max(0.0, event.xdata), 1.0) 
        y = min(max(0.0, event.ydata), 1.0) 

        xy_data = list(zip(*self.line.get_data()))

        
        if x + y >= 1.0:
            self._released_pos = ((x-y+1)/2, (y-x+1)/2)
        else:
            self._released_pos = (x,y)
            
        xy_data[self._ind] = self._released_pos

        self.line.set_data(zip(*xy_data))     

#         self.ann.xy = self._released_pos
#         self.ann.xytext = self._released_pos
#         self.ann.xyann = self._released_pos
        
#         self.marker_ann[self._ind].xytext =  new_pos
        ann = self.marker_ann[self._ind]
        ann.xyann =  self._released_pos
        ann.xy = ann.xyann
        ann.xytext = ann.xyann

        self.canvas.restore_region(self.background)

#         for a in self.marker_ann:
#             self.ax01.draw_artist(a)
        self.ax01.draw_artist(ann)
        self.ax01.draw_artist(self.line)
        
#         self.ax02.draw_artist(ann)
#         self.ax02.draw_artist(self.line)

#         self.canvas.blit(self.ax02.bbox)
        
        self.canvas.blit(self.ax01.bbox)

#         self.canvas.draw()


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
    


    ifs01 = IFS.random(universe, 1, randseed=2)

    indices, mus, nus, pis = ifs01.elements_split()
    
    ax = plt.subplot2grid((4,6), (0,0), rowspan=3, colspan=3)
    ax_01, line2d_01 = plot_triangular_(ax,
                                    mus, nus, ifs01.get_range(), bins=19)
    line2d_01.set_markersize(20)
    line2d_01.set_markerfacecolor('r')
    line2d_01.set_marker(marker=r'$\odot$')

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
 
#     ax02 = plt.subplot2grid((4,6), (0,3), rowspan=3, colspan=3)
#     
#     axx, line2d_02 = plot_triangular_(ax02,
#                                     mus, nus, ifs02.get_range(), bins=19)
#     line2d_01.set_markersize(20)
#     line2d_01.set_markerfacecolor('r')
#     line2d_01.set_marker(marker=r'$\odot$')


    
    print(fig.axes)
    
#     p = TriangularInteractor(ax_01, line2d_01, ax02, line2d_02)
    
    p = TriangularInteractor(ax_01, line2d_01)
    
    plt.show()
    
    a =10
