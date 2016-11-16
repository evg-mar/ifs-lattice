import matplotlib.pyplot as plt

from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons


class WidgetsBasic(object):
    line_active__  = 0
    index_active__ = 1
    
    slider_length__ = 0.1
    slider_hight__  = 0.015
    
    button_length__ = 0.1
    button_height__ = 0.1
    
    def __init__(self, canvas=None, active_prop=None):
        self.canvas = canvas
        self.active_prop = active_prop
        self.colors_ifs = { }
        self.props = []

    @property
    def prop_ifs(self):
        return self.active_prop[0]

    def recreate_widgets(self, # prop_ifs, 
                         idx_active, props, active_prop):
#         self.prop_ifs = active_prop[0]
        self.active_prop = active_prop
        self._recreate_active_ifs_radiobutton(idx_active, props)
        self._recreate_radius_slider()
        self._recreate_alpha_slider()
        self._recreate_textsize_slider()
        self._recreate_show_lines_check_button()
        

    def _recreate_active_ifs_radiobutton(self, idx_active, props):
        self.props = props

        axcolor = 'lightgoldenrodyellow'
        if hasattr(self, 'rax_activeifs'):
            self.rax_activeifs.cla()
        self.rax_activeifs = plt.axes([0.2+self.button_length__+0.01, 0.05, 
                                       self.button_length__,
                                       self.button_height__], axisbg=axcolor)
 
#             prop_ifs = self.active_lines_idx[self.ax_active][self.line_active__]
#             idx = self.axlines[self.ax_active].index(prop_ifs)
        activecolor = self.active_prop[0].get_color()
        self.w_rad_active_ifs = \
                RadioButtons(self.rax_activeifs,
                             sorted(self.colors_ifs.keys()),
                             active=idx_active,
                             activecolor=activecolor)

#         self.prop_ifs_active = self.props[idx_active]

        self.w_rad_active_ifs.on_clicked(self.colorfunc)
        return self.w_rad_active_ifs

    def colorfunc(self, label):
        idx = int(label)
#             global prop_ifs_active
#         self.prop_ifs_active = self.props[idx]
#         print("color func: prop_ifs: %s" % self.active_prop[0].label)
        self.active_prop[0] = self.props[idx]
#         print("color func: prop_ifs: %s" % self.active_prop[0].label)        
#             prop_ifs_active = self.axlines[self.ax_active][idx]
        self.w_rad_active_ifs.activecolor = self.prop_ifs.get_color()
#         self._recreate_active_ifs_radiobutton()
        self._recreate_radius_slider()
        self._recreate_show_lines_check_button()
        self._recreate_alpha_slider()
        self._recreate_textsize_slider()

        if self.canvas is None:
            self.canvas.draw()       



    def _recreate_textsize_slider(self):
        
        axcolor = 'lightgoldenrodyellow'        
        if hasattr(self, 'textsize_slax'):
            self.textsize_slax.cla()
        self.textsize_slax = plt.axes([0.05, 0.11, 
                                       self.slider_length__, 
                                       self.slider_hight__], axisbg=axcolor)

        fontsize = self.prop_ifs.annotations[0].get_fontsize()

        fontsize = 10 if fontsize is None else fontsize
        self.w_sl_textsize = Slider(self.textsize_slax, ' ', 5, 20,
                                 valinit=fontsize)
        self.w_sl_textsize.label = self.textsize_slax.text(0.02, 1.5, 
                             label='Font size',
                             s='font size: %.f-%.f' %(5,20), 
                             transform=self.textsize_slax.transAxes,
                             verticalalignment='center',
                             horizontalalignment='left')

        def update_fontsize_annotation(val=None):
            value = self.w_sl_textsize.val if (val is None) else val
            self.prop_ifs.set_fontsize_annotations(value)
            if self.canvas is not None:
                self.canvas.draw()
        
        self.w_sl_textsize.on_changed(update_fontsize_annotation)
        return self.w_sl_textsize


    def _recreate_alpha_slider(self):

        axcolor = 'lightgoldenrodyellow'
        if hasattr(self, 'alpha_slax'):
            self.alpha_slax.cla()
        self.alpha_slax = plt.axes([0.05, 0.08, 
                                       self.slider_length__, 
                                       self.slider_hight__], axisbg=axcolor)
        
        alpha = self.prop_ifs.holder.get_alpha()

        alpha = 0.5 if alpha is None else alpha
        self.w_sl_alpha = Slider(self.alpha_slax, ' ', 0, 1,
                                 valinit=alpha)
        self.w_sl_alpha.label = self.alpha_slax.text(0.02, 1.5, 
                             label='Radius marker',
                             s='alpha: %.f-%.f' %(0,1), 
                             transform=self.alpha_slax.transAxes,
                             verticalalignment='center',
                             horizontalalignment='left')
        
        def update_alpha(val=None):
            value = self.w_sl_alpha.val if (val is None) else val
            self.prop_ifs.holder.set_alpha(value)
            if self.canvas is not None:
                self.canvas.draw()
        
        self.w_sl_alpha.on_changed(update_alpha)
        return self.w_sl_alpha
        

    def _recreate_radius_slider(self):

        axcolor = 'lightgoldenrodyellow'        
        if hasattr(self, 'radius_slax'):
            self.radius_slax.cla()
        self.radius_slax = plt.axes([0.05, 0.05, 
                                    self.slider_length__, 
                                    self.slider_hight__], axisbg=axcolor)
        
        self.w_sl_radius = Slider(self.radius_slax, ' ', 5, 100,
                        valinit=self.prop_ifs.get_markersize())
        self.w_sl_radius.label = self.radius_slax.text(0.02, 1.5, 
                             label='Radius marker',
                             s='radius: %.f-%.f' %(5,100), 
                             transform=self.radius_slax.transAxes,
                             verticalalignment='center',
                             horizontalalignment='left')

        def update_radius(val=None):
            value = self.w_sl_radius.val if (val is None) else val
            self.prop_ifs.holder.set_markersize(value)
            if self.canvas is not None:
                self.canvas.draw()

        
        self.w_sl_radius.on_changed(update_radius)
        return self.w_sl_radius

    def _recreate_show_lines_check_button(self):

        axcolor = 'lightgoldenrodyellow'
        if hasattr(self, 'rax_showlines'):
            self.rax_showlines.cla()
        self.rax_showlines = plt.axes([0.2, 0.05,
                                       self.button_length__,
                                       self.button_height__], axisbg=axcolor)

        visible = self.prop_ifs.holder.get_visible()
        linestyle = self.prop_ifs.holder.get_linestyle()

        labels = ('hide ifs',
                 'markers', 
                 'edges',
                 'labels')
        actives = (self.prop_ifs.hide_ifs,
                   visible,
                   linestyle not in ['None', None],
                   self.prop_ifs.show_ann)

        self.holder_actives = dict(zip(labels, actives))        

        self.w_check_components = CheckButtons(self.rax_showlines, 
                    labels,
                    actives)

        def update_show_components(label):
            self.holder_actives[label] = not self.holder_actives[label]
            
            if label == 'hide ifs':
                if self.holder_actives[label]:
                    self.prop_ifs.holder.set_linestyle(' ')
                    self.prop_ifs.holder.set_visible(False)
                    self.prop_ifs.set_visible_annotations(False)
                else:
                    self.prop_ifs.holder.set_linestyle(' ')
                    self.prop_ifs.holder.set_visible(True)
                    self.prop_ifs.set_visible_annotations(True)

            elif label == 'markers':
                self.prop_ifs.holder.set_visible(self.holder_actives[label])

            elif label == 'edges':
                style = '-' if self.holder_actives[label] else ' '
                self.prop_ifs.holder.set_linestyle(style)

            elif label == 'labels':
                self.prop_ifs.set_visible_annotations(self.holder_actives[label])

            if self.canvas is not None:
                self.canvas.draw()

        self.w_check_components.on_clicked(update_show_components)
        return self.w_check_components

#     def _flip_hide_ifs(self):
#         if self.holder_actives['hide ifs']:
#             
#         if self.prop_ifs.holder.get_linestyle() == '-':
#             self._flip_edges()
#         if self.prop_ifs.holder.get_visible():
#             self._flip_markers()
#         if self.prop_ifs.show_ann:
#             self._flip_labels()            
# 
#     def _flip_edges(self):
# 
#         linestyle = self.prop_ifs.holder.get_linestyle()
# 
#         style = '-' if linestyle in ['None', None] else ' '
#         self.prop_ifs.holder.set_linestyle(style)
#         return self.prop_ifs.holder.get_linestyle()
# 
# 
#     def _flip_markers(self):
# 
#         self.prop_ifs.holder.set_visible(not self.prop_ifs.holder.get_visible())
# 
#         return self.prop_ifs.holder.get_visible()
# 
# 
#     def _flip_labels(self):
# 
#         self.prop_ifs.show_ann = not self.prop_ifs.show_ann
#         self.prop_ifs.set_visible_annotations(self.prop_ifs.show_ann)
#         return self.prop_ifs.show_ann
