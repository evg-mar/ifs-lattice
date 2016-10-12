from lattice import TriangPoset
from intuitionistic_fuzzy_set import *


class IfsPoset(TriangPoset):

    def __init__(self, triangPosetType):

        self._base_poset = triangPosetType()

    def eq(self, a, b):
        return (a[0] == b[0] and a[1] == b[1])

    def leq(self, a, b):
        return a[0] <= b[0] and a[1] >= b[1]

    def is_correct(self, ifs):

        return all([self._base_poset.is_correct(mu, nu) for mu, nu in ifs])

    def sup(self, *args):

        supports = [ifs.support_indices() for ifs in args]
        supp_indices = set.intersection(*supports)

        result = IFS(args[0].get_universe(), args[0].get_range())

        for idx in supp_indices:
            values = [ifs[idx] for ifs in args]
            result[idx] = self._base_poset.sup(*values)

        return result

    def inf(self, *args):

        result = IFS(args[0].get_universe(), args[0].get_range())

        for idx in args[0].indices():
            values = [ifs[idx] for ifs in args]
            val = self._base_poset.inf(*values)
            if val != STD_ZERO:
                result[idx] = val
