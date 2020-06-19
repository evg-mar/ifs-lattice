#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 23:25:03 2018

@author: evgeniy
"""

# draggable rectangle with the animation blit techniques; see
# http://www.scipy.org/Cookbook/Matplotlib/Animations
from matplotlib.patches import Rectangle


class RectangleBasic(object):

    def __init__(self, rect_big, mu, nu, 
                 color_mu=None, color_nu=None, alpha=0.5):
        
        self.rect = rect_big
        self.axes = self.rect.axes
#         self.rect.axes.set_ylim([0,1])

        x, y = rect_big.get_xy()
        height = rect_big.get_height()
        width  = rect_big.get_width()

        color_mu = "blue" if color_mu is None else color_mu
        self.rect_mu = Rectangle((x,y), width, mu, color=color_mu, alpha=alpha)
        self.axes.add_patch(self.rect_mu)

        color_nu = "green" if color_nu is None else color_nu
        self.rect_nu = Rectangle((x,height - nu), width, nu, color=color_nu, alpha=alpha)
        self.rect.axes.add_patch(self.rect_nu)


class EditableRectangle(RectangleBasic):
    lock = None # only one can be animated at a time
    
    def __init__(self, rect_big, mu, nu, 
                 color_mu=None, color_nu=None, alpha=0.5,
                 companion=None):
        super(EditableRectangle, self).__init__(rect_big, mu, nu,
                                             color_mu, color_nu, alpha)

        self.companion = companion

        self.press_xy = None
        self.mu_data = None
        self.nu_data = None
        
        self.background = \
            self.rect.figure.canvas.copy_from_bbox(self.axes.figure.bbox)


    @property
    def get_idx(self):
        return self.rect.get_x()
  
    @property    
    def get_mu(self):
        return self.rect_mu.get_y()
    
    @property
    def get_nu(self):
        return self.rect.get_height() - self.rect_nu.get_y()
    
    @property    
    def get_pi(self):
        return self.rect.get_height() - self.get_mu - self.get_mu 

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
        
    def set_data(self, mu, nu):
        self.set_munu((mu, nu))

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
            print("companion of rectangle set animated True")
#             self.companion.background = \
#                 canvas.copy_from_bbox(self.companion.axes.figure.bbox)
            self.companion.set_animated(True)
     
        canvas.draw()        
        
        self.background = canvas.copy_from_bbox(self.axes.figure.bbox)
        
        # now redraw just the rectangle
        axes.draw_artist(self.rect_mu)
        axes.draw_artist(self.rect_nu)
        # and blit just the redrawn area
        canvas.blit(axes.bbox)

        if self.companion is not None:
            self.companion.background = \
                canvas.copy_from_bbox(self.companion.axes.figure.bbox)
            self.update_companion()


    def draw_callback(self, event):

#         self.draw_holder_annotations(self.axes)
        self.rect.axes.draw_artist(self.rect_mu)
        self.rect.axes.draw_artist(self.rect_nu)
            
        canvas = self.rect.axes.figure.canvas
        canvas.blit(self.rect.axes.bbox)        
        self.background = canvas.copy_from_bbox(self.rect.axes.figure.bbox)

    def update_companion(self):
#         self.companion.set_mu(self.rect_mu.get_height())
#         self.companion.set_nu(1-self.rect_nu.get_y())
        self.companion.set_data(self.rect_mu.get_height(),
                                1-self.rect_nu.get_y())

        self.companion.draw_object()
        self.companion.axes.figure.canvas.blit(self.companion.axes.bbox)


    def update_nu(self, event):
        xpress, ypress = self.press_xy
        dy = event.ydata - ypress

        nu_y, nu_height = self.nu_data
        nu_y = max(min(1.0, nu_y + dy), 0.0)
#         self.rect_nu.set_y(nu_y)
#         self.rect_nu.set_height(self.rect.get_height() - nu_y)
        self.set_nu(self.rect.get_height() - nu_y)

        mu_height = self.rect_mu.get_height()
        if mu_height > nu_y:
            self.set_mu(nu_y)
#             self.rect_mu.set_height(nu_y)


    def update_mu(self, event):
        xpress, ypress = self.press_xy
        dy = event.ydata - ypress

        mu_y, mu_height = self.mu_data
        self.set_mu(min(max(0.0, mu_height + dy),
                        self.rect.get_height()))

        nu_y = self.rect_nu.get_y()
        mu_height = self.rect_mu.get_height()   
        if mu_height > nu_y:
            self.set_nu(self.rect.get_height() - mu_height)
#             self.rect_nu.set_y(mu_height)
#             self.rect_nu.set_height(self.rect.get_height() - mu_height)

        
    def update_pi(self, event):
        xpress, ypress = self.press_xy
        dx = event.xdata - xpress
        dy = event.ydata - ypress

        mu_y, mu_height = self.mu_data
        self.set_mu(max(0.0, mu_height + dy))
#         self.rect_mu.set_height(max(0.0, mu_height + dy))
        
        nu_y, nu_height = self.nu_data

#         self.rect_nu.set_y(min(1.0, nu_y + dy))
        self.set_nu(max(0.0, nu_height - dy))
#         self.rect_nu.set_height(max(0.0, nu_height - dy))


    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if EditableRectangle.lock is not self:
            return
        if event.inaxes != self.axes:
            return

        if self.update_flag == "update_pi":
            self.update_pi(event)
        elif self.update_flag == "update_mu":
            self.update_mu(event)
        else:
            self.update_nu(event)

        canvas = self.rect.figure.canvas
        # restore the background region
        canvas.restore_region(self.background)
        self.draw_object()
        # blit just the redrawn area
        canvas.blit(self.axes.bbox)

        if self.companion is not None:
            canvas.restore_region(self.companion.background)
            self.update_companion()

        
    def draw_blit(self):
        canvas = self.rect.figure.canvas
        # restore the background region
        canvas.restore_region(self.background)


        # blit just the redrawn area
        canvas.blit(self.axes.bbox)
     
    def blit(self):
        canvas = self.rect.figure.canvas
        # restore the background region
        canvas.restore_region(self.background)
        # blit just the redrawn area
        canvas.blit(self.axes.bbox)


    def draw_object(self):

        self.axes.draw_artist(self.rect_mu)
        self.axes.draw_artist(self.rect_nu)      
           

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
            # self.rect.figure.canvas.restore_region(self.companion.background)
            # self.update_companion()

            self.companion.set_animated(False)
#             self.companion.background = None
#             self.background = None

        # redraw the full figure
        self.rect.figure.canvas.draw()

###############################################################################       
        
class EditableRectangleRadius(EditableRectangle):
    
    def update_companion(self):
#         self.companion.set_mu(self.rect_mu.get_height())
#         self.companion.set_nu(1-self.rect_nu.get_y())
#        self.companion.set_data(self.rect_mu.get_height(),
#                                1-self.rect_nu.get_y())
        self.companion.set_radius(self.rect_mu.get_height())
    
        self.companion.draw_object()
        self.companion.axes.figure.canvas.blit(self.companion.axes.bbox)
