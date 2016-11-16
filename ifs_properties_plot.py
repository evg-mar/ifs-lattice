# import numpy as np
# from matplotlib.lines import Line2D
# from matplotlib.artist import Artist

# from ifs_operators_plot import *

# from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
import abc

def annotate_points_draw(ax_, line2d_):
    linepoints = zip(*line2d_.get_data())
    for idx, pt in enumerate(linepoints):
        artist_ann = ax_.annotate(str(idx), pt)
        ax_.draw_artist(artist_ann)


class PropertiesBasic(object):

    __metaclass__  = abc.ABCMeta

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
        self.holder.set_animated(True)

        self.create_annotations(ax)
        self.set_visible_annotations(True)
        self.set_animated_annotations(True)


    def create_annotations(self, ax):
        data = self.get_data()
#         data = list(zip(*self.get_data()))
        self.annotations = [ax.annotate(str(idx), pt, fontsize=10, zorder=10) 
                           for idx, pt in enumerate(data) ]

    def set_visible_annotations(self, value=True):
        for a in self.annotations:
            a.set_visible(value)

    def set_animated_annotations(self, value=True):
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

  
class PropertiesPath(PropertiesBasic):
    
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
    


class PropertiesIFS(PropertiesBasic):
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
                                  color='r',
                                  animated=True)
        
        self.beta2dline, = ax.plot([0.0, alpha, 1 - beta],
                                  [beta]*3,
                                  color='g',
                                  animated=True)



        self.update_const(ax, alpha, beta)

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

    def update_topo_const(self, ax, alpha, beta):
        self.topo_const.update_const(ax, alpha, beta)

    def draw_holder_annotations(self, ax):
        super(PropertiesIFSTopo, self).draw_holder_annotations(ax)
        self.topo_const.draw_topo_object(ax)  

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
