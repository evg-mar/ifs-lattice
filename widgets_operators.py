import matplotlib.pyplot as plt

from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

from ifs_triangular_representation import IfsTriangInteractive, IfsTriang

class WidgetsSimple(object):

    x_start__ = 0.05
    y_start__ = 0.05

    text_length__ = 0.025
    text_hight__ = 0.025

    slider_length__ = 0.06
    slider_hight__  = 0.015

    button_length__ = 0.05
    button_height__ = 0.1

    def __init__(self, canvas=None, active_prop=None):
        self.canvas = canvas
        self.active_prop = active_prop
#         self.colors_ifs = { }
        self.props = []

    @property
    def prop_ifs(self):
        return self.active_prop

    def recreate_widgets_(self, active_prop):
#         self.prop_ifs = active_prop[0]
        self.active_prop = active_prop
#         self._recreate_active_ifs_radiobutton(idx_active, props)
        self._recreate_radius_slider()
        self._recreate_alpha_slider()
        self._recreate_textsize_slider()
        self._recreate_show_lines_check_button()
#        self._recreate_save_ifs_button()

#    def _recreate_save_ifs_button(self):
#


    def _recreate_textsize_slider(self):

        axcolor = 'lightgoldenrodyellow'
        if hasattr(self, 'textsize_slax'):
            self.textsize_slax.cla()
        self.textsize_slax = plt.axes([self.x_start__,
                               self.y_start__ + 2*(self.slider_hight__ + self.text_hight__),
                                       self.slider_length__,
                                       self.slider_hight__], facecolor=axcolor)

        fontsize = self.prop_ifs.get_annotation_size()

        fontsize = 10 if fontsize is None else fontsize
        self.w_sl_textsize = Slider(self.textsize_slax, ' ', 5, 20,
                                 valinit=fontsize)
        self.w_sl_textsize.label = self.textsize_slax.text(0.02, 1.5,
                             label='Font size',
                             s='font size: [%.f-%.f]' %(5,20),
                             transform=self.textsize_slax.transAxes,
                             verticalalignment='center',
                             horizontalalignment='left')

        def update_fontsize_annotation(val=None):
            value = self.w_sl_textsize.val if (val is None) else val
            self.prop_ifs.set_annotation_size(value)
            if self.canvas is not None:
                self.canvas.draw()

        self.w_sl_textsize.on_changed(update_fontsize_annotation)
        return self.w_sl_textsize


    def _recreate_alpha_slider(self):

        axcolor = 'lightgoldenrodyellow'
        if hasattr(self, 'alpha_slax'):
            self.alpha_slax.cla()
        self.alpha_slax = plt.axes([self.x_start__,
                    self.y_start__ + 1*( self.slider_hight__ + self.text_hight__),
                                       self.slider_length__,
                                       self.slider_hight__], facecolor=axcolor)

        alpha = self.prop_ifs.get_alpha_marker()

        alpha = 0.5 if alpha is None else alpha
        self.w_sl_alpha = Slider(self.alpha_slax, ' ', 0, 1,
                                 valinit=alpha)
        self.w_sl_alpha.label = self.alpha_slax.text(0.02, 1.5,
                             label='Alpha marker',
                             s='contrast: [%.f-%.f]' %(0,1),
                             transform=self.alpha_slax.transAxes,
                             verticalalignment='center',
                             horizontalalignment='left')

        def update_alpha(val=None):
            value = self.w_sl_alpha.val if (val is None) else val
            self.prop_ifs.set_alpha_marker(value)
            if self.canvas is not None:
                self.canvas.draw()

        self.w_sl_alpha.on_changed(update_alpha)
        return self.w_sl_alpha


    def _recreate_radius_slider(self):

        axcolor = 'lightgoldenrodyellow'
        if hasattr(self, 'radius_slax'):
            self.radius_slax.cla()
        self.radius_slax = plt.axes([self.x_start__,
                 self.y_start__ + 0*( self.slider_hight__ + self.text_hight__),
                                    self.slider_length__,
                                    self.slider_hight__], facecolor=axcolor)

        a, b = 0.0, 0.05
        transform = lambda x: a + x*(b - a)
        transform_reverse = lambda y: (y - a)/(b - a)

        self.w_sl_radius = Slider(self.radius_slax, ' ', 0, 1,
                        valinit=transform_reverse(self.prop_ifs.get_radius()))
        self.w_sl_radius.label = self.radius_slax.text(0.02, 1.5,
                             label='Radius marker',
                             s='radius size: [%.f-%.f]' %(0, 1),
                             transform=self.radius_slax.transAxes,
                             verticalalignment='center',
                             horizontalalignment='left')

        def update_radius(val=None):
            #print("update prop id: ", id(self.prop_ifs))
            #print("radius: ", self.prop_ifs.radius)
            value = self.w_sl_radius.val if (val is None) else val
            self.prop_ifs.set_radius(transform(value))

            if self.canvas is not None:
                #print("updateD prop id: ", id(self.prop_ifs))
                #print("radiusD: ", self.prop_ifs.radius)
                self.canvas.draw()


        self.w_sl_radius.on_changed(update_radius)
        return self.w_sl_radius

    def _recreate_show_lines_check_button(self):

        axcolor = 'lightgoldenrodyellow'
        if hasattr(self, 'rax_showlines'):
            self.rax_showlines.cla()
        self.rax_showlines = plt.axes([self.x_start__ + self.slider_length__ + self.text_length__,
                                       self.y_start__,
                                       self.button_length__,
                                       self.button_height__], facecolor=axcolor)

        visible = self.prop_ifs.get_visible()
        show_ann = self.prop_ifs.get_annotation_visible()


        labels = ('showIFS',
                 #'marks',
                 #'edges',
                 'labels')
        actives = (visible,
                   # linestyle not in ['None', None],
                   show_ann)

        self.holder_actives = dict(zip(labels, actives))

        self.w_check_components = CheckButtons(self.rax_showlines,
                    labels,
                    actives)


        self.w_check_components.on_clicked(self.update_show_components)
        return self.w_check_components


    def update_show_components(self, label):
        self.holder_actives[label] = not self.holder_actives[label]

        if label == 'showIFS':
            self.prop_ifs.set_visible(self.holder_actives[label])

#        elif label == 'edges':
#            style = '-' if self.holder_actives[label] else ' '
#            self.prop_ifs.holder.set_linestyle(style)

        elif label == 'labels':
            self.prop_ifs.set_annotation_visible(self.holder_actives[label])


        if self.canvas is not None:
            print("draw canvas" + label + str(self.holder_actives[label]))
            self.canvas.draw()
        else:
            print("canvas is none")


#########################################################################

#class WidgetsSimpleChoice(WidgetsSimple):



#########################################################################
class WidgetsSimpleOperator(WidgetsSimple):

    def __init__(self, canvas=None, active_prop=None):
        super().__init__(canvas=canvas,
                         active_prop=active_prop)


    def recreate_widgets_(self, active_prop):
        super().recreate_widgets_(active_prop)
        self._recreate_save_ifs_button()
        self._recreate_show_operators_check_button()

    def _recreate_save_ifs_button(self):

#        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
#        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
#        bnext = Button(axnext, 'Next')

        axcolor = 'lightgoldenrodyellow'
        if hasattr(self, 'save_btax'):
            self.save_btax.cla()
        self.save_btax = plt.axes([self.x_start__ + self.slider_length__ \
                            + self.text_length__ + self.button_length__,
                                       self.y_start__,
                                       self.button_length__,
                                       self.button_height__], facecolor=axcolor)
        self.w_bt_save = Button(self.save_btax, 'Save \nIFS')


        self.w_bt_save.on_clicked(self.prop_ifs.save_to_json_default)


    def _recreate_show_operators_check_button(self):

        axcolor = 'lightgoldenrodyellow'
        if hasattr(self, 'rax_showlines_operator'):
            self.rax_showlines_operator.cla()
        self.rax_showlines_operator = plt.axes([self.x_start__ + self.slider_length__ \
                            + self.text_length__ + 2* self.button_length__,
                                       self.y_start__,
                                       self.button_length__,
                                       self.button_height__], facecolor=axcolor)

#        visible = self.prop_ifs.get_visible()
#        linestyle = self.prop_ifs.holder.get_linestyle()

        labels = tuple(self.active_prop.companions.keys())
        actives = tuple([True ] * len(labels))
        self.holder_actives_oper = {label: True for label in labels}

        # labels = ('F',
        #          'G',
        #          'H',
        #          'J')
        # actives = (True,
        #            True,
        #            True,
        #            True)

        self.holder_actives_oper = dict(zip(labels, actives))

        self.w_check_components_operator = CheckButtons(self.rax_showlines_operator,
                    labels,
                    actives)


        self.w_check_components_operator.on_clicked(self.update_show_components_operator)
        return self.w_check_components_operator

    def update_show_components_operator(self, label):
        self.holder_actives_oper[label] = not self.holder_actives_oper[label]
        print(self.active_prop.companions)
        print(self.active_prop.companions[label][1])
        self.active_prop.companions[label][1] \
                        .set_visible(self.holder_actives_oper[label])
        self.active_prop.companions[label][1] \
                        .set_annotation_visible(self.holder_actives_oper[label])
#        if label == 'F':
#            #self.prop_ifs.holder.set_visible(holder_actives[label])
#            self.active_prop.companions[label] \
#                .set_visible(self.holder_actives_oper[label])
#            pass
#
#        elif label == 'G':
#            #style = '-' if holder_actives[label] else ' '
#            #self.prop_ifs.holder.set_linestyle(style)
#            pass
#
#        elif label == 'H':
#            #self.prop_ifs.set_visible_annotations(self.holder_actives_operator[label])
#            pass
#        elif label == 'J':
#            # self.prop_ifs.set_visible_annotations(self.holder_actives_operator[label])
#            pass
        if self.canvas is not None:
            self.canvas.draw()


##########################################################################

# Widgets with choice of active ifs 
class WidgetsBasic(WidgetsSimple):

    def __init__(self, canvas=None, active_prop=None):
        super(WidgetsBasic, self).__init__(canvas, active_prop)

        self.colors_ifs = { }

    @property
    def prop_ifs(self):
        return self.active_prop

    def update_show_components(self, label):
        super(WidgetsBasic, self).update_show_components(label)
        if label == 'hide ifs':
            if self.holder_actives[label]:
                self.prop_ifs.holder.set_linestyle(' ')
                self.prop_ifs.holder.set_visible(False)
                self.prop_ifs.set_visible_annotations(False)
                self.prop_ifs.topo_const.set_visible(False)
            else:
                self.prop_ifs.holder.set_linestyle(' ')
                self.prop_ifs.holder.set_visible(True)
                self.prop_ifs.set_visible_annotations(True)
                self.prop_ifs.topo_const.set_visible(True)

    # here is updated the active prop_ifs
    def recreate_widgets(self,
                         idx_active, props, active_prop):
        super(WidgetsBasic, self).recreate_widgets_(active_prop)
        self._recreate_active_ifs_radiobutton(idx_active, props)

    def _recreate_active_ifs_radiobutton(self, idx_active, props):
        self.props = props
        axcolor = 'lightgoldenrodyellow'
        if hasattr(self, 'rax_activeifs'):
            self.rax_activeifs.cla()
        self.rax_activeifs = plt.axes([0.2+self.button_length__+0.01, 0.05,
                                       self.button_length__,
                                       self.button_height__], facecolor=axcolor)
        activecolor = self.active_prop.get_color()
        self.w_rad_active_ifs = \
                RadioButtons(self.rax_activeifs,
                             sorted(self.colors_ifs.keys()),
                             active=idx_active,
                             activecolor=activecolor)

        self.w_rad_active_ifs.on_clicked(self.colorfunc)
        return self.w_rad_active_ifs

    def colorfunc(self, label):
        idx = int(label)
        self.active_prop = self.props[idx]
        self.w_rad_active_ifs.activecolor = self.prop_ifs.get_color()
        self._recreate_radius_slider()
        self._recreate_show_lines_check_button()
        self._recreate_alpha_slider()
        self._recreate_textsize_slider()

        if self.canvas is None:
            self.canvas.draw()
