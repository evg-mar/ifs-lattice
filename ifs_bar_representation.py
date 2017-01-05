from editable_rectangle import EditableRectangle, RectangleBasic
from topo_const_bar import TopoConstBarInteractive
from matplotlib.patches import Rectangle
import numpy as np

class IfsBar(object):
    
    def __init__(self, label,
                       bar_type, # EditableRectangle or RectangleBasic
                       musnus,
                       axes=None,
                       alpha=0.5, 
                       hide_ifs=False,
                       showlabels=False):
        assert(len(musnus[0])==len(musnus[0]))
        self.label = label
        self.axes = axes

        self.mus = np.asarray(musnus[0])
        self.nus = np.asarray(musnus[1])
        self.indices = np.arange(len(self.mus)) 
        self.pis = 1.0 - self.nus - self.mus

        self.bar = axes.bar(self.indices, [1.0]*len(self.indices))
        self.axes.set_aspect(aspect='auto', adjustable='datalim')
        self.axes.set_ylim([0,1])

        self.editable_rects = [Rectangle((0,0), 1, 1)] * len(self.indices)

        for idx, (rect, mu, nu) in enumerate(zip(self.bar, self.mus, self.nus)):
            rect.set_facecolor("white")
            er = bar_type(rect, mu, nu)
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


class IfsBarTopoConst(IfsBar):
    def __init__(self, label,
                       bar_type, # EditableRectangle or RectangleBasic
                       musnus,
                       topo_const_type, # TopoConstBarInteractive
                       alpha_beta,
                       axes=None,
                       alpha=0.5, 
                       hide_ifs=False,
                       showlabels=False):
        super(IfsBarTopoConst, self).__init__(label, bar_type, musnus,
                                              axes, alpha,
                                              hide_ifs, showlabels)
        start_xlim, end_xlim = self.axes.get_xlim()
        width = 0.1
        height = 1.0
        rect = Rectangle((end_xlim, 0.0), width, height,
                         fc='white')
        self.axes.add_patch(rect)
        self.topo_const_bar = topo_const_type(rect, 
                                          alpha_beta[0],
                                          alpha_beta[1])


    def connect(self):
        super(IfsBarTopoConst, self).connect()
        self.topo_const_bar.connect()
        
    def disconnect(self):
        super(IfsBarTopoConst, self).disconnect()
        self.topo_const_bar.disconnect()


if __name__ == '__main__':
    
    import matplotlib.pyplot as plt

    fig = plt.figure()

    axes1 = plt.subplot2grid((1,2), (0,0), rowspan=1, colspan=1)
    # rects = ax.bar(range(10), [1]*10)
    
#     prop1 = IfsBar("proba01", EditableRectangle,  
#                    ([0.1, 0.4, 0.6],[0.6, 0.4, 0.4]), axes=axes1)
#     prop1.connect()

    prop1 = IfsBarTopoConst("proba01", EditableRectangle,  
                   ([0.1, 0.4, 0.6],[0.6, 0.4, 0.4]),
                   topo_const_type=TopoConstBarInteractive,
                   alpha_beta = (0.3, 0.5),
                    axes=axes1)
    prop1.connect()

    
    axes2 = plt.subplot2grid((1,2), (0,1), 
                             sharey=axes1, sharex=axes1,
                             rowspan=1, colspan=1)
    axes2.yaxis.set_label_position("left")
    prop2 = IfsBar('basic_rect', RectangleBasic, 
                   ([0.1, 0.4, 0.6], [0.6, 0.4, 0.4]),
                   axes=axes2)

    plt.show()
