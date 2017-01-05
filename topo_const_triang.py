
class TopoConst(object):
    def __init__(self, ax, alpha, beta, gamma):

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        self.axes = ax
        self.alpha2dline, = ax.plot([alpha]*3,
                                  [0.0, beta,  1-alpha],
                                  color='r')
        
        self.beta2dline, = ax.plot([0.0, alpha, 1 - beta],
                                  [beta]*3,
                                  color='g')


    def set_animated(self,value):
        self.alpha2dline.set_animated(value)
        self.beta2dline.set_animated(value)
        
    def set_topoconst(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        
        self.alpha2dline.set_data([alpha]*3,
                                  [0.0, beta,  1-alpha])
        self.beta2dline.set_data([0.0, alpha, 1 - beta],
                                  [beta]*3)

    def draw_topo_object(self):
        self.axes.draw_artist(self.alpha2dline)
        self.axes.draw_artist(self.beta2dline)
        
    def set_visible(self, flag):
        self.alpha2dline.set_visible(flag)
        self.beta2dline.set_visible(flag)
    
    def get_visible(self):
        return self.alpha2dline.get_visible() and \
               self.beta2dline.get_visible()


class TopoConstTriangInteractive(TopoConst):
    
    def __init__(self, ax, alpha, beta, gamma, companion=None):
        super(TopoConstTriangInteractive, self).__init__(ax, alpha, beta, gamma)
        self.companion = companion
        self.active_artists = []
        
        self.alpha2dline.set_picker(5)
        self.beta2dline.set_picker(5)
        
        self.background = self.axes.figure.canvas.copy_from_bbox(
                                                        self.axes.figure.bbox)

#     def set_all_active(self):
#         self.active_artists = [self.alpha2d]

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

    def set_data(self, alpha, beta):
#         if self.alpha2dline in self.active_artists:
        self.alpha = alpha
        self.alpha2dline.set_data([alpha]*3,
                                  [0.0, beta,  1-alpha])
#         if self.beta2dline in self.active_artists:
        self.beta = beta
        self.beta2dline.set_data([0.0, alpha, 1 - beta],
                                 [beta]*3)

    
    
    def set_topoconst_active(self, alpha, beta):
        if self.alpha2dline in self.active_artists:
            self.alpha = alpha
            self.alpha2dline.set_data([alpha]*3,
                                      [0.0, beta,  1-alpha])
        if self.beta2dline in self.active_artists:
            self.beta = beta
            self.beta2dline.set_data([0.0, alpha, 1 - beta],
                                     [beta]*3)

    def set_animated_active_artists(self, value):
        for a in self.active_artists:
            a.set_animated(value)


    def draw_active_artists(self):
        for a in self.active_artists:
            self.axes.draw_artist(a)
    
    def draw_all(self):
        self.axes.draw_artist(self.alpha2dline)
        self.axes.draw_artist(self.beta2dline)
        
    def draw_object(self):
        self.draw_all()
            
    def on_pick(self, event):

        if event.artist not in [self.alpha2dline, self.beta2dline]:
            return
        if len(self.active_artists) > 0:
            return

        if (self.alpha2dline.contains(event.mouseevent)[0] and \
           self.beta2dline.contains(event.mouseevent)[0]):
            self.active_artists = [self.alpha2dline, self.beta2dline]
        else:
            self.active_artists =[event.artist]

        
        self.set_animated_active_artists(True)

        canvas = self.axes.figure.canvas
        canvas.draw()

        self.background = canvas.copy_from_bbox(self.axes.figure.bbox)
        # now redraw just the rectangle
        self.draw_active_artists()

        # and blit just the redrawn area
        canvas.blit(self.axes.bbox)
        
        print("companion:", id(self.companion))
        if self.companion is not None:                
            print("companion...")
            self.companion.set_animated(True)
            canvas.draw()
            self.companion.draw_blit()


    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'

        if event.inaxes != self.axes:
            return
        if len(self.active_artists) == 0:
            return

        x, y = event.xdata, event.ydata
        if x <= 0 or y <= 0 or x + y >= 1:
            return

        self.set_topoconst_active(event.xdata, event.ydata)

        canvas = self.axes.figure.canvas
        canvas.restore_region(self.background)
        
        self.draw_active_artists()

        canvas.blit(self.axes.bbox)

        if self.companion is not None:
            print("update topo const bar....")
            self.companion.set_munu((event.xdata, event.ydata))
            self.companion.draw_object()
            canvas.blit(self.companion. axes.bbox)


    def draw_blit(self, obj):          
        obj.draw_object(self.axes)
        self.axes.figure.canvas.blit(self.axes.bbox)


    def on_release(self, event):
        'on release we reset the press data'
        if event.inaxes != self.axes:
            return
        if len(self.active_artists) == 0:
            return

        # turn off the rect animation property and reset the background
        self.set_animated_active_artists(False)
        self.active_artists = []
        
#         self.background = None
        
        if self.companion is not None:
            self.companion.set_animated(False)
#             self.companion.background = None
#             self.companion = None
        # redraw the full figure
        self.axes.figure.canvas.draw()
        
###########################################################


# class GammaTopoConstTriangInteractive(TopoConstTriangInteractive):
    


####################
if __name__ == '__main__':

    from universal_set import UniversalSet
    from intuitionistic_fuzzy_set import IFS
    from ifs_2Dplot import plot_triangular_

    import matplotlib.pyplot as plt

    universe = UniversalSet(set(range(50)))



    fig = plt.figure()
    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    


    ifs01 = IFS.random(universe, 1, randseed=1)

    indices, mus, nus, pis = ifs01.elements_split()
    
    ax = plt.subplot2grid((4,6), (0,0), rowspan=3, colspan=3)
    ax_01, line2d1_01 = plot_triangular_(ax,
                                    mus, nus, ifs01.get_range(), bins=19,
                                    rotation={'x':45, 'y':0})



    
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
    # rects = ax.bar(range(10), [1]*10)
# #     circ = HolderCircle(ax, (0.1,0.6), label='tuka')
#     prop = IfsTriang(ax, ([0.1, 0.4, 0.6], [0.6, 0.4, 0.4]),
#                                 radius=.01)
#     
    topoconst = TopoConstTriangInteractive(ax, 0.6, 0.2, 0.5)
    topoconst.connect()
#     prop.connect()
     
#     prop = IfsTriangInteractive(ax, ([0.1, 0.4, 0.6], [0.6, 0.4, 0.4]),
#                                 radius=.01)
# 
#     prop.connect()
    
     
    plt.show()   
    
    
    
    
    
