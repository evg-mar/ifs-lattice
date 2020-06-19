from editable_circle import HolderCircle
# from ifs_properties_plot import TopoConst, TopoConstInteractive
from topo_const_triang import TopoConstTriangInteractive

import abc

import numpy as np
import matplotlib.pyplot as plt
import collections
import json
import os

import collections as col

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
                       label_id='ifs_001',
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
        self.annotation_size = annotation_size
        self.alpha_marker = alpha_marker
        self.annotation_visible = show_annotation
        self.colors = colors
        self.label_id = label_id
        self.visible = visible
        
        self.canvas = self.axes.figure.canvas
        
        if init_flag:
            self.__init(bins, colors)
                             
        self.holder = []

        self.radia = radius if isinstance(radius, collections.Iterable) \
                             else [radius]*len(self.labels)

        for label, rad, mu, nu in zip(self.labels, self.radia, *musnus):

            obj = HolderCircle(axes, (mu,nu), rad,
                               annotation_size=annotation_size,
                               show_annotation=show_annotation,
                               label=str(label),
                               color=colors['elem'],
                               picker=picker,
                               alpha_marker=alpha_marker,
                               visible=visible)

            self.holder.append(obj)

    def get_color(self):
        return self.colors['elem']
            
    def get_visible(self):
        return self.visible
        
    def set_visible(self, visible):
        self.visible = visible
        for circle in self.holder:
            circle.set_visible(visible)
            
    def get_annotation_visible(self):
        return self.annotation_visible
    
    def set_annotation_visible(self, show_annotation):
        self.annotation_visible = show_annotation
        for circle in self.holder:
            circle.set_annotation_visible(show_annotation)
        
    def get_radius(self):
        return self.radia[0] if isinstance(self.radia, collections.Iterable) \
                else self.radia
            
    def set_radius(self, radius):
        self.radia = [radius]*len(self.labels)
        for rad, circle in zip(self.radia, self.holder):
            circle.set_radius(rad)            
                
    def get_annotation_size(self):
        return self.annotation_size
        
    def set_annotation_size(self, annotation_size):
        for circle in self.holder:
            circle.set_annotation_size(annotation_size)
            
    def get_alpha_marker(self):
        return self.alpha_marker 
            
    def set_alpha_marker(self, alpha_contrast):
        self.alpha_marker = alpha_contrast
        for circle in self.holder:
            circle.set_alpha(alpha_contrast)
            
    def get_data(self):
        return np.array(list(map(lambda obj: obj.center, self.holder)))
     

    def get_data_pair(self):
        mus = map(lambda obj: obj.get_center()[0], self.holder) 
        nus = map(lambda obj: obj.get_center()[1], self.holder)
        return np.array(list(mus)), np.array(list(nus)) 

    ######
    def save_to_json(self, json_path):
        data = self.get_data() 
        print('In save to Json')
        print(data)
        print(data[:,0])
        print(data[:,1])
        data_lst = list(zip(data[:,0], data[:,1]))
        print(data_lst)
        data = collections.OrderedDict(list(enumerate(data_lst)))
        # data = dict(data)
        print(len(data))
        print(data)
        
        tmp_holder = collections.OrderedDict([('data', data),
                                 #('data', list(zip(data[0], data[1]))),
                                 # ('radius', self.radius),
                                 ('contrast', self.get_alpha_marker()),
                                 ('labels_size', self.get_annotation_size()),
                                 ('color', self.get_color()),
                                 #('marker', self.holder.get_marker()),
                                 ('marker_size', self.get_radius()),
                                 ('label', self.label_id)])
        
        with open(json_path, 'w+') as fp:
            json.dump(tmp_holder, fp, indent=4)        
        
        print('Saving property: ' + json_path)
        
    @property
    def default_path(self):
        path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                            '..', 
                                            'working_dir',
                                            self.label_id + "_.json"))
        return path
        
    def save_to_json_default(self, event): 
        path = self.default_path
        print('Default Path: ', path)
        self.save_to_json(path )


#    @classmethod
#    def from_json(cls, json_path, ax, bins, rotation, 
#                  color=None, marker=None, alpha=None):
#        
#        with open(json_path) as data_file:    
#            data = json.load(data_file, object_pairs_hook=col.OrderedDict)
#            #assert set(data.keys())==set(['data','radius','alpha_marker',
#            #                              'labels_size'])
#   
#            marker = marker if marker is not None else data['marker']
#            alpha = alpha if alpha is not None else data['contrast']
#            color = color if color is not None else data['color']
#   
#            ifs_holder = list(data['data'].values())
#            indices = range(len(ifs_holder))
#            dat = list(map(tuple, ifs_holder))
#            mus, nus = list(zip(*dat))
#            mus, nus = list(mus), list(nus)
#            print(mus)
#
#            print(nus)
#                         
#            ax_01, line2d1_01 = plot_triangular_(ax,
#                                            mus, nus, rang=1.0, bins=10,
#                                            rotation={'x':45, 'y':0},
#                                            color=color,
#                                            marker=marker,
#                                            alpha=alpha)
#            ax_01.set_ylabel(r'$\nu$', fontsize=20)
#            ax_01.set_xlabel(r'$\mu$', fontsize=20)
#            
#            line2d1_01.set_linestyle(' ')
#            line2d1_01.set_markersize(data['marker_size'])
#            line2d1_01.set_markerfacecolor(color)
#            line2d1_01.set_color(color)
#        #     line2d1_01.set_marker(marker=r'$\odot$')
#            line2d1_01.set_marker(marker=marker)    
#            line2d1_01.set_zorder(2)
#            # ax_01.set_aspect('equal', 'datalim')
#
#            prop = PropertiesIFS(label='ifs01_ax01', 
#                                 holder=line2d1_01,
#                                 labels_size=data['labels_size'])
#            prop.init_default(ax)
#            return prop
               
###############################################################################
        

class IfsTriangInteractive(IfsTriang):
    def __init__(self,axes, axes_metrics,
                       musnus,
                       radius=0.01,
                       companions=col.OrderedDict([]),
                       metrics_unary=col.OrderedDict([]),
                       metrics_binary=col.OrderedDict([]),
                       widgets=None,
                       label_id = '',
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
                                                   label_id,
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

        self.companions     = companions
        self.metrics_unary  = metrics_unary
        self.metrics_binary = metrics_binary
        
        self.widgets        = widgets
        
        # self.companion = None
        self.companion_elements = None
        self.axes_metrics       = axes_metrics

        
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

        self.table_unary = None        
        self.table_binary = None
        self.update_tables()

        
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
            self.companion_elements = [(key, comp[0], comp[1].holder[self.activeCircle.idx]) \
                                       for key, comp in self.companions.items()]
            for key, action, companion_elem in self.companion_elements:
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
#        print(type(self.x2Dline))
        

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
            for key, action, comp_elem in self.companion_elements:
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

    def sync_companions(self):
        if len(self.companions) > 0:                
            ### companion elements
            companion_elements = [(key, comp[0], comp[1].holder[self.activeCircle.idx]) \
                                       for key, comp in self.companions.items()]            
            for xdata, ydata in self.get_data():
                ### companion_elements
                for key, action, comp_elem in companion_elements:
                    comp_elem.set_munu(action(xdata, ydata))
                    comp_elem.draw_object()
        
        

    def draw_blit(self, obj):          
        obj.draw_object()
        self.axes.figure.canvas.blit(self.axes.bbox)

        
    def update_tables(self):
        companion_elements_musnus = collections.OrderedDict([('A', self.get_data_pair())] + \
                            [(key, comp[1].get_data_pair()) \
                              for key, comp in self.companions.items() \
                              if comp[1].get_visible()])

        # binary operations
        rows = [k for k in self.metrics_binary.keys()]   
        rows_ = [ ]
        cols = []
        cell_text = []

        size_ifs = len(companion_elements_musnus['A'][0])

        for key, musnus in companion_elements_musnus.items():
            #if key == 'A' or  self.companions[key][1].get_visible():
            cols.append('i(A , '+key+')')
            
            holder = self.metrics_binary['incl_j']((companion_elements_musnus['A'],
                                           musnus))
            print(holder)
            print(list(holder.values()))
            rows_ = list(holder.keys())
            cell_text.append(list(map(lambda x: (x[0]/size_ifs, x[1]/size_ifs) \
                                      if isinstance(x, tuple) else x/size_ifs, 
                                 list(holder.values()) ))  )
    
        cell_text = list(map(list, zip(*cell_text)))
        cell_text = [list(map(str, ro)) for ro in cell_text]

        if self.table_binary is not None:
            self.table_binary.remove()

        self.table_binary =  self.axes.table(cellText=cell_text, # cell_text,
                      rowLabels=rows_,
                      cellColours=None,
                      #rowColours=colors,
#                          rowLoc='top',
                      colLabels=cols,
                      loc='right')
        
        
        # unary operations
        rows_u = [k for k in self.metrics_unary.keys()]        
        cols_u = []
        cell_text_u = []

        for key, mus_nus in companion_elements_musnus.items():
            #if key == 'A' or  self.companions[key][1].get_visible():
            cols_u.append(key)
            cell_text_u.append([self.metrics_unary[r](mus_nus) \
                for r in self.metrics_unary.keys()])
    
        cell_text_u = list(map(list, zip(*cell_text_u)))


        if self.table_unary is not None:
            self.table_unary.remove()

#        self.table_unary =  self.axes.table(cellText=cell_text_u, # cell_text,
#                      rowLabels=rows_u,
#                      cellColours=None,
#                      #rowColours=colors,
#                      colLabels=cols_u,
#                      loc='right')    
        

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

        
        if len(self.companions) > 0:

            self.update_tables()

            for key, action, comp_elem in self.companion_elements:
#                cols.append(key)
                comp_elem.set_animated(False)
                
                comp_elem.background = None
                
            self.companion_elements = None

            
        self.x2Dline.set_visible(False)    
        self.y2Dline.set_visible(False)    
        self.x2Dline.set_animated(False)    
        self.y2Dline.set_animated(False)    
           
        # redraw the full figure
        self.axes.figure.canvas.draw()

    def save_to_json_default(self, event):
        super().save_to_json_default( event)
        print(self.companions)
        for key, companion in self.companions.items():
            companion[1].save_to_json_default(event)

        
#############

#############        



class IfsTriangTopoConstInteractive(IfsTriangInteractive):
    def __init__(self,
                 axes, axes_metrics,
                 musnus,
                 topo_const_triang,
                 radius=0.01,
                 companions=col.OrderedDict([]),
                 metrics_unary=col.OrderedDict([]),
                 metrics_binary=col.OrderedDict([]),
                 widgets=None,
                 label_id = '',
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
        super(IfsTriangTopoConstInteractive, self).__init__(
            axes=axes,
            axes_metrics=axes_metrics,
            musnus=musnus,
            # topo_const_triang,
            radius=radius,
            companions=companions,
            metrics_unary=metrics_unary,
            metrics_binary=metrics_binary,
            widgets=widgets,
            label_id = label_id,
            labels=labels,
            picker=picker,
            alpha_marker=alpha_marker,
            visible=visible,
            annotation_size=annotation_size,
            show_annotation=show_annotation,
            colors = colors,
            bins = bins,
            init_flag=init_flag)
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
    
    # ax = plt.subplot2grid((5,7), (0,0), rowspan=3, colspan=3)

    ax02 = plt.subplot2grid((5,7), (0,4), rowspan=4, colspan=4)

#    topoconst = TopoConstTriangInteractive(ax, 0.6, 0.2, 0.5)
#
#    ifs_topoconst = IfsTriangTopoConstInteractive(ax, (mus,nus), topoconst)
#    ifs_topoconst.connect()
#    

    ifs02 = IFS.random(universe, 1, randseed=2)
    indices2, mus2, nus2, pis2 = ifs02.elements_split()

    metrics_unary = { 'Mean_mu': lambda musnus: np.mean(musnus[0]),
                      'Mean_nu': lambda musnus: np.mean(musnus[1])                      
                     
                     }

    from ifs_operators_plot import incl_i
    import collections as cols


    metrics_binary = \
        cols.OrderedDict([ ('incl_j',
                            lambda musnus1_musnus2: incl_i(musnus1_musnus2[0], musnus1_musnus2[1]))])


    ###################################################################################################

    # ifs_triang02 = IfsTriangInteractive(ax, axes_metrics=ax02,
    #                                         metrics_unary= metrics_unary,
    #                                         metrics_binary=metrics_binary,
    #                                         musnus=(mus2, nus2))
    # ifs_triang02.connect()
    #
    # from widgets_operators import WidgetsSimpleOperator
    #
    #
    # widgets = WidgetsSimpleOperator(active_prop=ifs_triang02,
    #                                 canvas=ifs_triang02.canvas)
    #
    # widgets.recreate_widgets_(ifs_triang02)



##############################################################################################################

    topoconst = TopoConstTriangInteractive(ax, 0.6, 0.2, 0.5)

    # ifs_topoconst = IfsTriangTopoConstInteractive(ax, (mus,nus), topoconst)
    # ifs_topoconst.connect()



    ifs_triang02 = IfsTriangTopoConstInteractive(ax, axes_metrics=ax02,
                                        topo_const_triang=topoconst,
                                        metrics_unary= metrics_unary,
                                        metrics_binary=metrics_binary,
                                        musnus=(mus2, nus2))
    ifs_triang02.connect()

    from widgets_operators import WidgetsSimpleOperator


    widgets = WidgetsSimpleOperator(active_prop=ifs_triang02,
                                    canvas=ifs_triang02.canvas)

    widgets.recreate_widgets_(ifs_triang02)


plt.show()