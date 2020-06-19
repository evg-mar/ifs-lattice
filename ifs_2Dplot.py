import copy
import numpy as np

import matplotlib.pyplot as plt
# from matplotlib import style

def rotate_axislabels(ax, angles={'x': 45,'y': 45,'z': 45}):
    if 'x' in angles:
        for label in ax.xaxis.get_ticklabels():
            label.set_rotation(angles['x'])
    if 'y' in angles:
        for label in ax.yaxis.get_ticklabels():
            label.set_rotation(angles['y'])


def plot_ifs(ifs, typ='interval_valued'):
    """
    plot type = 'intuitionistic' or 'interval_valued'
    """
    # fig = plt.figure()
    fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
    # ax1 = plt.subplot2grid((1,1), (0,0))
    indices, mus, nus, _ = ifs.elements_split()
    second = nus if (typ=='intuitionistic') else [ifs._range - n for n in nus]
    
    ax0.plot(indices, mus, color='b', label='Membership')
    ax1.plot(indices, second, color='g', label='Non-Membership')
    
    # plt.show()


def plot_together_intValued(ifs):

    # fig, ax0 = plt.subplots(nrows=1)
    fig = plt.figure()
    ax0 = plt.subplot2grid((1,1), (0,0))
    
    indices, mus, nus, pis = ifs.elements_split()
    mus_plus_pis = [m+p for m,p in zip(mus,pis)]
    ax0.plot(indices, mus, 'bo', linewidth=2,
            label='Membership')
    ax0.plot(indices, mus_plus_pis, 'go', linewidth=2,
            label='Non-membership')

    ax0.fill_between(indices, 0, mus, facecolor='b', alpha=0.3)
    ax0.fill_between(indices, mus_plus_pis, ifs._range, facecolor='g', alpha=0.3)   
#              mus_plus_pis, [ifs._range]*ifs.length(), 'g')

    last_value = ifs.get_range()
    for i in indices:
        ax0.plot([i,i], 
             [0,last_value],
             '--', color='k')

    ax0.set_xlabel('Universe')
    ax0.set_ylabel('Degrees')
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.title('2 type plot type')


def plot_together_Intuitionistic(ifs):

    # fig, ax0 = plt.subplots(nrows=1)
    fig = plt.figure()
    ax0 = plt.subplot2grid((1,1), (0,0))
    
    indices, mus, nus, pis = ifs.elements_split()
    mus_plus_pis = [m+p for m,p in zip(mus,pis)]
    ax0.plot(indices, mus, 'bo', linewidth=2,
            label='Membership')
    ax0.plot(indices, nus, 'go', linewidth=2,
            label='Non-membership')

    ax0.fill_between(indices, 0, mus, facecolor='b', alpha=0.3)
    ax0.fill_between(indices, 0, nus, facecolor='g', alpha=0.3)   
#              mus_plus_pis, [ifs._range]*ifs.length(), 'g')

    ax0.set_xlabel('Universe')
    ax0.set_ylabel('Degrees')    
    plt.legend(loc='upper right')
    plt.title('Intuitionistic plot type')


def plot_stack(ifs):
    """
    plot stack type = 'intuitionistic' type only
    """
    fig = plt.figure()

    indices, mus, nus, pis = ifs.elements_split()
    plt.stackplot(indices, mus, pis, nus, colors=['b','c','g'])

    plt.plot([],[],color='b', label='Membership', linewidth=5)
    plt.plot([],[],color='c', label='Indeterminacy', linewidth=5)
    plt.plot([],[],color='g', label='Non-membership', linewidth=5)

    plt.xlabel('Universe')
    plt.ylabel('Degrees')
    
    plt.legend(loc='upper right')
    # plt.show()


def plot_bar_type_1(ifs, plot_pi=False):
    """
    plot stack bars type = 'intuitionistic' type only
    """    
#     fig, ax0 = plt.subplots(1, figsize=(10,5))
    fig, ax0 = plt.subplots(nrows=1)
    indices, mus, nus, pis = ifs.elements_split()
    bar_width = 0.4
    
    
    ax0.bar(indices, mus, color='b', width=bar_width,
            label='Membership')
    ax0.bar([i+bar_width for i in indices], nus,color='g', width=bar_width,
            label='Non-membership')
    if plot_pi:
        ax0.bar([i+2*bar_width for i in indices], pis, color='c',
            width=bar_width,
            label='Indeterminacy')
    
    ax0.set_xlabel('Universe')
    ax0.set_ylabel('Degrees')
    
    plt.legend(loc='upper right')
    plt.title('Type 1 stack bars')
    
    # plt.show()
    
    
def plot_bar_type_2(ifs):
    """
    plot stack bars type = 'interval valued' type only
    """    
#     fig, ax0 = plt.subplots(1, figsize=(10,5))
    fig, ax0 = plt.subplots(nrows=1)
    indices, mus, nus, pis = ifs.elements_split()
    
    ax0.bar(indices, mus, color='b',
            label='Membership')
    ax0.bar(indices, pis, bottom=mus, color='c',
            label='Indeterminacy')    
    ax0.bar(indices, nus, bottom=[m+p for m,p in zip(mus,pis)], color='g',
            label='Non-membership')
    
    ax0.set_xlabel('Universe')
    ax0.set_ylabel('Degrees')
    
    plt.legend(loc='upper right')
    plt.title('Type 2 Stack Bars')
    
    # plt.show()
    
# -----------------------------------------------------------------#
#        Triangular Representation
# -----------------------------------------------------------------#

class PlotTriangular2D(object):
    
    def __init__(self, 
                mus, nus,
                rang=1,                 
                axtype={'triang':True, 'mu_histo':False, 'nu_histo':False},
                bins={'mu':10, 'nu':10},
                colors={'mu':'b', 'nu':'g', 'elem':'r'}):
        self.mus = mus
        self.nus = nus
        self.rang = rang
        self.axtype = copy.deepcopy(axtype)
        self.bins = copy.deepcopy(bins)
        self.colors = copy.deepcopy(colors)
        
        
    def set_musnus(self, mus, nus):
        assert(len(mus) == len(nus))
        self.mus = mus
        self.nus = nus

    def set_rang(self, rang):
        assert(rang > 0)

    def set_axestype(self, axtype):
        self.axtype = copy.deepcopy(axtype)

def plot_triangle(rang, ax, plottyp='-', color='k', linewidth=1.5):
    '''
    Plot the main triangle as font of the triangular
    representation of IFSs
    '''
    min_ = 0.0
    max_ = rang
    d = 30 # make visible all the edges of the triangle
    x_triang = [min_, min_, max_, min_]
    y_triang = [min_, max_, min_, min_]
    ax.set_xlim([min_-(max_-min_)/d, max_ + (max_-min_)/d])
    ax.set_ylim([min_-(max_-min_)/d, max_ + (max_-min_)/d])
#     ax.set_xticks(np.arange(min_, max_+1, 1))
#     ax.set_yticks(np.arange(min_, max_+1, 1))
    
    ax.plot(x_triang, y_triang,
            plottyp, linewidth=linewidth, color=color, 
            label='_nolegend_',
            )


def plot_triangular_(ax,
                    mus,nus, rang=1,
                    bins={'mu':10, 'nu':10},
                    colors={'mu':'b', 'nu':'g', 'elem':'r'},
                    rotation=None,
                    marker='o',
                    markersize=2,
                    alpha=0.4,
                    color='b'):
    assert(type(bins) in [int, dict])
    if type(bins) == int:
        bins = {'mu':bins, 'nu':bins}

    axScatter = ax
#     axNuHist = plt.subplot2grid((4,4), (1,3), rowspan=3, colspan=1,
#                                 sharey=axScatter)
#     axMuHist = plt.subplot2grid((4,4), (0,0), rowspan=1, colspan=3,
#                                 sharex=axScatter)

    # Set ticks to the scatter axes
    xlinspace = np.linspace(0.0, rang, bins['mu']+1)
    axScatter.set_xticks(xlinspace)
    ylinspace = np.linspace(0.0, rang, bins['nu']+1)
    axScatter.set_yticks(ylinspace)
    #//
    # Set invisible the ticks of the histogram axes
#     plt.setp(axMuHist.get_xticklabels(), visible=False)
#     plt.setp(axNuHist.get_yticklabels(), visible=False)
    #//

    plot_triangle(rang, axScatter, 'k')
    
    line2d_, = axScatter.plot(mus, nus, 
                              marker=marker, markerfacecolor=colors['elem'],
                              linestyle=' ', color=color, alpha=alpha,markersize=markersize)

    if rotation is not None:
        rotate_axislabels(axScatter, rotation)

#     histMuValues, _, _ = axMuHist.hist(mus, bins=xlinspace, color=colors['mu'])
#     histNuValues, _, _ = axNuHist.hist(nus, bins=ylinspace, color=colors['nu'],
#                                        orientation='horizontal')

    # Set limits to the histogram axes
#     histLimit = max(max(histMuValues), max(histNuValues))
#     axMuHist.set_ylim(0.0, histLimit)
#     axNuHist.set_xlim(0.0, histLimit)
    # //Set limits to the histogram axes

    axScatter.grid(True, linestyle='--', color='r')
    for lin in axScatter.get_xgridlines():
        lin.set_color(colors['mu'])
    for lin in axScatter.get_ygridlines():
        lin.set_color(colors['nu'])

    # Plot legend of the figure /for all subplots/
#     axLegend = plt.subplot2grid((4,4), (0,3), rowspan=1, colspan=1)
    # Hide font and ticks of the legend axes
#     axLegend.patch.set_visible(False)
#     axLegend.set_axis_off()
#     plt.setp(axLegend.get_xticklabels(), visible=False)
#     plt.setp(axLegend.get_yticklabels(), visible=False)
#     
#     histMuBars = plt.Rectangle((0, 0), 1, 1, fc=colors['mu'])
#     histNuBars = plt.Rectangle((0, 0), 1, 1, fc=colors['nu'])
# 
#     axLegend.legend((legendSc, histMuBars, histNuBars ),
#                     ("Map of the Universe",
#                      "Membership histogram",
#                      "Non-membership histogram"),
# #                     fontsize='large',
#                     loc='upper right')

    
    axScatter.legend(loc='upper right')
#     axScatter.legend((line2d_,), ("Map of the Universe",),
#                      loc='upper right', fontsize='large')
#     axScatter.set_xlabel('Membership', fontsize='x-large')
#     axScatter.set_ylabel('Non-membership', fontsize='x-large')
    
    return axScatter, line2d_



def plot_triangular_scatter(ax,
                    mus,nus, rang=1,
                    bins={'mu':10, 'nu':10},
                    colors={'mu':'b', 'nu':'g', 'elem':'r'},
                    rotation=None):
    assert(type(bins) in [int, dict])
    if type(bins) == int:
        bins = {'mu':bins, 'nu':bins}

    axScatter = ax
#     axNuHist = plt.subplot2grid((4,4), (1,3), rowspan=3, colspan=1,
#                                 sharey=axScatter)
#     axMuHist = plt.subplot2grid((4,4), (0,0), rowspan=1, colspan=3,
#                                 sharex=axScatter)

    # Set ticks to the scatter axes
    xlinspace = np.linspace(0.0, rang, bins['mu']+1)
    axScatter.set_xticks(xlinspace)
    ylinspace = np.linspace(0.0, rang, bins['nu']+1)
    axScatter.set_yticks(ylinspace)
    #//
    # Set invisible the ticks of the histogram axes
#     plt.setp(axMuHist.get_xticklabels(), visible=False)
#     plt.setp(axNuHist.get_yticklabels(), visible=False)
    #//

    plot_triangle(rang, axScatter, 'k')
    
    line2d_ = axScatter.scatter(mus, nus, 
                              marker='o', facecolor=colors['elem'],
                              linestyle='-', edgecolor='b')

    if rotation is not None:
        rotate_axislabels(axScatter, rotation)

#     histMuValues, _, _ = axMuHist.hist(mus, bins=xlinspace, color=colors['mu'])
#     histNuValues, _, _ = axNuHist.hist(nus, bins=ylinspace, color=colors['nu'],
#                                        orientation='horizontal')

    # Set limits to the histogram axes
#     histLimit = max(max(histMuValues), max(histNuValues))
#     axMuHist.set_ylim(0.0, histLimit)
#     axNuHist.set_xlim(0.0, histLimit)
    # //Set limits to the histogram axes

    axScatter.grid(True, linestyle='--', color='r')
    for lin in axScatter.get_xgridlines():
        lin.set_color(colors['mu'])
    for lin in axScatter.get_ygridlines():
        lin.set_color(colors['nu'])

    # Plot legend of the figure /for all subplots/
#     axLegend = plt.subplot2grid((4,4), (0,3), rowspan=1, colspan=1)
    # Hide font and ticks of the legend axes
#     axLegend.patch.set_visible(False)
#     axLegend.set_axis_off()
#     plt.setp(axLegend.get_xticklabels(), visible=False)
#     plt.setp(axLegend.get_yticklabels(), visible=False)
#     
#     histMuBars = plt.Rectangle((0, 0), 1, 1, fc=colors['mu'])
#     histNuBars = plt.Rectangle((0, 0), 1, 1, fc=colors['nu'])
# 
#     axLegend.legend((legendSc, histMuBars, histNuBars ),
#                     ("Map of the Universe",
#                      "Membership histogram",
#                      "Non-membership histogram"),
# #                     fontsize='large',
#                     loc='upper right')

    
    axScatter.legend(loc='upper right')
#     axScatter.legend((line2d_,), ("Map of the Universe",),
#                      loc='upper right', fontsize='large')
#     axScatter.set_xlabel('Membership', fontsize='x-large')
#     axScatter.set_ylabel('Non-membership', fontsize='x-large')
    
    return line2d_


def plot_triangular(mus,nus, rang=1,
                    bins={'mu':10, 'nu':10},
                    colors={'mu':'b', 'nu':'g', 'elem':'r'}):
    assert(type(bins) in [int, dict])
    if type(bins) == int:
        bins = {'mu':bins, 'nu':bins}

    fig = plt.figure()
    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    
    axScatter = plt.subplot2grid((4,4), (1,0), rowspan=3, colspan=3)
    
    axNuHist = plt.subplot2grid((4,4), (1,3), rowspan=3, colspan=1,
                                sharey=axScatter)
    axMuHist = plt.subplot2grid((4,4), (0,0), rowspan=1, colspan=3,
                                sharex=axScatter)

    # Set ticks to the scatter axes
    xlinspace = np.linspace(0.0, rang, bins['mu']+1)
    axScatter.set_xticks(xlinspace)
    ylinspace = np.linspace(0.0, rang, bins['nu']+1)
    axScatter.set_yticks(ylinspace)
    #//
    # Set invisible the ticks of the histogram axes
    plt.setp(axMuHist.get_xticklabels(), visible=False)
    plt.setp(axNuHist.get_yticklabels(), visible=False)
    #//

    plot_triangle(rang, axScatter, 'k')
    
    legendSc = axScatter.plot(mus, nus, 
                              marker='o', markerfacecolor=colors['elem'],
                              linestyle=' ', color='b')
    axScatter.legend(loc='upper right')
    rotate_axislabels(axScatter, {'x':45,'y':45})

    histMuValues, _, _ = axMuHist.hist(mus, bins=xlinspace, color=colors['mu'])
    histNuValues, _, _ = axNuHist.hist(nus, bins=ylinspace, color=colors['nu'],
                                       orientation='horizontal')

    # Set limits to the histogram axes
    histLimit = max(max(histMuValues), max(histNuValues))
    axMuHist.set_ylim(0.0, histLimit)
    axNuHist.set_xlim(0.0, histLimit)
    # //Set limits to the histogram axes

    axScatter.grid(True, linestyle='--', color='r')
    for lin in axScatter.get_xgridlines():
        lin.set_color(colors['mu'])
    for lin in axScatter.get_ygridlines():
        lin.set_color(colors['nu'])

    # Plot legend of the figure /for all subplots/
    axLegend = plt.subplot2grid((4,4), (0,3), rowspan=1, colspan=1)
    # Hide font and ticks of the legend axes
    axLegend.patch.set_visible(False)
    axLegend.set_axis_off()
    plt.setp(axLegend.get_xticklabels(), visible=False)
    plt.setp(axLegend.get_yticklabels(), visible=False)
    
    histMuBars = plt.Rectangle((0, 0), 1, 1, fc=colors['mu'])
    histNuBars = plt.Rectangle((0, 0), 1, 1, fc=colors['nu'])

    axLegend.legend((legendSc, histMuBars, histNuBars ),
                    ("Map of the Universe",
                     "Membership histogram",
                     "Non-membership histogram"),
#                     fontsize='large',
                    loc='upper right')

    axScatter.set_xlabel('Membership', fontsize='x-large')
    axScatter.set_ylabel('Non-membership', fontsize='x-large')



    axScatter.set_aspect('equal', 'datalim')
    # axMuHist.set_aspect('equal', 'datalim')
    # axNuHist.set_aspect('equal', 'datalim')
     
def test_legend():
    # Figure
    plt.figure()
    plt.gcf().suptitle(r'Difference between TI and $\lambda$D', size=16)
    # Subplot 1
    ax1 = plt.subplot2grid((1,3),(0,0),colspan=2)
    
    # Plot scattered data in first subplot
    ax1.scatter(np.linspace(1,5,5), np.linspace(-1,5,5), color='gold', marker='o', label=r'$\lambda$D')
    ax1.scatter(np.linspace(4,5,5), np.linspace(3,5,5),color='blue', marker='^', label=r'TI')

    ax1.legend(loc='upper left')    
    # Subplot 2
    ax2 = plt.subplot2grid((1,3),(0,2))
    
    ax2.barh(np.linspace(1,5,15), np.linspace(1,12,15), height=4, color='gold', label=r'$\lambda$D')
    ax2.barh(np.linspace(-1,15,10), np.linspace(1,25,10), height=4, color='blue', label=r'TI')
    

    # Legend

    
def plot_triangular_with_arrows(ifs):
    fig = plt.figure()
    ax0 = plt.subplot2grid((1,1), (0,0))
    
    plot_triangle(ifs.get_range(), ax0)
    
    indices, mus, nus, pis = ifs.elements_split()
    mus = np.array(mus, dtype='float32')
    nus = np.array(nus, dtype='float32')
 
    ax0.scatter(mus, nus, color='r') 
    ax0.plot(mus, nus, color='c')    
    
    musD = mus[1:] - mus[:-1]
    nusD = nus[1:] - nus[:-1]  
    Diff = np.sqrt(musD**2 + nusD**2)
    Diff = np.array(list(map(lambda a: np.nan if a==0 else a, Diff)),
                    dtype='float32')
    Cos = musD/Diff
    Sin = nusD/Diff  
    
    muS= mus[:-1] + (mus[1:] - mus[:-1])/2.0
    nuS= nus[:-1] + (nus[1:] - nus[:-1])/2.0
    # ax0.scatter(muS, nuS, color='g')    
    head_width = 0.2*ifs.get_range()/30
    head_length = 0.5*ifs.get_range()/30
    for mu,c,nu,s  in zip(muS,Cos, nuS,Sin):
        delta = 0.001 # if direction >= 0 else -0.0001
        if(s is not np.nan):
#             print(mu, nu, mu+c*delta, nu+s*delta)
            ax0.arrow(mu, nu, c*delta, s*delta,
                 head_width=head_width, head_length=head_length,
                 color='k')

   
    plt.title("Plot triangular with arrows")
