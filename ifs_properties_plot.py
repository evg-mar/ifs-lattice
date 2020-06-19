# import numpy as np
# from matplotlib.lines import Line2D
# from matplotlib.artist import Artist

# from ifs_operators_plot import *
import abc
import numpy as np
import json
import os

from collections import OrderedDict

from ifs_2Dplot import plot_triangular_

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
        if annotations is not None:
            self.set_fontsize_annotations(self.labels_size)

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
        fontsize = self.labels_size if self.labels_size is not None else 10 
        self.annotations = [ax.annotate(str(idx),pt,fontsize=fontsize,zorder=30) 
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
        self.set_fontsize_annotations(self.labels_size)
            
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
    

import collections as col

class PropertiesIFS(PropertiesAnnotations):
    epsilon = 0.02
    def __init__(self, label=None,
                       holder=None,
                       radius=2,
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
        



    def save_to_json(self, json_path):
        data = self.holder.get_data() 

        data_lst = list(zip(data[0], data[1]))
        data = OrderedDict(list(enumerate(data_lst)))
        # data = dict(data)
        
        tmp_holder = OrderedDict([('data', data),
                                 #('data', list(zip(data[0], data[1]))),
                                 # ('radius', self.radius),
                                 ('contrast', self.holder.get_alpha()),
                                 ('labels_size', self.labels_size),
                                 ('color', self.holder.get_color()),
                                 ('marker', self.holder.get_marker()),
                                 ('marker_size', self.holder.get_markersize()),
                                 ('label', self.label)])
        
        with open(json_path, 'w+') as fp:
            json.dump(tmp_holder, fp, indent=4)        
        
        print('Saving property: ' + json_path)
        
    @property
    def default_path(self):
        path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                            '..', 
                                            'working_dir',
                                            self.label + "_.json"))
        return path
        
    def save_to_json_default(self, event): 
        path = self.default_path
        self.save_to_json(self, path )


    @classmethod
    def from_json(cls, json_path, ax, bins, rotation, 
                  color=None, marker=None, alpha=None, markersize=None):
        
        with open(json_path) as data_file:    
            data = json.load(data_file, object_pairs_hook=col.OrderedDict)
            #assert set(data.keys())==set(['data','radius','alpha_marker',
            #                              'labels_size'])
   
            marker = marker if marker is not None else data['marker']
            alpha = alpha if alpha is not None else data['contrast']
            color = color if color is not None else data['color']
            markersize = markersize if markersize is not None else data['markersize']


            ifs_holder = list(data['data'].values())
            indices = range(len(ifs_holder))
            dat = list(map(tuple, ifs_holder))
            mus, nus = list(zip(*dat))
            mus, nus = list(mus), list(nus)
            print(mus)

            print(nus)
                         
            ax_01, line2d1_01 = plot_triangular_(ax,
                                            mus, nus, rang=1.0, bins=10,
                                            rotation={'x':45, 'y':0},
                                            markersize=markersize,
                                            color=color,
                                            marker=marker,
                                            alpha=alpha)
            ax_01.set_ylabel(r'$\nu$', fontsize=20)
            ax_01.set_xlabel(r'$\mu$', fontsize=20)
            
            line2d1_01.set_linestyle(' ')
            # line2d1_01.set_markersize(data['marker_size'])
            line2d1_01.set_markerfacecolor(color)
            line2d1_01.set_color(color)
        #     line2d1_01.set_marker(marker=r'$\odot$')
            line2d1_01.set_marker(marker=marker)    
            line2d1_01.set_zorder(2)
            # ax_01.set_aspect('equal', 'datalim')

            prop = PropertiesIFS(label='ifs01_ax01', 
                                 holder=line2d1_01,
                                 labels_size=data['labels_size'])
            prop.init_default(ax)
            return prop

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

