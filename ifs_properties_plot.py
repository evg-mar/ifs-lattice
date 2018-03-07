# import numpy as np
# from matplotlib.lines import Line2D
# from matplotlib.artist import Artist

# from ifs_operators_plot import *

# from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
import abc
import numpy as np
import json

from collections import OrderedDict

from ifs_2Dplot import plot_triangular_
from ifs_operators_plot import incGeneral

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
        



    def save_to_json(self, json_path):
        data = self.holder.get_data() 
        print(data)
        tmp_holder = OrderedDict([('data', list(zip(data[0], data[1]))),
                                 ('radius', self.radius),
                                 ('alpha_marker', self.alpha_marker),
                                 ('labels_size', self.labels_size),
                                 ('color', self.holder.get_color()),
                                 ('marker', self.holder.get_marker()),
                                 ('marker_size', self.holder.get_markersize())])
        
        print(tmp_holder)
        
        with open(json_path, 'w') as fp:
            json.dump(tmp_holder, fp, indent=4)        
        
        print('Saving property: ' + json_path)
        

    @classmethod
    def from_json(cls, json_path, ax, bins, rotation, 
                  color=None, marker=None, alpha=None):
        
        with open(json_path) as data_file:    
            data = json.load(data_file)
            #assert set(data.keys())==set(['data','radius','alpha_marker',
            #                              'labels_size'])
   
            marker = marker if marker is not None else data['marker']
            alpha = alpha if alpha is not None else data['alpha_marker']
            color = color if color is not None else data['color']
   
            ifs_holder = data['data']
            indices = range(len(ifs_holder))
            dat = list(map(tuple, ifs_holder))
            mus, nus = list(zip(*dat))
            mus, nus = list(mus), list(nus)
            print(mus)

            print(nus)
                         
            ax_01, line2d1_01 = plot_triangular_(ax,
                                            mus, nus, rang=1.0, bins=10,
                                            rotation={'x':45, 'y':0},
                                            color=color,
                                            marker=marker,
                                            alpha=alpha)
            ax_01.set_ylabel(r'$\nu$', fontsize=20)
            ax_01.set_xlabel(r'$\mu$', fontsize=20)
            
            line2d1_01.set_linestyle(' ')
            line2d1_01.set_markersize(data['marker_size'])
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
import ifs_operators_plot as oper  
import matplotlib.pyplot as plt 

class TopoConst(object):
    def __init__(self, ax, alpha, beta, gamma_a, gamma_b, companion=None):
        
        self.companion = companion
        
        self.alpha = alpha
        self.beta = beta
        self.gamma_a = gamma_a
        self.gamma_b = gamma_b

        self.axes = ax
        self.alpha2dline, = ax.plot([alpha]*3,
                                  [0.0, beta,  1-alpha],
                                  color='r',
                                  linewidth=2)
        
        self.beta2dline, = ax.plot([0.0, alpha, 1 - beta],
                                  [beta]*3,
                                  color='g',
                                  linewidth=2)
        
        self.gamma_a2dline, = ax.plot([alpha*gamma_a]*2,
                                      [0.0, 1 - alpha*gamma_a],
                                      color='black')
        self.gamma_b2dline, = ax.plot([0.0, 1 - beta*gamma_b],
                                      [beta*gamma_b]*2,
                              color='black')


        self.alpha_ann =   self.axes.annotate(r'$\alpha$', 
                    (self.alpha,0.0), 
                    xytext=(self.alpha-0.01,-0.08), fontsize=20)

        self.beta_ann =   self.axes.annotate(r'$\beta$', 
                    (0.0, self.beta), 
                    xytext=(-0.05, self.beta-0.01), fontsize=20)

        self.gamma_a_ann = self.axes.annotate(r'$\gamma_{\alpha}.\alpha$', 
             (self.alpha*self.gamma_a,0.0), 
             xytext=(self.alpha*self.gamma_a-0.01,-0.08), fontsize=20)
 
        self.gamma_b_ann = self.axes.annotate(r'$\gamma_{\beta}.\beta$', 
             (0.0, self.beta*self.gamma_b), 
             xytext=(-0.12, self.beta*self.gamma_b-0.01), fontsize=20)


        self.set_annotations()


    def set_animated(self,value):
        self.alpha2dline.set_animated(value)
        self.beta2dline.set_animated(value)

    def set_annotations(self):
        self.alpha_ann.set_position((self.alpha-0.01,-0.08))
        self.alpha_ann.set_text(r'$\alpha$')
        
        self.beta_ann.set_position((-0.05, self.beta-0.01))
        self.beta_ann.set_text(r'$\beta$')
        
        self.gamma_a_ann.set_position((self.alpha*self.gamma_a-0.01,-0.08))
        self.gamma_a_ann.set_text(r'$\gamma_{\alpha}.\alpha$')

        self.gamma_b_ann.set_position((-0.12, self.beta*self.gamma_b-0.01))
        self.gamma_b_ann.set_text(r'$\gamma_{\beta}.\beta$')

        
    @classmethod
    def from_json(cls, json_path, ax):
        with open(json_path) as data_file:    
            data = json.load(data_file)
            # assert set(data.keys())==set(['alpha','beta','gamma_a','gamma_b'])
            return TopoConst(ax,
                             alpha=data['alpha'], 
                             beta=data['beta'],
                             gamma_a=data['gamma_a'], 
                             gamma_b=data['gamma_b'])

    def save_to_json(self, json_path):
        holder = OrderedDict([('alpha', self.alpha),
                  ('beta', self.beta),
                  ('gamma_a', self.gamma_a),
                  ('gamma_b', self.gamma_b)])
        
        with open(json_path, 'w') as fp:
            json.dump(holder, fp, indent=4)        
        
        print('Saving: ' + json_path)
        print(holder)
        
    def set_topoconst(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        
        self.alpha2dline.set_data([alpha]*3,
                                  [0.0, beta,  1-alpha])
        self.beta2dline.set_data([0.0, alpha, 1 - beta],
                                  [beta]*3)

        self.gamma_a2dline.set_data([self.alpha*self.gamma_a]*2,
                                      [0.0, 1 - alpha*self.gamma_a])
        self.gamma_b2dline.set_data([0.0, 1 - self.beta*self.gamma_b],
                                    [self.beta*self.gamma_b]*2)

        self.set_annotations()

    def _fill_basic(self):
        pass

    def fill_fixed(self, typ):
        assert typ in ['closure', 'inclusion']
        # fill fixed points
#         self.axes.fill_between([0.0, self.alpha0],
#                                [1.0, 1-self.alpha0],
#                                hatch = '\\',
#                                #step = 'post',
#                                facecolor='none',
#                                edgecolor='red')

        self.axes.fill_between([self.alpha,1-self.beta,1-self.gamma_b*self.beta],
                               [1-self.alpha,self.beta, 0.0],
                               hatch = '\\',
                               #step = 'post',
                               facecolor='none',
                               edgecolor='red')
        if typ == 'inclusion':
            self._fill_inclusion()
        elif typ == 'closure':
            self._fill_closure()

    def fill_nu_full(self):
        self.axes.fill_between([0.0, 1-self.beta],
                               [1.0, self.beta],
                               [self.beta, self.beta],
                               hatch = '/',
                               #step = 'post',
                               facecolor='none',
                               edgecolor='g')
        
    def fill_nu_limited(self):

        self.axes.fill_between([0.0, self.alpha, 1-self.beta],
                               [1.0-self.gamma_a*self.alpha, 1-self.alpha, self.beta],
                               [self.beta, self.beta, self.beta],
                               hatch = '/',
                               #step = 'post',
                               facecolor='none',
                               edgecolor='g')

        self.axes.plot([0.0, self.gamma_a*self.alpha],
                       [1-self.gamma_a*self.alpha, 1-self.gamma_a*self.alpha],
                       linewidth=1.2,
                       color='black')
        self.axes.plot([0.0, self.alpha],
                       [1-self.alpha, 1-self.alpha],
                       linewidth=1.2,
                       color='black')
        self.axes.plot([0.0, self.alpha],
                       [1-self.gamma_a*self.alpha, 1-self.alpha],
                       linewidth=2,
                       color='g')


    def fill_mu_limited(self):
        self.axes.fill_between([self.alpha,1-self.beta,1-self.gamma_b*self.beta],
                       [1-self.alpha,self.beta, 0.0],
                       hatch = '\\',
                       #step = 'post',
                       facecolor='none',
                       edgecolor='red')
        self.axes.plot([1-self.beta, 1-self.beta],
                       [0.0, self.beta],
                       linewidth=1.2,
                       color='black')
        self.axes.plot([1-self.gamma_b*self.beta, 1-self.gamma_b*self.beta],
                       [0.0, self.gamma_b*self.beta],
                       linewidth=1.2,
                       color='black')
        self.axes.plot([1-self.beta, 1-self.gamma_b*self.beta],
                       [self.beta, 0.0],
                       linewidth=2,
                       color='red')

    def fill_mu_full(self):
        self.axes.fill_between([self.alpha, 1.0],
                       [1-self.alpha, 0.0],
                       hatch = '\\',
                       #step = 'post',
                       facecolor='none',
                       edgecolor='red')
        # 
#         self.axes.fill_between([0.0, 1-self.beta0, 1.0],
#                                [self.beta0, self.beta0, 0.0],
#                                hatch = '/',
#                                #step = 'post',
#                                facecolor='none',
#                                edgecolor='g')



    def draw_topo_object(self):
        self.axes.draw_artist(self.alpha2dline)
        self.axes.draw_artist(self.beta2dline)
        
    def set_visible(self, flag):
        self.alpha2dline.set_visible(flag)
        self.beta2dline.set_visible(flag)
    
    def get_visible(self):
        return self.alpha2dline.get_visible() and \
               self.beta2dline.get_visible()

############################

class TopoConstGeneral(object):
    def __init__(self, ax, 
                 alpha, 
                 beta, 
                 gamma_a, 
                 gamma_b, 
                 alpha0=0.0, 
                 beta0=0.0, 
                 companion=None):       

        assert alpha + beta <= 1.0

        
        self.companion = companion
         
        self.alpha = alpha
        self.beta = beta
        self.alpha0 = alpha0
        self.beta0 = beta0
        
        self.gamma_a = gamma_a
        self.gamma_b = gamma_b
 
        self.axes = ax

        self.alpha2dline0, = ax.plot([alpha0]*3,
                                  [0.0, beta0,  1-alpha0],
                                  color='r',
                                  linewidth=2)
         
        self.beta2dline0, = ax.plot([0.0, alpha0, 1 - beta0],
                                  [beta0]*3,
                                  color='g',
                                  linewidth=2)
        
        
        
        
        self.alpha2dline, = ax.plot([alpha]*3,
                                  [0.0, beta,  1-alpha],
                                  color='r',
                                  linewidth=2)
         
        self.beta2dline, = ax.plot([0.0, alpha, 1 - beta],
                                  [beta]*3,
                                  color='g',
                                  linewidth=2)

        dAlpha = alpha - alpha0
        dBeta  = beta - beta0

        self.gamma_a2dline, = ax.plot([(alpha0+dAlpha*gamma_a)]*2,
                                      [0.0, 1 - (alpha0+dAlpha*gamma_a)],
                                      color='black')
        self.gamma_b2dline, = ax.plot([0.0, 1 - (beta0 + dBeta*gamma_b)],
                                      [beta0 + dBeta*gamma_b]*2,
                              color='black')



        self.alpha_ann0 =   self.axes.annotate(r'$\alpha_1$', 
                    (self.alpha0,0.0), 
                    xytext=(self.alpha0-0.01,-0.08), fontsize=20)
 
        self.beta_ann0 =   self.axes.annotate(r'$\beta_1$', 
                    (0.0, self.beta0), 
                    xytext=(-0.05, self.beta0-0.01), fontsize=20)


        self.alpha_ann =   self.axes.annotate(r'$\alpha_2$', 
                    (self.alpha,0.0), 
                    xytext=(self.alpha-0.01,-0.08), fontsize=20)
 
        self.beta_ann =   self.axes.annotate(r'$\beta_2$', 
                    (0.0, self.beta), 
                    xytext=(-0.05, self.beta-0.01), fontsize=20)
 
        self.gamma_a_ann = self.axes.annotate(r'$\gamma_{\alpha}.\Delta_\alpha$', 
             (self.alpha0+ dAlpha*self.gamma_a, 0.0), 
             fontsize=20)
  
        self.gamma_b_ann = self.axes.annotate(r'$\gamma_{\beta}.\Delta_\beta$', 
             (0.0, self.beta0+dBeta*self.gamma_b), 
             fontsize=20)


        self.set_annotations_general()

    def fill_fixed(self):
        # fill fixed points
        self.axes.fill_between([0.0, self.alpha0],
                               [1.0, 1-self.alpha0],
                               hatch = '\\',
                               #step = 'post',
                               facecolor='none',
                               edgecolor='red')
        self.axes.fill_between([self.alpha, 1.0],
                               [1-self.alpha, 0.0],
                               hatch = '\\',
                               #step = 'post',
                               facecolor='none',
                               edgecolor='red')
        # 
        self.axes.fill_between([0.0, 1-self.beta0, 1.0],
                               [self.beta0, self.beta0, 0.0],
                               hatch = '/',
                               #step = 'post',
                               facecolor='none',
                               edgecolor='g')

        self.axes.fill_between([0.0, 1-self.beta],
                               [1.0, self.beta],
                               [self.beta, self.beta],
                               hatch = '/',
                               #step = 'post',
                               facecolor='none',
                               edgecolor='g')
        




    def set_animated(self,value):
        self.alpha2dline.set_animated(value)
        self.beta2dline.set_animated(value)

    def set_annotations_general(self):
        print('call set annot general')
        dAlpha = self.alpha - self.alpha0
        dBeta  = self.beta - self.beta0

        self.alpha_ann0.set_position((self.alpha0-0.01,-0.08))
        self.alpha_ann0.set_text(r'$\alpha_1$')
        
        self.beta_ann0.set_position((-0.05, self.beta0-0.01))
        self.beta_ann0.set_text(r'$\beta_1$')


        self.alpha_ann.set_position((self.alpha-0.01,-0.08))
        self.alpha_ann.set_text(r'$\alpha_2$')
        
        self.beta_ann.set_position((-0.05, self.beta-0.01))
        self.beta_ann.set_text(r'$\beta_2$')
        
        
        self.gamma_a_ann.set_position((self.alpha0+ dAlpha*self.gamma_a-0.01,-0.08))
        self.gamma_a_ann.set_text(r'$\gamma_{\alpha}.\Delta_\alpha$')

        self.gamma_b_ann.set_position((-0.12, self.beta0+dBeta*self.gamma_b-0.01))
        self.gamma_b_ann.set_text(r'$\gamma_{\beta}.\Delta_\beta$')

        
    @classmethod
    def from_json(cls, json_path, ax):
        with open(json_path) as data_file:    
            data = json.load(data_file)
            #assert set(data.keys())==set(['alpha','beta','gamma_a','gamma_b'])
            return TopoConstGeneral(ax,
                             alpha=data['alpha'], 
                             beta=data['beta'],
                             gamma_a=data['gamma_a'], 
                             gamma_b=data['gamma_b'],
                             alpha0=data['alpha0'], 
                             beta0=data['beta0'],)

    def save_to_json(self, json_path):
        holder = OrderedDict([('alpha', self.alpha),
                  ('beta', self.beta),
                  ('gamma_a', self.gamma_a),
                  ('gamma_b', self.gamma_b)])
        
        with open(json_path, 'w') as fp:
            json.dump(holder, fp, indent=4)        
        
        print('Saving: ' + json_path)
        print(holder)
        
    def set_topoconst(self, alpha, beta, alpha0, beta0):
        self.alpha = alpha
        self.beta = beta
        self.alpha0=alpha0
        self.beta0=beta0

        
        dAlpha = alpha - self.alpha0
        dBeta  = beta - self.beta0
        
        
        self.alpha2dline.set_data([alpha]*3,
                                  [0.0, beta,  1-alpha])
        self.beta2dline.set_data([0.0, alpha, 1 - beta],
                                  [beta]*3)

        self.gamma_a2dline.set_data([alpha0+dAlpha*self.gamma_a]*2,
                                      [0.0, 1 - alpha0+dAlpha*self.gamma_a])
        self.gamma_b2dline.set_data([0.0, 1 - beta0 + dBeta*self.gamma_b],
                                      [beta0 + dBeta*self.gamma_b]*2)

        self.set_annotations()

    def draw_topo_object(self):
        self.axes.draw_artist(self.alpha2dline)
        self.axes.draw_artist(self.beta2dline)
        
    def set_visible(self, flag):
        self.alpha2dline.set_visible(flag)
        self.beta2dline.set_visible(flag)
    
    def get_visible(self):
        return self.alpha2dline.get_visible() and \
               self.beta2dline.get_visible()


###########################

class TopoConstInteractive(TopoConst):
    
    def __init__(self, ax, alpha, beta, gamma_a, gamma_b, companion=None):
        super(self.__class__, self).__init__(ax, alpha, beta, gamma_a, gamma_b)
        self.companion = companion
        self.active_artist = None
 
    def connect(self):
        'connect to all the events we need'
        canvas = self.axes.figure.canvas
        self.cidpick = canvas.mpl_connect('pick_event',
                                          self.on_pick)
        
#         self.cidpress = canvas.mpl_connect('button_press_event',
#                                            self.on_press)
#         self.ciddraw = self.rect.figure.canvas.mpl_connect(
#             'draw_event', self.draw_callback)
        self.cidrelease = canvas.mpl_connect('button_release_event',
                                             self.on_release)
        self.cidmotion = canvas.mpl_connect('motion_notify_event',
                                            self.on_motion)


    def on_pick(self, event):
        print("on pick..", event.artist)

        if event.artist not in [self.alpha2dline, self.beta2dline]:
            return
        if self.active_artist is not None:
            return

        self.active_artist = event.artist

        self.active_artist.set_animated(True)

        
        canvas = self.axes.figure.canvas
        canvas.draw()

        self.background = canvas.copy_from_bbox(self.axes.figure.bbox)
        # now redraw just the rectangle
        self.axes.draw_artist(self.active_artist)

        # and blit just the redrawn area
        canvas.blit(self.axes.bbox)
        
        if self.companion is not None:                
            self.companion.set_animated(True)
#             self.companion.background = \
#                 canvas.copy_from_bbox(self.companion.rect.axes.figure.bbox)
            self.companion.draw_blit()
                    
##################
    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
#         if HolderCircle.lock is not self:
#             return
#         print("in motion...")
#         print(HolderCircle.lock)
        if event.inaxes != self.axes:
            return
        if self.active_artist != event.artist:
            return
#         if (HolderCircle.lock is None) or (HolderCircle.idx is None):
#             return
# 
#         obj = HolderCircle.lock

        self.set_topoconst(event.xdata, event.ydata)
#         obj.set_munu((event.xdata, event.ydata))
#         print('animated in motion...: ', obj.get_animated(), obj.annotation.get_animated())
#         print(obj)
#

        canvas = self.axes.figure.canvas
#         canvas = self.companion.rect.figure.canvas
        canvas.restore_region(self.background)
        self.axes.draw_artist(self.active_artist)
        canvas.blit(self.axes.bbox)

        if self.companion is not None:
            self.companion.set_munu((event.xdata, event.ydata))
            self.companion.draw_object()
            canvas.blit(self.companion.rect.axes.bbox)


    def draw_blit(self, obj):          
        obj.draw_on(self.axes)
        self.axes.figure.canvas.blit(self.axes.bbox)


    def on_release(self, event):
        'on release we reset the press data'
        if event.inaxes != self.axes:
            return
#         if (HolderCircle.lock is None) or (HolderCircle.idx is None):
#             return
        
#         if self.companions is not None:
#             companion = self.companions[HolderCircle.idx]
#             print(HolderCircle.lock)
# #             print(HolderCircle.lock.get_munu)
#             mu, nu = HolderCircle.lock.get_munu()
#             companion.set_munu(mu,nu)

        # turn off the rect animation property and reset the background
        self.active_artist.set_animated(False)
        
        
        self.background = None
        
        if self.companion is not None:
            self.companion.set_animated(False)
            self.companion.background = None
            self.companion = None
        # redraw the full figure
        self.axes.figure.canvas.draw()

####################



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
                       show_ann,
                       hide_ifs,
                       showverts,
                       showedges,
                       showlabels)

        self.topo_const = topo_const
        self.axes = self.holder.axes
#         self.idx_active = None

    @classmethod
    def from_property_topoconst(cls, prop, topo_const):
        return PropertiesIFSTopo(prop.label,
                                 prop.holder,
                                 topo_const,
                                 prop.radius,
                                 prop.annotations,
                                 prop.alpha_marker,
                                 prop.labels_size,
                                 prop.show_ann,
                                 prop.hide_ifs,
                                 prop.showverts,
                                 prop.showedges,
                                 prop.showlabels)

    @classmethod
    def from_json(cls, json_path_prop,
                  json_path_topoconst,
                  ax,
                  bins,
                  rotation,
                  color='b',
                  marker='o'):
        topo_const = TopoConst.from_json(json_path_topoconst, ax)
        prop = PropertiesIFS.from_json(json_path_prop, ax, bins, rotation,
                                       color=color,
                                       marker=marker)
        return PropertiesIFSTopo.from_property_topoconst(prop, topo_const)


    def save_to_json(self, json_path_prop, json_path_topoconst):
        super(PropertiesIFSTopo, self).save_to_json(json_path_prop)
        self.topo_const.save_to_json(json_path_topoconst)


    def update_topo_const(self, alpha, beta):
        self.topo_const.set_topoconst(alpha, beta)

     

#     def draw_holder_annotations(self, ax):
#         super(PropertiesIFSTopo, self).draw_holder_annotations(ax)
#         self.topo_const_triang.draw_topo_object(ax)  

    def incGeneral(self):
        return oper.incGeneral(self.get_data_pair(),
                        self.topo_const.alpha,
                        self.topo_const.beta,
                        self.topo_const.gamma_a,
                        self.topo_const.gamma_b)

    def clGeneral(self):
        return oper.clGeneral(self.get_data_pair(),
                       self.topo_const.alpha,
                       self.topo_const.beta,
                       self.topo_const.gamma_a,
                       self.topo_const.gamma_b)

    def applyInclusion(self):
        data = self.incGeneral()
        self.set_data(data[0], data[1])     
        self.set_data_annotations(list(zip(data[0], data[1])))

    def applyClosure(self):
        print('original closure')
        print(self.get_data())
        data = self.clGeneral()
        self.set_data(data[0], data[1])
        print(list(zip(data[0], data[1])))
        print(self.get_data())
        self.set_data_annotations(list(zip(data[0], data[1])))

#########################
# Introducing two alphas and betas

class PropertiesIFSTopoGeneral(PropertiesIFS):
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
    
        super(self.__class__, self).__init__(label,
                       holder,
                       radius,
                       annotations,
                       alpha_marker, 
                       labels_size,
                       show_ann,
                       hide_ifs,
                       showverts,
                       showedges,
                       showlabels)

        self.topo_const = topo_const
        self.axes = self.holder.axes
#         self.idx_active = None

    @classmethod
    def from_property_topoconst(cls, prop, topo_const):
        return PropertiesIFSTopoGeneral(prop.label,
                                 prop.holder,
                                 topo_const,
                                 prop.radius,
                                 prop.annotations,
                                 prop.alpha_marker,
                                 prop.labels_size,
                                 prop.show_ann,
                                 prop.hide_ifs,
                                 prop.showverts,
                                 prop.showedges,
                                 prop.showlabels)

    @classmethod
    def from_json(cls, json_path_prop,
                  json_path_topoconst,
                  ax,
                  bins,
                  rotation,
                  color='b',
                  marker='o'):
        topo_const = TopoConstGeneral.from_json(json_path_topoconst, ax)
        prop = PropertiesIFS.from_json(json_path_prop, ax, bins, rotation,
                                       color=color,
                                       marker=marker)
        return PropertiesIFSTopoGeneral.from_property_topoconst(prop, topo_const)


    def save_to_json(self, json_path_prop, json_path_topoconst):
        super(PropertiesIFSTopo, self).save_to_json(json_path_prop)
        self.topo_const.save_to_json(json_path_topoconst)


    def update_topo_const(self, alpha, beta):
        self.topo_const.set_topoconst(alpha, beta)

     

#     def draw_holder_annotations(self, ax):
#         super(PropertiesIFSTopo, self).draw_holder_annotations(ax)
#         self.topo_const_triang.draw_topo_object(ax)  

    def incGeneral2(self):
        return oper.incGeneral2(self.get_data_pair(),
                        self.topo_const.alpha0,
                        self.topo_const.beta0,
                        self.topo_const.alpha,
                        self.topo_const.beta,
                        self.topo_const.gamma_a,
                        self.topo_const.gamma_b)

    def clGeneral2(self):
        return oper.clGeneral2(self.get_data_pair(),
                       self.topo_const.alpha0,
                       self.topo_const.beta0,
                       self.topo_const.alpha,
                       self.topo_const.beta,
                       self.topo_const.gamma_a,
                       self.topo_const.gamma_b)

    def fill_fixed(self):
        #self.axes
        pass

    def applyInclusion(self, 
                       fill_fixed=False): # Fill fixed points
        data = self.incGeneral2()
        self.set_data(data[0], data[1])     
        self.set_data_annotations(list(zip(data[0], data[1])))
        


    def applyClosure(self, 
                     fill_fixed=False):
        data = self.clGeneral2()
        self.set_data(data[0], data[1])
        #print(list(zip(data[0], data[1])))     
        self.set_data_annotations(list(zip(data[0], data[1])))


##########################


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

    @classmethod
    def from_properties_ifs_topo(cls, prop_ifs_topo):
        return  cls(prop_ifs_topo.label,
                   prop_ifs_topo.holder,
                   prop_ifs_topo.topo_const,
                   prop_ifs_topo.radius,
                   prop_ifs_topo.annotations,
                   prop_ifs_topo.alpha_marker, 
                   prop_ifs_topo.labels_size,
                   prop_ifs_topo.hide_ifs,
                   prop_ifs_topo.show_ann,
                   prop_ifs_topo.showverts,
                   prop_ifs_topo.showedges,
                   prop_ifs_topo.showlabels)

    
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
            self.topo_const.draw_topo_object()

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
            self.update_topo_const(xdata, ydata)
            self.axes.figure.canvas.restore_region(self.background)
            self.topo_const.draw_topo_object()        

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

        self.axes.figure.canvas.draw()
    
    
    
    
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
    
    ax = plt.subplot2grid((1,1), (0,0), rowspan=3, colspan=3)


    #############
    json_path = '/home/evgeniy/Documents/IFS-Simulator/ifs-lattice/ifsholder/'    
    json_prop_name = 'property01.json'
#    prop01 = PropertiesIFS.from_json(json_path + json_prop_name, 
#                                    ax, 
#                                     bins=10, 
#                                     rotation={'x':45, 'y':0})    
    #############   
#    prop01.init_default(ax)

    json_topoconst = 'topo_const_config_general.json'
#    topo_c0201 = TopoConst.from_json(ax=ax, 
#                           json_path=json_path+json_name)



    prop_topo = PropertiesIFSTopo.from_json(json_path + json_prop_name, 
                                            json_path + json_topoconst,
                                            ax, 
                                            bins=10, 
                                            rotation={'x':45, 'y':0})

    
    prop_topo_cl = PropertiesIFSTopo.from_json(json_path + json_prop_name, 
                                            json_path + json_topoconst,
                                            ax, 
                                            bins=10, 
                                            rotation={'x':45, 'y':0},
                                            color='red',
                                            marker="^")

    prop_topo_cl.topo_const.fill_nu_limited()
    prop_topo_cl.topo_const.fill_mu_full()
    # prop_topo_cl.topo_const.fill_
    prop_topo_cl.applyClosure()
    
    # inclusion
    '''
    prop_topo_inc = PropertiesIFSTopo.from_json(json_path + json_prop_name, 
                                            json_path + json_topoconst,
                                            ax, 
                                            bins=10, 
                                            rotation={'x':45, 'y':0},
                                            color='g',
                                            marker="v")

    prop_topo_inc.topo_const.fill_nu_full()
    prop_topo_inc.topo_const.fill_mu_limited()
    # prop_topo_cl.topo_const.fill_
    prop_topo_inc.applyInclusion()
    '''



#  GENERAL

#     prop_topoG = PropertiesIFSTopoGeneral.from_json(json_path + json_prop_name, 
#                                             json_path + json_topoconst,
#                                             ax, 
#                                             bins=10, 
#                                             rotation={'x':45, 'y':0})
# 
# 
#     prop_topo_clG = PropertiesIFSTopoGeneral.from_json(json_path + json_prop_name, 
#                                             json_path + json_topoconst,
#                                             ax, 
#                                             bins=10, 
#                                             rotation={'x':45, 'y':0},
#                                             color='red',
#                                             marker="^")
#     
#     prop_topo_clG.topo_const.fill_fixed()
#     prop_topo_clG.applyClosure()

# 
#  
#     prop_topo_inc = PropertiesIFSTopoGeneral.from_json(json_path + json_prop_name, 
#                                             json_path + json_topoconst,
#                                             ax, 
#                                             bins=10, 
#                                             rotation={'x':45, 'y':0},
#                                             color='green',
#                                             marker="v")
    #prop_topo_inc.topo_const.fill_fixed()
    #prop_topo_inc.applyInclusion()
    
# END GENERAL
    
    ax.set_xlim([-0.15, 1.15])
    ax.set_ylim([-0.15, 1.15])
    



#     print(prop_topo.holder)
#     print(prop_topo.holder.axes)
#     prop_topo_interactive = \
#         PropertiesIFSTopoInteractive.from_properties_ifs_topo(prop_topo)
#      
#     prop_topo_interactive.applyClosure()
# #     
#     print(prop_topo_interactive.holder.axes)
#     prop_topo_interactive.set_animated(True)
#     prop_topo_interactive.connect()

    plt.show()
    
    print('Finish here...')
