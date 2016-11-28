# import numpy as np
# from matplotlib.lines import Line2D
# from matplotlib.artist import Artist

# from ifs_operators_plot import *

# from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
import abc
import numpy as np

def annotate_points_draw(ax_, line2d_):
    linepoints = zip(*line2d_.get_data())
    for idx, pt in enumerate(linepoints):
        artist_ann = ax_.annotate(str(idx), pt)
        ax_.draw_artist(artist_ann)


class PropertiesBasic(object):

    __metaclass__  = abc.ABCMeta

    
    @abc.abstractmethod
    def get_data(self):
        return
    
    @abc.abstractmethod
    def set_data(self, data):
        return
    
    @abc.abstractclassmethod
    def get_color(self):
        return

    @abc.abstractclassmethod
    def set_color(self):
        return

    

    

class PropertiesAnnotations(PropertiesBasic):


#     def __init__(self, posetpool):
#         self.posetpool = posetpool
    def __init__(self, label=None,
                       holder=None,
                       radius=5,
                       annotations=None,
                       alpha_marker=0.5, 
                       labels_size=12,
                       hide_ifs=False,
                       show_ann=True,
                       showverts=True,
                       showedges=False,
                       showlabels=False):
        self.label = label
        self.holder = holder
        self.annotations = annotations
        self.radius = radius
        self.alpha_marker = alpha_marker 
        self.labels_size = labels_size

        self.hide_ifs = hide_ifs
        self.show_ann = show_ann
        
        self.showverts = self.holder.get_visible() if showverts is None else showverts 
        self.showedges = showedges
        self.showlabels = showlabels

    @abc.abstractclassmethod
    def get_markersize(self):
        return

    @abc.abstractclassmethod
    def set_markersize(self, size):
        return

    @abc.abstractclassmethod
    def draw_holder_annotations(self, ax):
        return

    def init_default(self, ax):
        self.holder.set_visible(True)
        self.holder.set_animated(False)

        self.create_annotations(ax)
        self.set_visible_annotations(True)
        self.set_animated_annotations(False)

    def set_animated(self, value):
        self.set_animated_annotations(value)
        self.holder.set_animated(value)

    def create_annotations(self, ax):
        data = self.get_data()
#         data = list(zip(*self.get_data()))
        self.annotations = [ax.annotate(str(idx), pt, fontsize=10, zorder=10) 
                           for idx, pt in enumerate(data) ]

    def set_visible_annotations(self, value):
        self.show_ann = value
        for a in self.annotations:
            a.set_visible(value)

    def set_animated_annotations(self, value):
        for a in self.annotations:
            a.set_animated(value)

    def set_data_annotations(self, positions):
        for ann, pos in zip(self.annotations, positions):
            ann.xyann = pos
            ann.xy = pos
            ann.xytext = pos
            
    def set_data_annotations_single(self, idx, pos):
        assert(0 <= idx < len(self.annotations))    
        ann = self.annotations[idx]
        ann.xyann = pos
        ann.xy = pos
        ann.xytext = pos       

#     @abc.abstractclassmethod
    def set_fontsize_annotations(self, fontsize):
        for ann in self.annotations:
            ann.set_fontsize(fontsize)    
#         return

    def set_zorder_annotations(self, zorder):
        for ann in self.annotations:
            ann.set_zorder(zorder)

    def draw_annotations(self, ax):
        for a in self.annotations:
            if self.show_ann:
                ax.draw_artist(a)

  
class PropertiesPath(PropertiesAnnotations):
    
    def __init__(self, label=None,
                       holder=None,
                       radius=5,
                       annotations=None,
                       alpha_marker=0.5, 
                       labels_size=12,
                       hide_ifs=False,
                       show_ann=True,
                       showverts=True,
                       showedges=False,
                       showlabels=False):
        
        super(PropertiesPath, self).__init__(label,
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

#     @abc.abstractmethod
    def get_data(self):
#         return PropertiesBasic.get_data(self)
       return self.holder.get_offsets() 

#     @abc.abstractmethod
    def set_data(self, data):
        self.holder.set_offsets(data)

    def get_color(self):
        return self.holder._facecolors_original
    
    def set_color(self, color):
        self.holder.set_facecolor(color)

    def get_markersize(self):
        return self.holder._sizes

    def set_markersize(self,size):
        self.holder.set_sizes(size)

    def draw_holder_annotations(self, ax):
        self.draw_annotations(ax)
        if self.holder.get_visible():
#              ax.figure.canvas.renderer.draw_path_collection(self.holder)
            self.holder.draw(ax.figure.canvas.renderer)
#             ax.draw_artist(self.holder)                
    


class PropertiesIFS(PropertiesAnnotations):
    epsilon = 0.02
    def __init__(self, label=None,
                       holder=None,
                       radius=5,
                       annotations=None,
                       alpha_marker=0.5, 
                       labels_size=12,
                       hide_ifs=False,
                       show_ann=True,
                       showverts=True,
                       showedges=False,
                       showlabels=False):
        
        super(PropertiesIFS, self).__init__(label,
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


#     @abc.abstractmethod
    def get_data(self):
#         return PropertiesBasic.get_data(self)
#        return self.holder.get_data() 
       return list(zip(*self.holder.get_data()))

#     @abc.abstractmethod
    def set_data(self, mus, nus):
        self.holder.set_data(mus, nus)

    def get_data_pair(self):
        return self.holder.get_data()

    def get_color(self):
        return self.holder.get_color()
    
    def set_color(self):
        self.holder.set_color()


    def get_markersize(self):
        return self.holder.get_markersize()

    def set_markersize(self,size):
        self.holder.set_markersize(size)

    def draw_holder_annotations(self, ax):
        self.draw_annotations(ax)
        if self.holder.get_visible():
#             ax.figure.canvas.renderer.draw_path_collection(self.holder)
#             self.holder.draw(ax.figure.canvas.renderer)
            ax.draw_artist(self.holder)



##############################################################
#######
##############################################################
import ifs_operators_plot as oper  
import matplotlib.pyplot as plt 

class TopoConst(object):
    def __init__(self, ax, alpha, beta, gamma):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        self.alpha2dline, = ax.plot([alpha]*3,
                                  [0.0, beta,  1-alpha],
                                  color='r')
        
        self.beta2dline, = ax.plot([0.0, alpha, 1 - beta],
                                  [beta]*3,
                                  color='g')

#         self.set_animated(True)

#         self.update_const(ax, alpha, beta)

    def set_animated(self,value):
        self.alpha2dline.set_animated(value)
        self.beta2dline.set_animated(value)
        
    def update_const(self, ax, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        
        self.alpha2dline.set_data([alpha]*3,
                                  [0.0, beta,  1-alpha])
        self.beta2dline.set_data([0.0, alpha, 1 - beta],
                                  [beta]*3)

    def draw_topo_object(self, ax):
        ax.draw_artist(self.alpha2dline)
        ax.draw_artist(self.beta2dline)
        
    def set_visible(self, flag):
        self.alpha2dline.set_visible(flag)
        self.beta2dline.set_visible(flag)
    
    def get_visible(self):
        return self.alpha2dline.get_visible() and \
               self.beta2dline.get_visible()



class PropertiesIFSTopo(PropertiesIFS):
    def __init__(self, label=None,
                       holder=None,
                       topo_const=None,
                       radius=5,
                       annotations=None,
                       alpha_marker=0.5, 
                       labels_size=12,
                       show_ann=True,
                       hide_ifs=False,
                       showverts=True,
                       showedges=False,
                       showlabels=False):
    
        super(PropertiesIFSTopo, self).__init__(label,
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

        self.topo_const = topo_const
        self.axes = self.holder.axes
#         self.idx_active = None


    def update_topo_const(self, ax, alpha, beta):
        self.topo_const.update_const(ax, alpha, beta)

#     def draw_holder_annotations(self, ax):
#         super(PropertiesIFSTopo, self).draw_holder_annotations(ax)
#         self.topo_const.draw_topo_object(ax)  

    def incGeneral(self):
        return oper.incGeneral(self.get_data_pair(),
                        self.topo_const.alpha,
                        self.topo_const.beta,
                        self.topo_const.gamma)

    def clGeneral(self):
        return oper.clGeneral(self.get_data_pair(),
                       self.topo_const.alpha,
                       self.topo_const.beta,
                       self.topo_const.gamma)


class PropertiesIFSTopoInteractive(PropertiesIFSTopo):
    
    def __init__(self, label=None,
                       holder=None,
                       topo_const=None,
                       radius=5,
                       annotations=None,
                       alpha_marker=0.5, 
                       labels_size=12,
                       show_ann=True,
                       hide_ifs=False,
                       showverts=True,
                       showedges=False,
                       showlabels=False):
    
        super(PropertiesIFSTopoInteractive, self).__init__(label,
                       holder,
                       topo_const,
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

        
    
    def set_animated(self, value):
        super(PropertiesIFSTopo, self).set_animated(value)
        self.topo_const.set_animated(value)

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

#         if event.inaxes == self.widgets.rax_activeifs:
#         if event.inaxes in self.active_lines_idx.keys():        
#             self.recreate_widgets()
# 
#         if event.inaxes in self.active_lines_idx.keys():
#             if self.ax_active != event.inaxes:
#                 self.ax_active = event.inaxes
#                 self.recreate_widgets()
            

#             self.refresh_widgets()
#             prop_ifs, _ = self.active_lines_idx[self.ax_active]

        if not self.holder.get_visible():
            return

        self.idx_active = self.get_ind_under_point(event.xdata,
                                              event.ydata)
        
        if self.idx_active is None:
            return
    
        canvas = self.axes.figure.canvas
        axes = self.axes
        
        if self.idx_active > -1:
            if self.show_ann:
                self.set_animated_annotations(True)
            if self.showverts:
                self.holder.set_animated(True)
        else:
            self.topo_const.set_animated(True)
            
        canvas.draw()
        
        self.background = canvas.copy_from_bbox(self.axes.figure.bbox)

        # now redraw just the rectangle
        if self.idx_active > -1:
            self.draw_holder_annotations(self.axes)
        else:
            self.topo_const.draw_topo_object(self.axes)
#             
#             axes.draw_artist(self.rect_mu)
#             axes.draw_artist(self.rect_nu)
#     
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

        x = np.zeros(len(x0)+1, dtype=float)
        x[0:-1] = x0
        x[-1] = self.topo_const.alpha
        
        y = np.zeros(len(y0)+1, dtype=float)
        y[0:-1] = y0
        y[-1] = self.topo_const.beta
        
#         print(x)
#         print(y)
#         print(event.xdata, event.ydata)
#         print(event.x, event.y)
#         print(self.ax01.transData.inverted().transform((event.x, event.y)))
#         print(event.xdata, event.ydata)

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
            print('update holder & annotation')
#                self.update_holder_annotation(prop_ifs_inactive,
#                                              idx_act,
#                                              xdata, ydata)                
            self.axes.figure.canvas.restore_region(self.background)
            self.draw_holder_annotations(self.axes)
        
        elif self.idx_active == -1:
            self.update_topo_const(self.axes, xdata, ydata)
#                 prop_ifs_inactive.update_topo_const(ax_inactive,
#                                                     xdata, ydata)
            self.axes.figure.canvas.restore_region(self.background)
            self.topo_const.draw_topo_object(self.axes)        

        self.axes.figure.canvas.blit(self.axes.bbox)


    def update_holder_annotation(self, xdata, ydata):
#         print("..in update holder annotations...")
        if xdata + ydata >= 1.0:
            pos = ((xdata-ydata+1)/2, (ydata-xdata+1)/2)
        else:
            pos = (xdata,ydata)
            
        line_xy = list(zip(*self.get_data_pair()))    
        line_xy[self.idx_active] = pos
        data = list(zip(*line_xy))

        self.set_data(data[0], data[1])     
        
        
        if self.show_ann:
            print("updating the annotation...")
            self.set_data_annotations_single(self.idx_active, pos)

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
# 
#         if self.ax_active == self.ax01:
#             idx = self.axlines[self.ax_active].index(prop_ifs)
#             prop2_ifs = self.axlines[self.ax02][idx]          
#         mus, nus = self.incGeneral()
#             mus, nus = oper.incGeneral(prop_ifs.get_data_pair(),
#                                  0.6, 0.2, 0.5)

#             prop2_ifs01 = self.axlines[self.ax02][0]
#         prop2_ifs.set_data(mus,nus)
#         prop2_ifs.set_data_annotations(list(zip(mus,nus)))
        self.axes.figure.canvas.draw()
    
    
    
    