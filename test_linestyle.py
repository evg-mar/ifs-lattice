# draggable rectangle with the animation blit techniques; see
# http://www.scipy.org/Cookbook/Matplotlib/Animations
import numpy as np
import matplotlib.pyplot as plt


from matplotlib.patches import Rectangle
class EditableRectangle(object):
    lock = None # only one can be animated at a time
    
    def __init__(self, rect_big, mu, nu, colmu=None, colnu=None):
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

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
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
            print("press update mu")
            self.update_flag = "update_mu"
        elif self.rect_nu.contains(event)[0]:
            print("press update nu")
            self.update_flag = "update_nu"
        else:
            self.update_flag = "update_pi"
            print("press update pi")
            
        print('event contains', self.rect.xy)
        
        self.mu_data = self.rect_mu.get_y(), self.rect_mu.get_height()
        self.nu_data = self.rect_nu.get_y(), self.rect_nu.get_height()
        self.press_xy =  event.xdata, event.ydata
        
        EditableRectangle.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        self.rect_mu.set_animated(True)
        self.rect_nu.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.rect.axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.rect_mu)
        axes.draw_artist(self.rect_nu)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)

    def update_nu(self, event):
        xpress, ypress = self.press_xy
        dx = event.xdata - xpress
        dy = event.ydata - ypress

        nu_y, nu_height = self.nu_data
        ny_y = max(min(1.0, nu_y + dy), 0.0)
        self.rect_nu.set_y(nu_y)
        self.rect_nu.set_height(self.rect.height() - nu_y)

        mu_height = self.rect_mu.get_height()
        if mu_height > nu_y:
            self.rect_mu.set_height(nu_y)

    def update_mu(self, event):
        xpress, ypress = self.press_xy
        dx = event.xdata - xpress
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
            print("update_pi")
            self.update_pi(event)
        elif self.update_flag == "update_mu":
            print("update_mu")
            self.update_mu(event)
        else:
            self.update_nu(event)

        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.rect_mu)
        axes.draw_artist(self.rect_nu)      

        # blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_release(self, event):
        'on release we reset the press data'
        if EditableRectangle.lock is not self:
            return

        self.press_xy = None
        self.mu_xy = None
        self.nu_xy = None
        EditableRectangle.lock = None

        # turn off the rect animation property and reset the background
        self.rect_mu.set_animated(False)
        self.rect_nu.set_animated(False)
        self.background = None

        # redraw the full figure
        self.rect.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)



fig = plt.figure()
ax = fig.add_subplot(111)
rects = ax.bar(range(10), [1]*10)
drs = []
for rect in rects:
#     rect.set_facecolor("white")
    rect.set_visible(False)
    dr = EditableRectangle(rect, 0.3, 0.5)
    dr.connect()
    drs.append(dr)

plt.show()