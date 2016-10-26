from intuitionistic_fuzzy_set import IFS, STD_ZERO
from lattice import PiTriangPoset, StdTriangPoset, TriangPoset


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
        supp_indices = set.union(*supports)

        result = IFS(args[0].get_universe(), args[0].get_range())

        for idx in supp_indices:
            values = [ifs[idx] for ifs in args]
            val_ifs = self._base_poset.sup(*values)
            
            if val_ifs == STD_ZERO:
                continue
            elif val_ifs is not None:
                result[idx] = val_ifs
            else:
                raise AssertionError("Operation not defined!")

        return result

    def inf(self, *args):

        supports = [ifs.support_indices() for ifs in args]
        supp_indices = set.intersection(*supports)

        result = IFS(args[0].get_universe(), args[0].get_range())

        for idx in supp_indices:
            values = [ifs[idx] for ifs in args]
            val_ifs = self._base_poset.inf(*values)
            if val_ifs != STD_ZERO:
                result[idx] = val_ifs 

        return result

stdOrd = IfsPoset(StdTriangPoset)
piOrd  = IfsPoset(PiTriangPoset)
