import matplotlib.pyplot as plt
from matplotlib import style

import numpy as np

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

def plot_triangle(ifs, ax, color='k', linewidth=1.5):
    min = 0.0
    max = ifs.get_range() - 1

    x_triang = [min, min, max, min]
    y_triang = [min, max, min, min]
    ax.set_xlim([min-(max-min)/30.0, max+(max-min)/30.0])
    ax.set_ylim([min-(max-min)/30.0, max+(max-min)/30.0])
    ax.set_xticks(np.arange(min, max+1, 1))
    ax.set_yticks(np.arange(min, max+1, 1))
    
    ax.plot(x_triang, y_triang, linewidth=linewidth, color=color)
    ax.set_xlabel('Membership')
    ax.set_xlabel('Non-membership')


def plot_triangular(ifs):
    fig = plt.figure()
    ax0 = plt.subplot2grid((1,1), (0,0))
    plot_triangle(ifs, ax0, 'k')
    indices, mus, nus, pis = ifs.elements_split()
    ax0.scatter(mus, nus, color='r')    
    
def plot_triangular_with_arrows(ifs):
    fig = plt.figure()
    ax0 = plt.subplot2grid((1,1), (0,0))
    
    plot_triangle(ifs, ax0)
    
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
    
    print(muS)
    print(nuS)
    head_width = 0.2*ifs.get_range()/30
    head_length = 0.5*ifs.get_range()/30
    for mu,c,nu,s  in zip(muS,Cos, nuS,Sin):
        delta = 0.001 # if direction >= 0 else -0.0001
        if(s is not np.nan):
            print(mu, nu, mu+c*delta, nu+s*delta)
            ax0.arrow(mu, nu, c*delta, s*delta,
                 head_width=head_width, head_length=head_length,
                 color='k')

   
    plt.title("Plot triangular with arrows")


def plot_3D_histogramm(ifs):
    pass

#     mus_plus_pis = [m+p for m,p in zip(mus,pis)]
#     ax0.plot(indices, mus, 'bo', linewidth=2,
#             label='Membership')
#     ax0.plot(indices, nus, 'go', linewidth=2,
#             label='Non-membership')
# 
#     ax0.fill_between(indices, 0, mus, facecolor='b', alpha=0.3)
#     ax0.fill_between(indices, 0, nus, facecolor='g', alpha=0.3)   
# #              mus_plus_pis, [ifs._range]*ifs.length(), 'g')
# 
#     ax0.set_xlabel('Universe')
#     ax0.set_ylabel('Degrees')    
#     plt.legend(loc='upper right')
#     plt.title('Intuitionistic plot type')




