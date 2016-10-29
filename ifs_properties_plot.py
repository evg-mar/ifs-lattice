# import numpy as np
# from matplotlib.lines import Line2D
# from matplotlib.artist import Artist

# from ifs_operators_plot import *

# from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

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

    def draw_line_annotations(self, ax):
        self.draw_annotations(ax)
        if self.line.get_visible():
            ax.draw_artist(self.line)
