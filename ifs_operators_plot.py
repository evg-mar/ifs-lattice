import numpy as np


def infStd(*ifsets):
    mus = np.minimum(*[ifset[0] for ifset in ifsets])
    nus = np.maximum(*[ifset[1] for ifset in ifsets])
    return (mus,nus)

def supStd(*ifsets):
    mus = np.maximum(*[ifset[0] for ifset in ifsets])
    nus = np.minimum(*[ifset[1] for ifset in ifsets])
    return (mus,nus)
###
###
def infPi(*ifsets):
    mus = np.minimum(*[ifset[0] for ifset in ifsets])
    nus = np.minimum(*[ifset[1] for ifset in ifsets])
    return (mus,nus)

def supPi(*ifsets):
    mus = np.maximum(*[ifset[0] for ifset in ifsets])
    nus = np.maximum(*[ifset[1] for ifset in ifsets])
    if mus + nus > 1:
        # The result is not a correct IFS
        return None
    else:
        return (mus,nus)
##############
## Unary operators
##############
def neg(ifset):
    return (ifset[1], ifset[0])
##############
## Topological operators
##############

def incGeneral(ifset, alpha, beta, gamma_a, gamma_b):
    mus = ifset[0]
    nus = ifset[1]
    if not np.min(mus) < 1.0:
        print('incorrect input incGeneral')
        return ifset
        
#     nsu = ifset[1]
    if not gamma_a > 0.0:
        mus_rst = mus
    else:
        mu_slope = 1 / (1-gamma_a)    
        mus_rst = map(lambda mu: mu if(mu >= alpha) else \
                                    max(mu_slope*(mu - gamma_a*alpha), 0.0),
                   mus)
        mus_rst = list(mus_rst)
    nus_rst = map(lambda pair: pair[1] if pair[1] >= beta else \
                               min((1-gamma_b)*pair[1] + gamma_b*beta, 1-pair[0]),
                               zip(mus_rst,nus))
#     print("in incGeneral \n")    
    return (np.asarray(list(mus_rst)), np.asarray(list(nus_rst)))



def clGeneral(ifset, alpha, beta, gamma_a, gamma_b):
#     print("in clGeneral")
#     print(neg(ifset))
    result = neg(incGeneral(neg(ifset), beta, alpha, gamma_b, gamma_a))

    return result

###############################

def incGeneral2(ifset,alpha0, beta0, 
                      alpha, beta, 
                      gamma_a, gamma_b):
    mus = ifset[0]
    nus = ifset[1]
    if not np.min(mus) < 1.0:
        return ifset
#     nsu = ifset[1]
    if not gamma_a > 0.0:
        mus_rst = mus
    else:
        mu_slope = 1 / (1-gamma_a)
        dAlpha = alpha - alpha0
        dBeta  = beta  - beta0
        
        def f_inc(mu):
            if mu <= alpha0:
                return mu
            elif alpha0 < mu <= alpha0 + gamma_a*dAlpha:
                return alpha0
            elif alpha0 + gamma_a*dAlpha < mu <= alpha:
                return mu_slope*(mu - alpha) + alpha 
            else:
                return mu
            
        def g_cl(nu):
            if nu < beta0:
                return nu
            elif beta0 <= nu <= beta:
                return (1 - gamma_b)*(nu - beta) + beta
            else:
                return nu
                
        mus_rst = map(f_inc, mus)
        mus_rst = list(mus_rst)
    nus_rst = map(lambda pair: pair[1] if pair[1] >= beta else \
                               min(g_cl(pair[1]), 1-pair[0]),
                               zip(mus_rst,nus))
#     print("in incGeneral \n")    
    return (np.asarray(list(mus_rst)), np.asarray(list(nus_rst)))


def clGeneral2(ifset, alpha0, beta0, 
                      alpha, beta, 
                      gamma_a, gamma_b):
#     print("in clGeneral")
#     print(neg(ifset))
    result = neg(incGeneral2(neg(ifset), 
                             beta0, alpha0, 
                             beta, alpha, gamma_b, gamma_a))

    return result



