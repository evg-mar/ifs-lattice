##############################################################################

def F_continuous_lower(t,
      alpha0, alpha, gamma_a
      # beta0,  beta, , gamma_b
      ):
    # lower - izpaknala function
    dAlpha = alpha - alpha0

    result = None

    if 0 <= t < alpha0:
        result = t
    elif alpha0 <= t < alpha0 + gamma_a * dAlpha:
        result = alpha0
    elif alpha0 + gamma_a * dAlpha <= t < alpha and gamma_a < 1.0:
        result = (1. / (1. - gamma_a) )*(t - alpha) + alpha
    elif alpha <= t <= 1:
        result = t
    else:
        raise AttributeError

    return result

def F_continuous_upper(t, alpha0, alpha, gamma_a):
    return 1.0 - F_continuous_lower(1.0 - t,
                                  alpha0  = 1.0 - alpha,
                                  alpha   = 1.0 - alpha0,
                                  gamma_a = 1.0 - gamma_a)

######################################################################
#####                               Spike                     ########
######################################################################
def F_spike_upper(t,
      alpha0, alpha, gamma_a):
    dAlpha = alpha - alpha0

    result = None

    if 0.0 <= t <= alpha0:
        result = t
    elif alpha0 <= t < alpha:
        result = (1. - gamma_a)*t + gamma_a*alpha
    elif alpha <= t <= 1.:
        result = t
    else:
        raise AttributeError

    return result

def F_spike_lower(t, alpha0, alpha, gamma_a):
    return 1.0 - F_spike_upper(1.0 - t,
                                 alpha0  = 1.0 - alpha,
                                 alpha   = 1.0 - alpha0,
                                 gamma_a = 1.0 - gamma_a)

##############################################################################
##############################################################################
##############################################################################

def incGeneral_single(
                        mu_type, # 'continuous' or 'spike'
                        nu_type, # 'continuous' or 'spike'
                        cut_type, # 'mu' or 'nu'
                        alpha0, alpha, gamma_a,
                       beta0, beta, gamma_b):

    assert 0.0 <= alpha0 <= alpha <= 1.0
    assert 0.0 <= gamma_a <= 1.0

    assert 0.0 <= beta0 <= beta <= 1.0
    assert 0.0 <= gamma_b <= 1.0

    assert mu_type in ['continuous', 'spike'] and nu_type in ['continuous', 'spike']
    assert nu_type in ['continuous', 'spike'] and nu_type in ['continuous', 'spike']
    assert cut_type in ['mu', 'nu']

    F_mu = F_continuous_lower if mu_type == 'continuous' else F_spike_lower
    F_nu = F_continuous_upper if nu_type == 'continuous' else F_spike_upper

    def inc_single(mu, nu):
        mu_inc = F_mu(mu, alpha0, alpha, gamma_a)
        nu_inc = F_nu(nu, beta0,  beta,  gamma_b)
        if cut_type == 'mu':
            nu_inc = min(nu_inc, 1 - mu_inc)
        elif cut_type == 'nu':
            mu_inc = min(mu_inc, 1. - nu_inc)
        else:
            raise AttributeError

        return mu_inc, nu_inc

    return inc_single


def clGeneral_single(
        mu_type, # 'continuous' or 'spike'
        nu_type, # 'continuous' or 'spike'
        cut_type, # 'mu' or 'nu'
                      alpha0, alpha, gamma_a,
                      beta0, beta, gamma_b):

    assert 0.0 <= alpha0 <= alpha <= 1.0
    assert 0.0 <= gamma_a <= 1.0

    assert 0.0 <= beta0 <= beta <= 1.0
    assert 0.0 <= gamma_b <= 1.0

    assert mu_type in ['continuous', 'spike'] and nu_type in ['continuous', 'spike']
    assert nu_type in ['continuous', 'spike'] and nu_type in ['continuous', 'spike']
    assert cut_type in ['mu', 'nu']

    F_mu = F_continuous_upper if mu_type == 'continuous' else F_spike_upper
    F_nu = F_continuous_lower if nu_type == 'continuous' else F_spike_lower

    def cl_single(mu, nu):

        mu_inc = F_mu(mu, alpha0, alpha, gamma_a)
        nu_inc = F_nu(nu, beta0,  beta,  gamma_b)
        if cut_type == 'mu':
            nu_inc = min(nu_inc, 1 - mu_inc)
        elif cut_type == 'nu':
            mu_inc = min(mu_inc, 1. - nu_inc)
        else:
            raise AttributeError

        return mu_inc, nu_inc


    return cl_single


if __name__ == "__main__":

    from matplotlib import pyplot as plt
    import numpy as np

    alpha0, alpha = .3, .8
    gamma_a = .3

    def plot_spike(alpha0, alpha, gamma_a):

        x = np.arange(0.0, 1.0, 0.001)
        # y_continuous_lower =[ F_continuous_lower(t, alpha0=alpha0, alpha=alpha, gamma_a=gamma_a) for t in x]
        # y_continuous_upper =[ F_continuous_upper(t, alpha0=alpha0, alpha=alpha, gamma_a=gamma_a) for t in x]


        y_spike_lower =[ F_spike_lower(t, alpha0=alpha0, alpha=alpha, gamma_a=gamma_a) for t in x]
        y_spike_upper =[ F_spike_upper(t, alpha0=alpha0, alpha=alpha, gamma_a=gamma_a) for t in x]

    # y_continuous_ =[ 1.0 - F_continuous(1-t,
    #                             alpha0= 1 - alpha,
    #                             alpha= 1 - alpha0,
    #                             gamma_a = 1- gamma_a) for t in x]
    # y_spike = [ F_spike(t, alpha0=alpha0, alpha=alpha, gamma_a=gamma_a) for t in x]

    # plt.plot(x, y_continuous_lower, color='r', label = 'Spike lower')
    # plt.plot(x, y_continuous_upper, color='blue', label = 'Spike upper')

        fig, ax = plt.subplots()

        ax.plot(x, y_spike_lower, color='r', alpha=0.5, label='Spike lower')
        ax.plot([alpha, alpha], [alpha - (1.-gamma_a)*(alpha-alpha0), alpha], '--', color='red',alpha=1.0)

        ax.plot(x, y_spike_upper, color='blue',alpha=0.5, label = 'Spike upper')
        ax.plot([alpha0, alpha0], [alpha0, alpha0 + gamma_a*(alpha-alpha0)], '--', color='blue',alpha=1.0)

        ax.plot([0., alpha], [alpha0 + gamma_a*(alpha-alpha0), alpha0 + gamma_a*(alpha-alpha0)], '--', color='black',
                linewidth = 0.5, alpha=0.9 )

        ax.plot([0., alpha0], [alpha0 , alpha0 ], '--', color='black',
                linewidth = 0.5, alpha=0.9 )

        ax.plot([0., alpha], [alpha , alpha ], '--', color='black',
                linewidth = 0.5, alpha=0.9 )


        ax.plot([alpha0, alpha0], [0.0 , alpha0 ], '--', color='black',
                linewidth = 0.5, alpha=0.9 )

        ax.plot([alpha, alpha], [.0 , alpha ], '--', color='black',
                linewidth = 0.5, alpha=0.9 )

        ax.set_xlabel('x')
        ax.set_ylabel('y')

        ax.set_xlim([0., 1.])
        ax.set_ylim([0., 1.])

        ax.set_xticks([0, alpha0,  alpha, 1])
        ax.set_xticklabels([0,
                            r'$\alpha_1$',
                            r'$\alpha_2$' ,
                            1])


        ax.set_yticks([0, alpha0, alpha0 + gamma_a*(alpha-alpha0), alpha, 1])
        ax.set_yticklabels([0, r'$\alpha_1$',
                            r'$\alpha_1 + \gamma.\Delta \alpha$',
                            r'$\alpha_2$',
                            1])

        ax.legend(loc="upper left")
        ax.set_aspect('equal', adjustable='box')
        plt.show()
    # plt.plot()



    def plot_continuous(alpha0, alpha, gamma_a):

        x = np.arange(0.0, 1.0, 0.001)
        y_continuous_lower =[ F_continuous_lower(t, alpha0=alpha0, alpha=alpha, gamma_a=gamma_a) for t in x]
        y_continuous_upper =[ F_continuous_upper(t, alpha0=alpha0, alpha=alpha, gamma_a=gamma_a) for t in x]


        # y_spike_lower =[ F_spike_lower(t, alpha0=alpha0, alpha=alpha, gamma_a=gamma_a) for t in x]
        # y_spike_upper =[ F_spike_upper(t, alpha0=alpha0, alpha=alpha, gamma_a=gamma_a) for t in x]


        # plt.plot(x, y_continuous_lower, color='r', label = 'Spike lower')
        # plt.plot(x, y_continuous_upper, color='blue', label = 'Spike upper')

        fig, ax = plt.subplots()

        ax.plot(x, y_continuous_lower, color='r', alpha=0.5, label='Continuous lower')
        # ax.plot([alpha, alpha], [alpha - (1.-gamma_a)*(alpha-alpha0), alpha], '--', color='red',alpha=1.0)

        ax.plot(x, y_continuous_upper, color='blue',alpha=0.5, label = 'Continuous upper')
        # ax.plot([alpha0, alpha0], [alpha0, alpha0 + gamma_a*(alpha-alpha0)], '--', color='blue',alpha=1.0)

        ax.plot([alpha0 + gamma_a*(alpha-alpha0), alpha0 + gamma_a*(alpha-alpha0)],[0., alpha],  '--', color='black',
                linewidth = 0.5, alpha=0.9 )

        ax.plot([alpha0 , alpha0 ],[0., alpha0], '--', color='black',
                linewidth = 0.5, alpha=0.9 )

        ax.plot([alpha , alpha ], [0., alpha],  '--', color='black',
                linewidth = 0.5, alpha=0.9 )


        ax.plot([0.0 , alpha0 ], [alpha0, alpha0],  '--', color='black',
                linewidth = 0.5, alpha=0.9 )

        ax.plot([.0 , alpha0 + gamma_a*(alpha-alpha0) ], [alpha, alpha],  '--', color='black',
                linewidth = 0.5, alpha=0.9 )

        ax.set_xlabel('x')
        ax.set_ylabel('y')


        ax.set_xlim([0., 1.])
        ax.set_ylim([0., 1.])

        ax.set_yticks([0, alpha0,  alpha, 1])
        ax.set_yticklabels([0,
                            r'$\alpha_1$',
                            r'$\alpha_2$',
                            1])


        ax.set_xticks([0,
                       alpha0, alpha0 + gamma_a*(alpha-alpha0), alpha,
                       1])
        ax.set_xticklabels([0,
                            r'$\alpha_1$',
                            r'$\alpha_1 + \gamma.\Delta \alpha$',
                            r'$\alpha_2$',
                            1])

        ax.legend(loc="upper left")
        ax.set_aspect('equal', adjustable='box')
        plt.show()
    # plt.plot()

    plot_continuous(alpha0=alpha0,
               alpha=alpha,
               gamma_a=gamma_a)



    plot_spike(alpha0=alpha0,
               alpha=alpha,
               gamma_a=gamma_a)

# def incGeneral2_single(mu, nu, alpha0, beta0, alpha, beta, gamma_a, gamma_b):
#     if

