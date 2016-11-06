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


    def init_default(self, ax):
        self.holder.set_visible(True)
        self.holder.set_animated(True)

        self.create_annotations(ax)
        self.set_visible_annotations(True)
        self.set_animated_annotations(True)


    def create_annotations(self, ax):
        linepoints = list(zip(*self.get_data()))
        self.annotations = [ax.annotate(str(idx), pt, fontsize=10, zorder=10) 
                           for idx, pt in enumerate(linepoints) ]

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

    def set_fontsize_annotations(self, fontsize):
        for ann in self.annotations:
            ann.set_fontsize(fontsize)    

    def set_zorder_annotations(self, zorder):
        for ann in self.annotations:
            ann.set_zorder(zorder)

    def draw_annotations(self, ax):
        for a in self.annotations:
            if self.show_ann:
                ax.draw_artist(a)

    def draw_holder_annotations(self, ax):
        self.draw_annotations(ax)
        if self.holder.get_visible():
            ax.draw_artist(self.holder)                
#     def _flip_edges(self):
#         if self.ax_active in self.active_lines_idx.keys():
#             prop_ifs, _ = self.active_lines_idx[self.ax_active]
#             linestyle = prop_ifs.line.get_linestyle()
# #             prop_ifs.showedges = not prop_ifs.showedges
# 
#             style = '-' if linestyle in ['None', None] else ' '
#             prop_ifs.line.set_linestyle(style)
#             return prop_ifs.line.get_linestyle() 
#         # If the active axes is not ax01 or ax02
#         return None
# 
# 
#     def _flip_markers(self):
#         if self.ax_active in self.active_lines_idx.keys():
#             prop_ifs = self.active_lines_idx[self.ax_active][self.line_active__]
#             prop_ifs.line.set_visible(not prop_ifs.line.get_visible())
# 
#             if not prop_ifs.line.get_visible():
#                 self.active_lines_idx[self.ax_active][self.index_active__] = None
# 
#             return prop_ifs.line.get_visible()
#         # If the active axes is not ax01 or ax02
#         return None
# 
# 
#     def _flip_labels(self):
#         if self.ax_active in self.active_lines_idx.keys():
#             prop_ifs, _ = self.active_lines_idx[self.ax_active]       
#             prop_ifs.show_ann = not prop_ifs.show_ann
#             prop_ifs.set_visible_annotations(prop_ifs.show_ann)
#             return prop_ifs.show_ann
#         # If the active axes is not ax01 or ax02
#         return None



# 
#     @abc.abstractmethod
#     def eq(self, first, second):
  
class PropertiesPath(PropertiesBasic):
    
    def __init__(self, label=None,
                       holder=None,
                       radius=5,
                       annotations=None,
                       alpha_marker=0.5, 
                       labels_size=12,
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
                       show_ann,
                       showverts,
                       showedges,
                       showlabels)

#     @abc.abstractmethod
    def get_data(self):
#         return PropertiesBasic.get_data(self)
       return self.holder.get_offset() 

#     @abc.abstractmethod
    def set_data(self, data):
        self.holder.set_offcet(data)

    def get_color(self):
        return self.holder.get_color()
    
    def set_color(self):
        self.holder.set_color()


class PropertiesIFS(PropertiesBasic):
    def __init__(self, label=None,
                       holder=None,
                       radius=5,
                       annotations=None,
                       alpha_marker=0.5, 
                       labels_size=12,
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
                       show_ann,
                       showverts,
                       showedges,
                       showlabels)


#     @abc.abstractmethod
    def get_data(self):
#         return PropertiesBasic.get_data(self)
       return self.holder.get_data() 

#     @abc.abstractmethod
    def set_data(self, mus, nus):
        self.holder.set_data(mus, nus)

    def get_color(self):
        return self.holder.get_color()
    
    def set_color(self):
        self.holder.set_color()
