# draggable rectangle with the animation blit techniques; see
# http://www.scipy.org/Cookbook/Matplotlib/Animations
import numpy as np
import matplotlib.pyplot as plt


from matplotlib.patches import Rectangle
class EditableRectangle(object):
    lock = None # only one can be animated at a time
    flip = 1
    
    def __init__(self, rect_big, mu, nu, 
                 colmu=None, colnu=None,
                 companion=None, prop_triang=None):

        self.companion = companion
        self.prop_triang = prop_triang

        self.rect = rect_big

        x, y = rect_big.get_xy()
        height = rect_big.get_height()
        width  = rect_big.get_width()

        colmu = "blue" if colmu is None else colmu
        self.rect_mu = Rectangle((x,y), width, mu, facecolor=colmu)
        self.rect.axes.add_patch(self.rect_mu)

        colnu = "green" if colnu is None else colnu
        self.rect_nu = Rectangle((x,height - nu), width, nu, facecolor=colnu)
        self.rect.axes.add_patch(self.rect_nu)

        self.press_xy = None
        self.mu_data = None
        self.nu_data = None
        self.background = None

    
    def get_idx(self):
        return self.rect.get_x()
    
    def get_mu(self):
        return self.rect_mu.get_y()
    
    def get_nu(self):
        return self.rect.get_height() - self.rect_nu.get_y()
    
    def get_pi(self):
        return self.rect.get_height() - self.get_mu() - self.get_mu() 

    ## Setters
    def set_mu(self, mu):
        self.rect_mu.set_height(mu)
#         if self.companion is not None:
#             self.companion.set_mu(mu)

    def set_nu(self, nu):
        self.rect_nu.set_y(self.rect.get_height() - nu)
        self.rect_nu.set_height(nu)
#         if self.companion is not None:
#             self.companion.set_nu(nu)

    def set_munu(self, munu):
        self.set_mu(munu[0])
        self.set_nu(munu[1])

    def set_animated(self, value):
        self.rect_mu.set_animated(value)
        self.rect_nu.set_animated(value)

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
#         self.rect.figure.canvas.mpl_disconnect(self.ciddraw)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
#         self.ciddraw = self.rect.figure.canvas.mpl_connect(
#             'draw_event', self.draw_callback)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes:
            return
        if EditableRectangle.lock is not None:
            return
        contains, attrd = self.rect.contains(event)
        if not contains:
            return
        
        if self.rect_mu.contains(event)[0]:
            self.update_flag = "update_mu"
        elif self.rect_nu.contains(event)[0]:
            self.update_flag = "update_nu"
        else:
            self.update_flag = "update_pi"

        self.mu_data = self.rect_mu.get_y(), self.rect_mu.get_height()
        self.nu_data = self.rect_nu.get_y(), self.rect_nu.get_height()
        self.press_xy =  event.xdata, event.ydata

        EditableRectangle.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        
        self.set_animated(True)
        
        if self.companion is not None:
            self.companion.set_animated(True)
     
        canvas.draw()
        
        
        self.background = canvas.copy_from_bbox(self.rect.axes.figure.bbox)
        
        # now redraw just the rectangle
        axes.draw_artist(self.rect_mu)
        axes.draw_artist(self.rect_nu)
        # and blit just the redrawn area
        canvas.blit(axes.bbox)

        if self.companion is not None:
            self.prop_triang.background = \
                canvas.copy_from_bbox(self.companion.axes.figure.bbox)
            self.update_companion()
#         self.prop_triang.draw_blit(self.companion)


    def draw_callback(self, event):

#         self.draw_holder_annotations(self.axes)
        self.rect.axes.draw_artist(self.rect_mu)
        self.rect.axes.draw_artist(self.rect_nu)
            
        canvas = self.rect.axes.figure.canvas
        canvas.blit(self.rect.axes.bbox)        
        self.background = canvas.copy_from_bbox(self.rect.axes.figure.bbox)

    def update_companion(self):
        self.companion.set_mu(self.rect_mu.get_height())
        self.companion.set_nu(1-self.rect_nu.get_y())
#         self.prop_triang.draw_blit(self.companion)
        self.companion.draw_on(self.prop_triang.axes)
        self.prop_triang.axes.figure.canvas.blit(self.prop_triang.axes.bbox)


    def update_nu(self, event):
        xpress, ypress = self.press_xy
        dy = event.ydata - ypress

        nu_y, nu_height = self.nu_data
        nu_y = max(min(1.0, nu_y + dy), 0.0)
        self.rect_nu.set_y(nu_y)
        self.rect_nu.set_height(self.rect.get_height() - nu_y)

        mu_height = self.rect_mu.get_height()
        if mu_height > nu_y:
            self.rect_mu.set_height(nu_y)


    def update_mu(self, event):
        xpress, ypress = self.press_xy
        dy = event.ydata - ypress

        mu_y, mu_height = self.mu_data
        self.rect_mu.set_height(min(max(0.0, mu_height + dy),
                                    self.rect.get_height()))

        nu_y = self.rect_nu.get_y()
        mu_height = self.rect_mu.get_height()   
        if mu_height > nu_y:
            self.rect_nu.set_y(mu_height)
            self.rect_nu.set_height(self.rect.get_height() - mu_height)

        
    def update_pi(self, event):
        xpress, ypress = self.press_xy
        dx = event.xdata - xpress
        dy = event.ydata - ypress

        mu_y, mu_height = self.mu_data
        self.rect_mu.set_height(max(0.0, mu_height + dy))
        
        nu_y, nu_height = self.nu_data
        self.rect_nu.set_y(min(1.0, nu_y + dy))
        self.rect_nu.set_height(max(0.0, nu_height - dy))

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if EditableRectangle.lock is not self:
            return
        if event.inaxes != self.rect.axes:
            return

        if self.update_flag == "update_pi":
            self.update_pi(event)
        elif self.update_flag == "update_mu":
            self.update_mu(event)
        else:
            self.update_nu(event)

        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        # restore the background region
        canvas.restore_region(self.background)
        self.draw_object()
        # blit just the redrawn area
        canvas.blit(axes.bbox)

        if self.companion is None:
            return
        self.update_companion()

        
    def draw_blit(self):
        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        self.draw_object()

        # blit just the redrawn area
        canvas.blit(axes.bbox)
     
    def draw_object(self):
        axes = self.rect.axes
        axes.draw_artist(self.rect_mu)
        axes.draw_artist(self.rect_nu)      
           

    def on_release(self, event):
        'on release we reset the press data'
        if EditableRectangle.lock is not self:
            return

        self.press_xy = None
        self.mu_xy = None
        self.nu_xy = None
        EditableRectangle.lock = None

        # turn off the rect animation property and reset the background
        self.set_animated(False)

        if self.companion is not None:
            self.companion.set_animated(False)
            self.companion.background = None
            self.background = None

        # redraw the full figure
        self.rect.figure.canvas.draw()


import numpy as np

class PropertiesBar(object):
    
    def __init__(self, label,
                       mus,
                       nus,
                       ax=None,
#                        radius=5,
#                        annotations=None,
                       alpha=0.5, 
                       hide_ifs=False,
#                        show_ann=True,
#                        showverts=True,
#                        showedges=False,
                       showlabels=False):
        assert(len(mus)==len(nus))
        self.label = label
        self.ax = ax
        self.indices = np.arange(len(mus)) 
        self.mus = np.asarray(mus)
        self.nus = np.asarray(nus)
        self.pis = 1.0 - self.nus - self.mus
#         self.mubar = ax.bar(self.indices, mus, color='b',
#                 label='Membership')
# #         ax.bar(indices, pis, bottom=mus, color='c',
# #                 label='Indeterminacy')    
#         self.nubar = ax.bar(self.indices, self.nus, bottom=[m+p for m,p in zip(mus,self.pis)],
#                 color='g',
#                 label='Non-membership')
        self.bar = ax.bar(self.indices, [1.0]*len(self.indices))
        self.editable_rects = [Rectangle((0,0), 1, 1)] * len(self.indices)

        for idx, (rect, mu, nu) in enumerate(zip(self.bar, self.mus, self.nus)):
            rect.set_facecolor("white")
            er = EditableRectangle(rect, mu, nu)
#             er.connect()
            self.editable_rects[idx] = er


        self.alpha = alpha 
        self.hide_ifs = hide_ifs
        
    def connect(self):
        for er in self.editable_rects:
            er.connect()
            
    def disconnect(self):
        for er in self.editable_rects:
            er.disconnect()

    # Setters
    def set_x(self, mus):
        for mu, er in zip(mus, self.editable_rects):
            er.set_mu(mu)
            
    def set_y(self, nus):
        for nu, er in zip(nus, self.editable_rects):
            er.set_mu(nu)
            
    def set(self, mus, nus):
        for mu, nu, er in zip(mus, nus, self.editable_rects):
            er.set_munu((mu, nu))       
    
    # Getters
    def get_x(self):
        return np.array([rect.get_mu() for rect in self.editable_rects])
    
    def get_y(self):
        return np.array([rect.get_nu() for rect in self.editable_rects])

    def get_data_pair(self):
        return (self.get_x(), self.get_y())
    
    def get_data(self):
        return np.array([(r.get_mu(), r.get_nu()) for r in self.editable_rects])
        
        
if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # rects = ax.bar(range(10), [1]*10)
    
    prop = PropertiesBar("proba01", [0.1, 0.4, 0.6],
                                    [0.6, 0.4, 0.4], ax=ax)
    prop.connect()
    # 
    # drs = []
    # for rect in rects:
    #     rect.set_facecolor("white")
    #     dr = EditableRectangle(rect, 0.3, 0.5)
    #     dr.connect()
    #     drs.append(dr)
    
    plt.show()