# draggable rectangle with the animation blit techniques; see
# http://www.scipy.org/Cookbook/Matplotlib/Animations

from matplotlib.patches import Circle


class HolderCircle(Circle):
    
    def __init__(self, axes, munu,
                       radius=0.01,
                       annotation_size=12,
#                        visible=True,
                       show_annotation=True,
                       edgecolor="black",
                       alpha_marker=0.5,
#                        showvert=True,
                       **kwargs):
        super(HolderCircle, self).__init__(xy=munu,
                                           radius=radius,
                                           edgecolor=edgecolor,
                                           alpha=alpha_marker,
                                           **kwargs)
        self.set_edgecolor(edgecolor)
        self.lock =None
        self.idx  = None
        
        self.axes = axes
        self.axes.add_patch(self)
        self.annotation = None
        # label, facecolor, edgecolor, get_visible, get_alpha

        if self.get_label() != '' and show_annotation == True:
            self.create_annotation(annotation_size, self._label)

        self.active_objects = {self.annotation: True}
        
        self.background = \
            self.axes.figure.canvas.copy_from_bbox(self.axes.figure.bbox)

    
    
    def __str__(self):
        return self._label + super(HolderCircle, self).__str__()
    
    def set_annotation_visible(self, show_annotation):
        self.annotation.set_visible(show_annotation)
        
    def get_annotation_visible(self):
        return self.annotation.get_visible()
        
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
    
    # @property
    def annotation_size(self):
        return self.annotation.get_fontsize()

    # @property
    def set_annotation_size(self, annotation_size):
        return self.annotation.set_fontsize(annotation_size)        
        
    def draw_blit(self):
        canvas = self.axes.figure.canvas
#        canvas = self.rect.figure.canvas
        # restore the background region
        canvas.restore_region(self.background)


        # blit just the redrawn area
        canvas.blit(self.axes.figure.bbox)
            
            
    def draw_object(self):
        self.axes.draw_artist(self)
        for obj, active_flag in self.active_objects.items():
            if active_flag:
                self.axes.draw_artist(obj)

    def add_object(self, axes):
        self.axes.add_patch(self)
#         for obj, active_flag in self.active_objects.items():
#             if active_flag:
#                 axes.add_artist(obj)

#     @property
    def get_munu(self):
        return self.center
        
    def get_center(self):
        return self.center
    
    def set_mu(self, mu):      
        mu_ = min(max(0.0, mu), 1.0) 
        self.center = mu_, self.center[1]
        if hasattr(self, 'annotation'):
            ann = self.annotation
            ann.xy = ann.xyann = ann.xytext = (mu_, self.center[1])        

    def set_nu(self, nu):
        nu_ = min(max(0.0, nu), 1.0) 
        self.center = self.center[0], nu_
        if hasattr(self, 'annotation'):
            ann = self.annotation
            ann.xy = ann.xyann = ann.xytext = (self.center[0], nu_)           
    
    def set_munu(self, munu):
        mu_ = min(max(0.0, munu[0]), 1.0) 
        nu_ = min(max(0.0, munu[1]), 1.0)
        if mu_ + nu_ >= 1:
            self.center = ((mu_-nu_+1)/2, (nu_-mu_+1)/2) 
        else:
            self.center = (mu_, nu_)

        if hasattr(self, 'annotation'):
            print('has annotation...')
            ann = self.annotation
            ann.xy = ann.xyann = ann.xytext = self.center
            
    def set_data(self, mu, nu):
        self.set_munu((mu, nu))
            
    @property
    def get_text(self):
        return self.annotation.get_text()

