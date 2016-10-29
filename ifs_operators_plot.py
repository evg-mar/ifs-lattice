import numpy as np


def infStd(*ifsets):
    mus = np.minimum(*ifsets)
    nus = np.maximum(*ifsets)
    return (mus,nus)

def supStd(*ifsets):
    mus = np.maximum(*ifsets)
    nus = np.minimum(*ifsets)
    return (mus,nus)
###
###
def infPi(*ifsets):
    mus = np.minimum(*ifsets)
    nus = np.minimum(*ifsets)
    return (mus,nus)

def supPi(*ifsets):
    mus = np.maximum(*ifsets)
    nus = np.maximum(*ifsets)
    if mus + nus > 1:
        # The result is not a correct IFS
        return None
    else:
        return (mus,nus)






