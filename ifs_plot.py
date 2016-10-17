import numpy as np

import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')


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
    plt.title('Interval Valued plot type')

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


def plot_bar_Intuitionistic(ifs, plot_pi=False):
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
    plt.title('Inttuitionistic type stack bars')
    
    # plt.show()
    
    
def plot_bar_intValued(ifs):
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
    plt.title('Interval valued type stack bars')
    
    # plt.show()
    
# -----------------------------------------------------------------#
#        Triangular Representation
# -----------------------------------------------------------------#

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
    ax.set_xticks(np.arange(min_, max_+1, 1))
    ax.set_yticks(np.arange(min_, max_+1, 1))
    
    ax.plot(x_triang, y_triang, plottyp, linewidth=linewidth, color=color)
    ax.set_xlabel('Membership')
    ax.set_ylabel('Non-membership')


def plot_triangular(ifs, ax, color='r'):
#     fig = plt.figure()
#     ax0 = plt.subplot2grid((1,1), (0,0))
    plot_triangle(ifs.get_range(), ax, 'k')
    indices, mus, nus, pis = ifs.elements_split()
    ax.scatter(mus, nus, color=color)    

    
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

###-----------------------------------------------------------
#     Plot 3D
###-----------------------------------------------------------

from mpl_toolkits.mplot3d import Axes3D


def plot_grid_triangular(ax, rang, muEdges=None, nuEdges=None, 
                        colors={'mu':'b', 'nu':'g'}):
    assert(not(muEdges is not None) or ('mu' in colors))
    assert((muEdges is not None) or not('mu' in colors))
    assert(not(nuEdges is not None) or ('nu' in colors))
    assert((nuEdges is not None) or not('nu' in colors))    
    
    if muEdges is not None:
        #plot the mu grid
        for pos in muEdges:
            ax.plot([pos, pos], [0, rang-pos], '--', color=colors['mu'])
    if nuEdges is not None:
        #plot the nu grid
        for pos in nuEdges:
            ax.plot([0, rang-pos], [pos,pos], '--', color=colors['nu'])
   

def plot_membership_3Dhistogram(ifs, 
                                ax, 
                                bins=None, 
                                typs=['mu','nu'],
                                colors={'mu':'b', 'nu':'g'},
                                alpha=0.3):
    
    bins = ifs.get_range()  if (bins is None) else bins 
        
    indices, mus, nus, pis = ifs.elements_split()
    rang = ifs.get_range()

    plot_triangle(rang, ax, plottyp='--', color='k')
    # Plot scatter
    ax.scatter(mus, nus, np.zeros(len(mus),dtype='float32'),
               color='r')
    #//Plot scatter

    hist2d, muEdges, nuEdges = np.histogram2d(mus,nus, bins=bins,
                                          range=[[0,rang],[0,rang]])
    
    plot_grid_triangular(ax, rang, muEdges[1:], nuEdges[1:], colors)

    # Plot the nu histogram on the Nu axis
    d = rang/bins  # the length of a bin (area = length(bin)**2)
    
    # In the 2d histograms (on the Nu and Mu axes), if b = number of bins
    # The area of the k-th line is A_k = (b - k + 1/2) * d^2, where k = 1:b
    # (b - k + 1/2) * d^2 should be proportional to the length of the
    # square k-test line D_k
    # D_k/D_1 = sqrt(A_k/A_1) = C and we want D_1 = d/2
    # That is, D_k = D_1 * sqrt(A_k/A_1)
    D1 = d/2
    C = np.sqrt([(bins - k + 0.5)/(bins -1 + 0.5) for k in range(1,bins+1)])
    dAx = D1*C
    #We suppose that the mu and nu bins have equal length!!!
    #In the future this they may be different -> edgesMin should depend on that
    edgesMid = muEdges[:-1] + (muEdges[1:] - muEdges[:-1] - dAx)*0.5

    zLimit = 0.0 # To be set in the plot_membership function
    
    def plot_membership(typ):
        assert(typ in ['mu','nu'])
        
        # static variable to update the limit of the z-axes
        if not hasattr(plot_membership, "zLimit"):
            plot_membership.zLimit = 0.0
        
        dMu = dAx if typ=='mu' else 0.0
        dNu = dAx if typ=='nu' else 0.0

        muEdgesMid = edgesMid if typ=='mu' else -d*np.ones_like(edgesMid)
        nuEdgesMid = edgesMid if typ=='nu' else -d*np.ones_like(edgesMid)


        dz  = [sum(hist2d[:,i]) for i in range(len(hist2d))] if typ=='nu' \
              else [sum(hist2d[i,:]) for i in range(len(hist2d))]

        plot_membership.zLimit = max(plot_membership.zLimit, max(dz))
        
        ax.bar3d(muEdgesMid, nuEdgesMid, np.zeros_like(edgesMid),
                 dMu, dNu, dz,
                 color=colors[typ],
                 alpha=alpha)

    plot_membership('mu')
    plot_membership('nu')
    zLimit = plot_membership.zLimit

    ax.set_xlabel('Membership')
    ax.set_xlim3d(-0.5, rang+0.5)
    ax.set_ylabel('Non-membership')
    ax.set_ylim3d(-0.5, rang+0.5)
    ax.set_zlabel('Number of occurences')
    ax.set_zlim3d(0, zLimit + 0.5)


def plot_3D_histogramm(ifs,
                       bins=None,
                       colors={'mu':'b','nu':'g'}):

    '''
    Plot a 3D histogram in the triangular representation
    of an IFS.
    '''
    
    bins = ifs.get_range()  if (bins is None) else bins 
   
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    
    indices, mus, nus, pis = ifs.elements_split()
    # print(ifs.get_range())
    rang = ifs.get_range()

    plot_triangle(rang, ax, plottyp='--', color='k')
    # Plot scatter
    ax.scatter(mus, nus, np.zeros(len(mus),dtype='float32'),
               color='r')
    #//Plot scatter

    hist2d, mEdges, nEdges = np.histogram2d(mus,nus, bins=bins,
                                          range=[[0,rang],[0,rang]])
    
    plot_grid_triangular(ax, rang, mEdges[1:], nEdges[1:], colors)
     

#     print(mEdges)
#     print(nEdges)
    lhist = len(hist2d)
    for i in range(lhist):
        hist2d[i,lhist-1-i] *= 2

    mEdgesMid= mEdges[:-1] + (mEdges[1:] - mEdges[:-1])*0.375
    nEdgesMid= nEdges[:-1] + (nEdges[1:] - nEdges[:-1])*0.375

    muPos = np.zeros(bins*(bins+1)//2,dtype='float32')
    nuPos = np.zeros_like(muPos)
    dz = np.zeros_like(muPos)
    
    S = lambda k: k*(k+1)//2 # = 1+2+...+k
    l = len(mEdgesMid)
    for i, pos in enumerate(mEdgesMid):
        start = S(l)-S(l-i)     # = l+(l-1)+...+(l-i+1)
        end   = S(l)-S(l-(i+1)) # = l+(l-1)+...+(l-i+1)+(l-i)
        dz[start:end]  = hist2d[i,:l-i]
        muPos[start:end] = pos
        nuPos[start:end] = nEdgesMid[:l-i]
        # The diagonal bins are triangular (half), fix them
#         muPos[end-1] = mEdges[i] + (mEdges[i+1] - mEdges[i])*0.25
#         nuPos[end-1] = nEdges[l-i-1] + (mEdges[l-i] - mEdges[l-i-1])*0.25

    dmu = (mEdges[1] - mEdges[0])*0.25 * np.ones_like(muPos)
    dnu = (nEdges[1] - nEdges[0])*0.25 * np.ones_like(nuPos)
    
    for i, _ in enumerate(mEdgesMid):
        diag_pos = S(l)-S(l-(i+1))
        dmu[diag_pos-1] = (mEdges[i+1] - mEdges[i])*0.125  
        dnu[diag_pos-1] = (mEdges[l-i] - mEdges[l-i-1])*0.125  

    ax.bar3d(muPos, nuPos, np.zeros_like(muPos),
             dmu,
             dnu, 
             dz, 
             color='y', alpha=0.3)
# #            zsort='average')

    ax.set_xlabel('Membership')
    ax.set_xlim3d(-0.5, rang+0.5)
    ax.set_ylabel('Non-membership')
    ax.set_ylim3d(-0.5, rang+0.5)
    ax.set_zlabel('Number of occurences per area (square)')
    ax.set_zlim3d(0, max(dz) + 0.5)


