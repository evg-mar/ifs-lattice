# draggable rectangle with the animation blit techniques; see
# http://www.scipy.org/Cookbook/Matplotlib/Animations
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.text import Annotation

from matplotlib.patches import Rectangle, Circle

from universal_set import UniversalSet
from intuitionistic_fuzzy_set import IFS

class HolderCircle(Circle):
    lock =None
    idx  = None
    
    def __init__(self, axes, munu,
                       radius=0.01,
                       annotation_size=12,
#                        visible=True,
                       show_annotation=True,
#                        showvert=True,
                       **kwargs):
        super(HolderCircle, self).__init__(xy=munu,
                                           radius=radius,
                                           **kwargs)
        self.axes = axes
        self.axes.add_patch(self)
        # label, facecolor, edgecolor, get_visible, get_alpha

        if self.get_label() != '' and show_annotation == True:
            self.create_annotation(annotation_size, self._label)

        self.active_objects = {self.annotation: True}
    
    
    def __str__(self):
        return self._label + super(HolderCircle, self).__str__()
    
    def set_animated(self, value):
#         print("in set animated...")
        super(HolderCircle, self).set_animated(value)
        self.annotation.set_animated(value)
#         for obj, active_flag in self.active_objects.items():
#             if active_flag:
#                 obj.set_animated(value)
    
    def create_annotation(self, annotation_size, label=''):
        label = label if (label != '') else self._label
        assert(label != '')
        self.annotation = self.axes.annotate(str(label),
                                     self.center,
                                     fontsize='medium') #, zorder=10)

    def draw_on(self, axes):
        self.axes.draw_artist(self)
        for obj, active_flag in self.active_objects.items():
            if active_flag:
                axes.draw_artist(obj)

    def add_object(self, axes):
        self.axes.add_patch(self)
#         for obj, active_flag in self.active_objects.items():
#             if active_flag:
#                 axes.add_artist(obj)

#     @property
    def get_munu(self):
        return self.center
    
    def set_mu(self, mu):
        self.center = mu, self.center[1]
        if hasattr(self, 'annotation'):
            print('has annotation...')
            ann = self.annotation
            ann.xy = ann.xyann = ann.xytext = (mu, self.center[1])        

    def set_nu(self, nu):
        self.center = self.center[0], nu
        if hasattr(self, 'annotation'):
            print('has annotation...')
            ann = self.annotation
            ann.xy = ann.xyann = ann.xytext = (self.center[0], nu)           
    
    def set_munu(self, munu):
        self.center = munu
        if hasattr(self, 'annotation'):
            print('has annotation...')
            ann = self.annotation
            ann.xy = ann.xyann = ann.xytext = munu
            
    @property
    def get_text(self):
        return self.annotation.get_text()


import abc
import numpy as np

class PropertiesTriangAbstract(object):
    __metaclass__  = abc.ABCMeta

    
    @abc.abstractmethod
    def get_data(self):
        return
     
    @abc.abstractmethod
    def get_data_pair(self):
        return
     
#     @abc.abstractmethod
#     def set_data(self, mu, nu):
#         return
     
#     @abc.abstractclassmethod
#     def get_color(self):
#         return
#  
#     @abc.abstractclassmethod
#     def set_color(self):
#         return


from ifs_2Dplot import plot_triangle

class PropertiesTriang(PropertiesTriangAbstract):
    flip = 1

    def __init__(self, axes, musnus,
                       radius=0.01,
                       labels=None,
                       companions=None,
                       picker=10,
                       color='blue',
                       alpha_marker=0.5, 
                       visible=True,
                       annotation_size=12,
                       show_annotation=True):
        
        self.axes = axes
        self.labels = labels if (labels is not None) \
                             else list(range(len(musnus[0])))
                             
        self.companions = companions     
        self.companion = None                
        bins = {'mu':10, 'nu':10}
        colors = {'mu':'b', 'nu':'g', 'elem':'r'}
        rang = 1
        rotation=None

        xlinspace = np.linspace(0.0, rang, bins['mu']+1)
        self.axes.set_xticks(xlinspace)
        ylinspace = np.linspace(0.0, rang, bins['nu']+1)
        self.axes.set_yticks(ylinspace)                             
                             
        plot_triangle(rang, self.axes, 'k')                             
                             
        self.axes.grid(True, linestyle='--', color='r')
        for lin in self.axes.get_xgridlines():
            lin.set_color(colors['mu'])
        for lin in self.axes.get_ygridlines():
            lin.set_color(colors['nu'])
                             
        self.axes.legend(loc='upper right')                    
        
        self.holder = []
#         print(musnus)
#         print(self.labels)


        for label, mu, nu in zip(self.labels, *musnus):
            obj = HolderCircle(axes, (mu,nu), radius,
                               label=str(label),
                               picker=picker)
#             obj.add_object()
            self.holder.append(obj)


    def get_data(self):
        return np.array(list(map(lambda obj: obj.get_center(), self.holder)))
     

    def get_data_pair(self):
        mus = map(lambda obj: obj.get_center()[0], self.holder) 
        nus = map(lambda obj: obj.get_center()[1], self.holder)
        return np.array(list(mus)), np.array(list(nus)) 

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
        print("on pick..", event.artist)
        if not isinstance(event.artist, HolderCircle):
            return
        if HolderCircle.lock is not None:
            return
        HolderCircle.lock = event.artist
        HolderCircle.idx  = self.holder.index(event.artist)
        
        event.artist.set_animated(True)

        canvas = self.axes.figure.canvas
        canvas.draw()

        self.background = canvas.copy_from_bbox(self.axes.figure.bbox)
        # now redraw just the rectangle
        event.artist.draw_on(self.axes)

        # and blit just the redrawn area
        canvas.blit(self.axes.bbox)
        
        if self.companions is not None:                
            self.companion = self.companions[HolderCircle.idx]
            self.companion.set_animated(True)
            self.companion.background = \
                canvas.copy_from_bbox(self.companion.rect.axes.figure.bbox)
            self.companion.draw_blit()
                    
        
    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
#         if HolderCircle.lock is not self:
#             return
#         print("in motion...")
#         print(HolderCircle.lock)
        if event.inaxes != self.axes:
            return
        if (HolderCircle.lock is None) or (HolderCircle.idx is None):
            return

        obj = HolderCircle.lock
        obj.set_munu((event.xdata, event.ydata))
        print('animated in motion...: ', obj.get_animated(), obj.annotation.get_animated())
        print(obj)
     
    
        canvas = self.axes.figure.canvas
#         canvas = self.companion.rect.figure.canvas
        canvas.restore_region(self.background)

        self.companion.set_munu((event.xdata, event.ydata))
        self.companion.draw_object()
        canvas.blit(self.companion.rect.axes.bbox)

        obj.draw_on(self.axes)
        canvas.blit(self.axes.bbox)


    def draw_blit(self, obj):          
        obj.draw_on(self.axes)
        self.axes.figure.canvas.blit(self.axes.bbox)


    def on_release(self, event):
        'on release we reset the press data'
        if event.inaxes != self.axes:
            return
        if (HolderCircle.lock is None) or (HolderCircle.idx is None):
            return
        
#         if self.companions is not None:
#             companion = self.companions[HolderCircle.idx]
#             print(HolderCircle.lock)
# #             print(HolderCircle.lock.get_munu)
#             mu, nu = HolderCircle.lock.get_munu()
#             companion.set_munu(mu,nu)

        # turn off the rect animation property and reset the background
        HolderCircle.lock.set_animated(False)
        HolderCircle.lock = HolderCircle.idx = None

        self.background = None
        
        if self.companion is not None:
            self.companion.set_animated(False)
            self.companion.background = None
            self.companion = None
        # redraw the full figure
        self.axes.figure.canvas.draw()

        

   
if __name__ == '__main__':
    a = 10

    universe = UniversalSet(set(range(50)))



    fig = plt.figure()
    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    


    ifs01 = IFS.random(universe, 1, randseed=1)

    indices, mus, nus, pis = ifs01.elements_split()
    
    ax = plt.subplot2grid((4,6), (0,0), rowspan=3, colspan=3)
#     ax_01, line2d1_01 = plot_triangular_(ax,
#                                     mus, nus, ifs01.get_range(), bins=19,
#                                     rotation={'x':45, 'y':0})



    
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
    # rects = ax.bar(range(10), [1]*10)
#     circ = HolderCircle(ax, (0.1,0.6), label='tuka')
     
    prop = PropertiesTriang(ax, ([0.1, 0.4, 0.6], [0.6, 0.4, 0.4]),radius=.01)
    prop.connect()
    # 
    # drs = []
    # for rect in rects:
    #     rect.set_facecolor("white")
    #     dr = EditableRectangle(rect, 0.3, 0.5)
    #     dr.connect()
    #     drs.append(dr)
     
    plt.show()