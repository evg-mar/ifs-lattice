import numpy as np
import copy
# import random
# from ifs_lattice import *
# from universal_set import *


STD_ZERO = (0, 1)
STD_ONE = (1, 0)

PI_ZERO = (0, 0)


class IFS(object):

    def __init__(self, universe, rang=None):

        self._universe = universe
        self._range = rang
        self._selector = {}

    @classmethod
    def from_IFS(cls, other):
        result = cls(other._universe, other._range)
        result._selector = copy.deepcopy(other._selector)
        return result

    @classmethod
    def random(cls, universe, rang, randseed=1):
        np.random.seed(randseed)
        #np.random.seed(a=randseed, version=2)
        result = cls(universe, rang)
        result._selector = {}

        sample = np.random.random((result._universe.length(), 2)) *\
                 (rang)
        for idx, (a,b) in enumerate(sample):            
            result._selector[idx] = (min(a,b), rang - max(a,b))

        return result
    
    @property
    def neg(self):
        result = IFS.from_IFS(self)
        result._selector = { }
        result._selector = {i: (nu,mu) 
                                    for i, (mu,nu) in self._selector.items()
                                    if (nu,mu) != STD_ZERO}
        indices = set(self.indices()) - set(self._selector.keys())
        result._selector.update({i:STD_ONE for i in indices})
        return result

    def __getitem__(self, key):

        if key not in self._universe.indices():
            raise KeyError("%i is not a valide index" % key)
        else:
            return self._selector.get(key, STD_ZERO)

    def set_bykey(self, key, value):
        self[self._universe.get_index(key)] = value

    def __setitem__(self, key, value):

        if key in self._universe.indices():
            self._selector[key] = value
        else:
            raise KeyError("%i is not a valide index" % key)

    def __str__(self):
        result = ("Ifs id: %d, Range: %d \n"% (id(self),self._range,))
        result += str(self._selector)
        return result  

    def get(self, idx, default=None):
        return self._selector.get(idx, default)

    def get_range(self):
        return self._range

    def get_universe(self):
        return self._universe

    def indices(self):
        return self._universe.indices()

    def support_indices(self):
        supp_idxes = [i for i, v in self._selector.items()
                                        if v != STD_ZERO
                     ]
        return set(supp_idxes)

    def enumerate_support_indeces(self):
        for i, v in self._selector.items():
            if v != STD_ZERO:
                yield (i,v)

    def elements_split(self):
        """
        Split and return the indices, mus and nus
        in the corresponding order.
        """
        items = sorted(list(self._selector.items()), key=lambda a: a[0])
        items = list(zip(*items))
        indices = items[0]
        values = list(zip(*items[1]))
        mus, nus = values[0], values[1]
        pis = tuple([self._range - m - n for m,n in items[1]])
        return indices, mus, nus, pis

    def length(self):
        return self._universe.length()

#    def update(self, universe):
#        self._universe = universe

#    def intersection(self, rhs):
 #       result = IndicesSet(self.universe)
 #       result._item = self._item & rhs._item
 #       return result

 #   def union(self, rhs):
  #      result = IndicesSet(self.universe)
 #       result._item = self._item | rhs._item
 #       return result
