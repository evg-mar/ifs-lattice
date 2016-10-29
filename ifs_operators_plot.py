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






