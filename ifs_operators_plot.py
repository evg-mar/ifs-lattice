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

def incGeneral(ifset, alpha, beta, gamma):
    mus = ifset[0]
#     nsu = ifset[1]
    mu_slope = 1 / (1-gamma)

    mus_rst = map(lambda mu: mu if(mu >= alpha) else \
                                max(mu_slope*(mu - gamma*alpha), 0.0),
               mus)
    nus_rst = map(lambda pair: pair[1] if pair[1] >= beta else \
                               min((1-gamma)*pair[1] + gamma*beta, 1 - pair[0]),
                               zip(*ifset))
#     print("in incGeneral \n")    
    return (np.asarray(list(mus_rst)), np.asarray(list(nus_rst)))

def clGeneral(ifset, alpha, beta, gamma):
#     print("in clGeneral")
#     print(neg(ifset))
    result = neg(incGeneral(neg(ifset), beta, alpha, gamma))

    return result






