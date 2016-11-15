from intuitionistic_fuzzy_set import IFS, STD_ZERO
from lattice import PiTriangPoset, StdTriangPoset, TriangPoset


cutLess = lambda x, alpha: x if (x > alpha) else 0.0

lowerLimit = lambda x, beta:  beta if (x < beta)  else x

def open01_(cons, val):
    mu_ = cutLess(val[0], cons[0])
    nu_ = lowerLimit(val[1], cons[1])
    return (mu_,nu_)

def open01(cons, ifs):
    result_ifs = IFS.from_IFS(ifs)
    for ind, val in ifs.emunerate_support_indeces():
        result_ifs[ind] = open01(cons, val)
    return result_ifs
