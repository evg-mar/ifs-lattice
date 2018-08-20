from editable_circle import HolderCircle
# from ifs_properties_plot import TopoConst, TopoConstInteractive
from topo_const_triang import TopoConstTriangInteractive

import abc

import numpy as np
import matplotlib.pyplot as plt
import collections

class IfsTriangAbstract(object):
    __metaclass__  = abc.ABCMeta

    
    @abc.abstractmethod
    def get_data(self):
        return
     
    @abc.abstractmethod
    def get_data_pair(self):
        return
     
from ifs_2Dplot import plot_triangle

class IfsTriang(IfsTriangAbstract):
    flip = 1

    
    def __init(self, bins, colors):
                                     
        rang = 1
#         rotation=None

        xlinspace = np.linspace(0.0, rang, bins['mu']+1)
        self.axes.set_xticks(xlinspace)
        ylinspace = np.linspace(0.0, rang, bins['nu']+1)
        self.axes.set_yticks(ylinspace)

        plot_triangle(rang, self.axes, 'k')

        self.axes.grid(True, linestyle='--')
        for lin in self.axes.get_xgridlines():
            lin.set_color(colors['mu'])
        for lin in self.axes.get_ygridlines():
            lin.set_color(colors['nu'])
                             
        self.axes.legend(loc='upper right')                    

        
    
    def __init__(self, axes, musnus,
                       radius=0.01,
                       labels=None,
                       picker=10,
                       alpha_marker=0.5, 
                       visible=True,
                       annotation_size=12,
                       show_annotation=True,
                       colors = {'mu':'b', 'nu':'g', 'elem':'r'},
                       bins = {'mu':10, 'nu':10},
                       init_flag=True):
        print("in ifs triang...")
                
        self.axes = axes
        self.labels = labels if (labels is not None) \
                             else list(range(len(musnus[0])))

        if init_flag:
            self.__init(bins, colors)
                             
        self.holder = []

        radia = radius if isinstance(radius, collections.Iterable) \
                             else [radius]*len(self.labels)

        for label, rad, mu, nu in zip(self.labels, radia, *musnus):

            obj = HolderCircle(axes, (mu,nu), rad,
                               label=str(label),
                               color=colors['elem'],
                               picker=picker,
                               alpha_marker=alpha_marker)

            self.holder.append(obj)

    def get_data(self):
        return np.array(list(map(lambda obj: obj.get_center(), self.holder)))
     

    def get_data_pair(self):
        mus = map(lambda obj: obj.get_center()[0], self.holder) 
        nus = map(lambda obj: obj.get_center()[1], self.holder)
        return np.array(list(mus)), np.array(list(nus)) 



class IfsTriangInteractive(IfsTriang):
    def __init__(self,axes, musnus,
                       radius=0.01,
                       companions=None,
                       labels=None,
                       picker=10,
                       alpha_marker=0.5, 
                       visible=True,
                       annotation_size=12,
                       show_annotation=True,
                       colors = {'mu':'b', 'nu':'g', 'elem':'r'},
                       bins = {'mu':10, 'nu':10},
                       init_flag=True
                       ):
        super(IfsTriangInteractive, self).__init__(axes, musnus,
                                                   radius,
                                                   labels,
                                                   picker,
                                                   alpha_marker,
                                                   visible,
                                                   annotation_size,
                                                   show_annotation,
                                                   colors,
                                                   bins,
                                                   init_flag)

        self.activeCircle = None

        self.companions = companions
        # self.companion = None
        self.companion_elements = None

        
        xdata, ydata = 0.5, 0.5
        self.x2Dline, = self.axes.plot([xdata]*3,
                                  [0.0, ydata,  1-xdata],
                                  color='r',
                                  linewidth=2)
        self.x2Dline.set_visible(False)

        self.y2Dline, = self.axes.plot([0.0, xdata, 1 - ydata],
                                  [ydata]*3,
                                  color='g',
                                  linewidth=2)
        self.y2Dline.set_visible(False)

    def connect(self):
        'connect to all the events we need'
        canvas = self.axes.figure.canvas
        self.cidpick = canvas.mpl_connect('pick_event',
                                          self.on_pick)
        
        self.cidpress = canvas.mpl_connect('button_press_event',
                                           self.on_press)
#         self.ciddraw = self.rect.figure.canvas.mpl_connect(
#             'draw_event', self.draw_callback)
        self.cidrelease = canvas.mpl_connect('button_release_event',
                                             self.on_release)
        self.cidmotion = canvas.mpl_connect('motion_notify_event',
                                            self.on_motion)

    def on_press(self, event):
        print("on press...")

    def on_pick(self, event):
#        self.connect()
        
        print("on pick..", event.artist)
        if not isinstance(event.artist, HolderCircle):
            return
        if event.artist not in self.holder:
            return
        if self.activeCircle is not None:
            return

        self.activeCircle = event.artist
        # HolderCircle.lock = event.artist
        for c in self.holder:
            print(c)
        print(event.artist)

        self.activeCircle.idx  = self.holder.index(event.artist)

        
        canvas = self.axes.figure.canvas
        canvas.draw()

        
#        event.artist.set_animated(True)
        self.activeCircle.set_animated(True)
        self.activeCircle.background =  \
                canvas.copy_from_bbox(self.activeCircle.axes.figure.bbox)
        self.activeCircle.draw_blit()


        self.background = canvas.copy_from_bbox(self.axes.figure.bbox)
        # now redraw just the rectangle
#        event.artist.draw_object()

        if self.companions is not None:                
            
            ### companion elements
            self.companion_elements = [(comp[0], comp[1][self.activeCircle.idx]) \
                                       for comp in self.companions]
            for action, companion_elem in self.companion_elements:
                companion_elem.set_animated(True)
                companion_elem.background = \
                    canvas.copy_from_bbox(companion_elem.axes.figure.bbox)
                companion_elem.draw_blit()
            ###

        xdata, ydata = self.activeCircle.get_munu()
        if xdata + ydata > 1.0:
           xdata, ydata = ((xdata-ydata+1)/2, (ydata-xdata+1)/2)
            
        self.x2Dline.set_data([xdata]*3,
                                  [0.0, ydata,  1-xdata])
#        self.axes.draw_artist(self.x2Dline)
        
        self.y2Dline.set_data([0.0, xdata, 1 - ydata],
                                  [ydata]*3)
#        self.axes.draw_artist(self.y2Dline)        
  
           
        self.x2Dline.set_visible(True)
        self.x2Dline.set_linestyle('-')
        self.x2Dline.set_animated(True)
        print(type(self.x2Dline))
        

        self.y2Dline.set_visible(True)
        self.y2Dline.set_linestyle('-')
        self.y2Dline.set_animated(True)

        self.axes.draw_artist(self.x2Dline) 
        self.axes.draw_artist(self.y2Dline) 
#        # and blit just the redrawn area
        canvas.blit(self.axes.bbox)                    
        
    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
#         if HolderCircle.lock is not self:
#             return
#         print("in motion...")
#         print(HolderCircle.lock)
        if event.inaxes != self.axes:
            return
        if (self.activeCircle is None) or (self.activeCircle.idx is None):
            return

            
        xdata, ydata = event.xdata, event.ydata
        if xdata + ydata > 1.0:
           xdata, ydata = ((xdata-ydata+1)/2, (ydata-xdata+1)/2)
        
        obj = self.activeCircle
        obj.set_munu((xdata, ydata))
        print('animated in motion...: ', obj.get_animated(), obj.annotation.get_animated())
        print(obj)

        canvas = self.axes.figure.canvas

        canvas.restore_region(self.background)

        if self.companions is not None:
            
            ### companion_elements
            for action, comp_elem in self.companion_elements:
                comp_elem.set_munu(action(xdata, ydata))
                comp_elem.draw_object()
#            if comp_elem_last is not None:
#                canvas.blit(comp_elem.axes.bbox)
        self.x2Dline.set_data([xdata]*3,
                                  [0.0, ydata,  1-xdata])
        self.axes.draw_artist(self.x2Dline)
        
        self.y2Dline.set_data([0.0, xdata, 1 - ydata],
                                  [ydata]*3)
        self.axes.draw_artist(self.y2Dline)        
#        self.x2Dline.set_visible(True)    
#        self.y2Dline.set_visible(True)
#        self.draw_blit(self.x2Dline)



        obj.draw_object()
        canvas.blit(self.axes.bbox)


    def draw_blit(self, obj):          
        obj.draw_object()
        self.axes.figure.canvas.blit(self.axes.bbox)


    def on_release(self, event):
        'on release we reset the press data'
        print('on release')
        if event.inaxes != self.axes:
            return
        if (self.activeCircle is None): # or (self.activeCircle.idx is None):
            return

        # turn off the rect animation property and reset the background
        self.activeCircle.set_animated(False)
        self.activeCircle = None # HolderCircle.idx = None

        self.background = None
        
        if self.companions is not None:
            
            for action, comp_elem in self.companion_elements:
                comp_elem.set_animated(False)
                comp_elem.background = None
                
            self.companion_elements = None

            
        self.x2Dline.set_visible(False)    
        self.y2Dline.set_visible(False)    
        self.x2Dline.set_animated(False)    
        self.y2Dline.set_animated(False)    

            
        # redraw the full figure
        self.axes.figure.canvas.draw()

        
class IfsTriangTopoConstInteractive(IfsTriangInteractive):
    def __init__(self,axes, musnus,
                       topo_const_triang,
                       radius=0.01,
                       companions=None,
#                        companion_topo_const=None,
                       labels=None,
                       picker=10,
                       alpha_marker=0.5, 
                       visible=True,
                       annotation_size=12,
                       show_annotation=True,
                       colors = {'mu':'b', 'nu':'g', 'elem':'r'},
                       bins = {'mu':10, 'nu':10},
                       init_flag=True    
                 ):
        super(IfsTriangTopoConstInteractive, self).__init__(axes, musnus,
                       radius,
                       companions,
                       labels,
                       picker,
                       alpha_marker, 
                       visible,
                       annotation_size,
                       show_annotation,
                       colors,
                       bins,
                       init_flag)
        self.topo_const_triang = topo_const_triang
#         self.companion_topo_const = companion_topo_const
        
    def connect(self):
        super(IfsTriangTopoConstInteractive, self).connect()
        self.topo_const_triang.connect()
#         if self.companion_topo_const is not None:
#             self.companion_topo_const.connect()


if __name__ == '__main__':

    from universal_set import UniversalSet
    from intuitionistic_fuzzy_set import IFS

    import matplotlib.pyplot as plt

    universe = UniversalSet(set(range(15)))

    fig = plt.figure()
    plt.subplots_adjust(hspace=0.1, wspace=0.1)

    ifs01 = IFS.random(universe, 1, randseed=1)

    indices, mus, nus, pis = ifs01.elements_split()
    
    ax = plt.subplot2grid((4,6), (0,0), rowspan=3, colspan=3)


    topoconst = TopoConstTriangInteractive(ax, 0.6, 0.2, 0.5)
#
#    ifs_topoconst = IfsTriangTopoConstInteractive(ax, (mus,nus), topoconst)
#    ifs_topoconst.connect()
#    

    ifs02 = IFS.random(universe, 1, randseed=2)
    indices2, mus2, nus2, pis2 = ifs02.elements_split()

    ifs_triang02 = IfsTriangInteractive(ax, (mus2, nus2))
    ifs_triang02.connect()
    
    
#     ifstriang_topoconst = IfsTriangInteractive(ax, (mus,nus))
#     ifstriang_topoconst.connect()
#     prop.connect()
     
#     prop = IfsTriangInteractive(ax, ([0.1, 0.4, 0.6], [0.6, 0.4, 0.4]),
#                                 radius=.01)
# 
#     prop.connect()
    
     
    plt.show()