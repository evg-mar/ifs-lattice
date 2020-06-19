"""
     Plot 3D
"""
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
from matplotlib import lines
from matplotlib import style
style.use('ggplot')

import numpy as np

from ifs_2Dplot import plot_triangle



def rotate_axislabels(ax, angles={'x': 45,'y': 45,'z': 45}):
    if 'x' in angles:
        for label in ax.xaxis.get_ticklabels():
            label.set_rotation(angles['x'])
    if 'y' in angles:
        for label in ax.yaxis.get_ticklabels():
            label.set_rotation(angles['y'])
    if 'z' in angles:
        for label in ax.zaxis.get_ticklabels():
            label.set_rotation(angles['z'])

    

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
                                colors={'mu':'b', 'nu':'g', 'elem':'r'},
                                alpha=0.3):
    
    bins = ifs.get_range()  if (bins is None) else bins 
        
    indices, mus, nus, pis = ifs.elements_split()
    rang = ifs.get_range()

    plot_triangle(rang, ax, plottyp='--', color='k')
    # Plot scatter
    ax.scatter(mus, nus, np.zeros(len(mus),dtype='float32'),
               color=colors['elem'])
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
    ############
    ax.set_xlabel('Membership', labelpad=20)
    ax.set_xlim3d(-d, rang+d)
    ax.set_xticks(muEdges, minor=False)
    ax.tick_params(axis='x', colors=colors['mu'])
    
    ax.set_ylabel('Non-membership', labelpad=20)
    ax.set_ylim3d(-d, rang+d)
    ax.set_yticks(nuEdges, minor=False)
    ax.tick_params(axis='y', colors=colors['nu'])    

    rotate_axislabels(ax, angles={'x':-45,'y':45})

    ax.set_zlabel('Number of occurences per area', labelpad=20)
    ###########
    ax.set_zlim3d(0, zLimit + 0.5)
      
    #Add a legend in 3D
    elemMapsLabel = lines.Line2D([0],[0], linestyle="none",
                               c=colors['elem'], marker = 'o')    
    muHistBars = plt.Rectangle((0, 0), 1, 1, fc=colors['mu'])
    nuHistBars = plt.Rectangle((0, 0), 1, 1, fc=colors['nu'])
      
    ax.legend([muHistBars, nuHistBars, elemMapsLabel],
              ['Membership histogram bins', 
               'Non-membership histogram bins', 
               'Map of the elements from the Universe'],
              numpoints = 2)



def plot_3D_histogramm(ifs,
                       bins=None,
                       colors={'mu':'b','nu':'g','hist':'y','elem':'r'}):
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
               color=colors['elem'])
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
             color=colors['hist'], alpha=0.3)
# #            zsort='average')

    d = rang/bins  # the length of a bin (area = length(bin)**2)
    
    ax.set_xlabel('Membership', labelpad=20)
    ax.set_xlim3d(-d, rang+d)
    ax.set_xticks(mEdges, minor=False)
    ax.tick_params(axis='x', colors=colors['mu'])
    
    ax.set_ylabel('Non-membership', labelpad=20)
    ax.set_ylim3d(-d, rang+d)
    ax.set_yticks(nEdges, minor=False)
    ax.tick_params(axis='y', colors=colors['nu'])    

    rotate_axislabels(ax, angles={'x':-45,'y':45})

    ax.set_zlabel('Number of occurences per area (square)', labelpad=20)
    ax.set_zlim3d(0, max(dz) + 0.5)
    
    #Add a legend in 3D
    muBinsLabel = lines.Line2D([0],[0], linestyle="none",
                               c=colors['mu'], marker = 0)
    nuBinsLabel = lines.Line2D([0],[0], linestyle="none",
                               c=colors['nu'], marker = 0)
    elemMapsLabel = lines.Line2D([0],[0], linestyle="none",
                               c=colors['elem'], marker = 'o')
    histBars = plt.Rectangle((0, 0), 1, 1, fc=colors['hist'])
    
    
    
    ax.legend([muBinsLabel, nuBinsLabel, histBars, elemMapsLabel],
              ['Membership degree grid', 
               'Non-membership degree grid', 
               "Histogram bars",
               "Map of the elements from the Universe"],
              numpoints = 2)
