import abc


class TriangPoset(object):
    __metaclass__  = abc.ABCMeta

    def __init__(self, posetpool):
        self.posetpool = posetpool

    @abc.abstractmethod
    def eq(self, first, second):
         """Returns:
         True - iff the elements are equal in the poset.
         None - iff the elements are not comparable
         Raise exception iff they are not of comparable classes"""
         return

    @abc.abstractmethod
    def leq(self, first, second):
        return

    @abc.abstractmethod
    def sup(self, *args):
        return

    @abc.abstractmethod
    def inf(self, *args):
        return

    @abc.abstractmethod
    def is_correct(self, *args):
        return

    def neq(self, first, second):
         return not self.eq(first, second)

    def lt(self, first, second):
        return self.neq(first, second) and self.leq(first, second)

    def geq(self, first, second):
        return self.leq(second, first)

    def gt(self, first, second):
        return self.lt(second, first)


class StdTriangPoset(TriangPoset):

    def eq(self, a, b):
        return (a[0] == b[0] and a[1] == b[1])

    def leq(self, a, b):
        return a[0] <= b[0] and a[1] >= b[1]

    def is_correct(self, *elem):
        mu, nu = elem[0], elem[1]
        return (mu >= 0 and nu >= 0 and 0 <= mu + nu and mu + nu <= 1)

    def sup(self, *args):
#         if not self.is_correct(a):
#             raise AssertionError("First argument is not correct!")
#         if not self.is_correct(b):
#             raise AssertionError("Second argument is not correct!")



        mx = max([arg[0] for arg in args])
        mn = max([arg[1] for arg in args])

        return mx, mn

    def inf(self, *args):
#         if not self.is_correct(a):
#             raise AssertionError("First argument is not correct!")
#         if not self.is_correct(b):
#             raise AssertionError("Second argument is not correct!")

        mn = max([arg[0] for arg in args])
        mx = max([arg[1] for arg in args])

        return mn, mx

class PiTriangPoset(TriangPoset):

    def eq(self, a, b):
        return (a[0] == b[0] and a[1] == b[1])

    def leq(self, a, b):
        return a[0] <= b[0] and a[1] <= b[1]

    def is_correct(self, elem):
        mu, nu = elem[0], elem[1]
        return (mu >= 0 and nu >= 0 and 0 <= mu + nu and mu + nu <= 1)

    def sup(self, *args):
#         if not self.is_correct(a):
#             raise AssertionError("First argument is not correct!")
#         if not self.is_correct(b):
#             raise AssertionError("Second argument is not correct!")

        mu = max([arg[0] for arg in args])
        nu = max([arg[1] for arg in args])

        if self.is_correct(mu, nu):
            return mu, nu
        else:
            return None

    def inf(self, *args):
#         if not self.is_correct(a):
#             raise AssertionError("First argument is not correct!")
#         if not self.is_correct(b):
#             raise AssertionError("Second argument is not correct!")

        mu = min([arg[0] for arg in args])
        nu = min([arg[1] for arg in args])

        if self.is_correct(mu, nu):
            return mu, nu
        else:
            return None
