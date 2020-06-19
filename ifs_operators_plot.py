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
## Inclusion operators
##############    
import collections 

def incl_j(musnus1, musnus2):
    # Set theoretical inclusion indicator
    holder = collections.OrderedDict([])
        
    # [((1, 2), (3, 4)), ((1, 2), (3, 4)), ((1, 2), (3, 4))]
    lst = list(zip(list(zip(musnus1[0], musnus1[1])), 
                   list(zip(musnus2[0], musnus2[1]))))

    def argwhere(filt):
        indices = np.argwhere(np.array(list(map(filt, lst)))==True) 
        indices = [x[0] for x in indices]    
        return indices

    #################################################################
    def eq_(a, b):
        return np.abs(a - b) < 1e-05
    
    def cmp(cmp_, munu1_munu2):
        munu1, munu2 = munu1_munu2[0], munu1_munu2[1]
        return cmp_(munu1[0], munu2[0]) and cmp_(munu1[1], munu2[1])

    def eq(munu1_munu2):
        return cmp(eq_, munu1_munu2)

    holder['e_eq'] = argwhere(eq)

    #################################################################

    def lt(munu1_munu2):
        munu1, munu2 = munu1_munu2[0], munu1_munu2[1]
        return munu1[0] < munu2[0] and munu1[1] > munu2[1] 

    def gt(munu1_munu2):
        munu1, munu2 = munu1_munu2[0], munu1_munu2[1]
        return munu1[0] > munu2[0] and munu1[1] < munu2[1] 

    holder['e_0'] = argwhere(lt), argwhere(gt)
    #################################################################

    def lt_pi(munu1_munu2):
        munu1, munu2 = munu1_munu2[0], munu1_munu2[1]
        return munu1[0] < munu2[0] and munu1[1] < munu2[1] 

    def gt_pi(munu1_munu2):
        munu1, munu2 = munu1_munu2[0], munu1_munu2[1]
        return munu1[0] > munu2[0] and munu1[1] > munu2[1] 

    holder['e_pi'] = argwhere(lt_pi), argwhere(gt_pi)

    #################################################################

    def lt_square(munu1_munu2):
        munu1, munu2 = munu1_munu2[0], munu1_munu2[1]
        return munu1[0] < munu2[0] and eq_(munu1[1], munu2[1]) 

    def gt_square(munu1_munu2):
        munu1, munu2 = munu1_munu2[0], munu1_munu2[1]
        return munu1[0] > munu2[0] and eq_(munu1[1], munu2[1]) 

    holder['e_square'] = argwhere(lt_square), argwhere(gt_square)
    #################################################################

    def lt_diam(munu1_munu2):
        munu1, munu2 = munu1_munu2[0], munu1_munu2[1]
        return eq_(munu1[0], munu2[0]) and munu1[1] > munu2[1] 

    def gt_diam(munu1_munu2):
        munu1, munu2 = munu1_munu2[0], munu1_munu2[1]
        return eq_(munu1[0], munu2[0]) and munu1[1] < munu2[1] 

    holder['e_diam'] = argwhere(lt_diam), argwhere(gt_diam) 

    #################################################################

    return holder
    
def incl_i(musnus1, musnus2):
    # Set theoretical inclusion indicator
    holder = incl_j(musnus1, musnus2)
    result = collections.OrderedDict()
    result['e_eq'] = len(holder['e_eq'])
    for key, pair in holder.items():
        if key != 'e_eq':
            result[key] = len(pair[0]), len(pair[1])
    return result

    
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

