# draggable rectangle with the animation blit techniques; see
# http://www.scipy.org/Cookbook/Matplotlib/Animations
from matplotlib.patches import Rectangle
from editable_rectangle import EditableRectangle, RectangleBasic


class TopoConstBar(RectangleBasic):
    def __init__(self, rect_big, mu, nu, 
                 color_mu=None, color_nu=None):
        super(self.__class__, self).__init__(rect_big, mu, nu,
                                             color_mu, color_nu)
        x0, x1 = self.rect.axes.get_xlim()
        self.line2dalpha, = self.axes.plot([x0, x1], [mu, mu],
                                           color=color_mu)

        y0, y1 = self.rect.get_y(), self.rect.get_height()
        self.line2dbeta, = self.axes.plot([x0, x1], [y1-nu, y1-nu],
                                           color=color_nu)


class TopoConstBarInteractive(EditableRectangle):

    def __init__(self, rect_big, mu, nu, 
                 color_mu='orange', color_nu='red',
                 companion=None, prop_triang=None):
        super(TopoConstBarInteractive, self).__init__(rect_big, mu, nu,
                                                     color_mu, color_nu,
                                                     companion)

        # self.companion from EditableRetangle
        x0, x1 = self.rect.axes.get_xlim()
        self.line2dalpha, = self.axes.plot([x0, x1], [mu, mu],
                                           color=color_mu)

        y0, y1 = self.rect.get_y(), self.rect.get_height()
        self.line2dbeta, = self.axes.plot([x0, x1], [y1-nu, y1-nu],
                                           color=color_nu)

    ## Setters
    def set_mu(self, mu):
        super(TopoConstBarInteractive, self).set_mu(mu)
        self.rect_mu.set_height(mu)
        self.line2dalpha.set_ydata([mu, mu])
        
#         if self.companion is not None:
#             self.companion.set_mu(mu)

    def set_nu(self, nu):
        super(TopoConstBarInteractive, self).set_nu(nu)
        nu = self.get_nu
        height = self.rect.get_height()
        self.line2dbeta.set_ydata([height-nu, height - nu])

#         if self.companion is not None:
#             self.companion.set_nu(nu)
    def set_animated(self, value):
        super(TopoConstBarInteractive, self).set_animated(value)
        self.line2dalpha.set_animated(value)
        self.line2dbeta.set_animated(value)        

    def draw_object(self):
        super(TopoConstBarInteractive, self).draw_object()
        self.axes.draw_artist(self.line2dalpha)
        self.axes.draw_artist(self.line2dbeta)      

        
if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from ifs_bar_representation import IfsBar
    import matplotlib.pyplot as plt

    fig = plt.figure()

    axes1 = plt.subplot2grid((1,2), (0,0), rowspan=1, colspan=1)
    # rects = ax.bar(range(10), [1]*10)
    
    prop1 = IfsBar("static_bar", EditableRectangle,
                    ([0.1, 0.4, 0.6], [0.6, 0.4, 0.4]),
                    axes=axes1)
    prop1.connect()
    
    start_xlim, end_xlim = prop1.axes.get_xlim()
    width = 0.1
    rect = Rectangle((end_xlim, 0.0), width, 1.0, fc='white')

    prop1.axes.add_patch(rect)
    axes1.set_xlim([start_xlim, end_xlim + width])
    print(end_xlim + width)
    topo_const = TopoConstBarInteractive(rect, 0.3, 0.5, 
                                         color_mu='orange', color_nu='red')
    topo_const.connect()
    
    axes2 = plt.subplot2grid((1,2), (0,1), 
                             sharey=axes1, sharex=axes1,
                             rowspan=1, colspan=1)
    axes2.yaxis.set_label_position("left")
    prop2 = IfsBar( "proba02", RectangleBasic,
                    ([0.1, 0.4, 0.6], [0.6, 0.4, 0.4]), 
                    axes=axes2)

    plt.show()
