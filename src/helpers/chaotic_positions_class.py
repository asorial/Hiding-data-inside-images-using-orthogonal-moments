
import math


class BetaChaoticPositions:
    def __init__(self, k, a, b1, c1, b2, c2, x0, x1):
        self.k = k
        self.a = a
        self.b1 = b1
        self.c1 = c1
        self.b2 = b2
        self.c2 = c2
        self.x0 = x0
        self.x1 = x1
        self.p = self.b1 + self.c1 * self.a
        self.q = self.b2 + self.c2 * self.a

    def beta_fuction(self, x):
        xc = (self.p * self.x1 + self.q * self.x0) / (self.p + self.q)
        if x >= self.x0 and x <= self.x1:
            base_1 = (x - self.x0) / (xc - self.x0)
            base_2 = (self.x1 - x) / (self.x1 - xc)
            return base_1 ** self.p * base_2 ** self.q
        else:
            return 0

    def beta_chaotic_map(self, x, n):
        L = []
        for i in range(n):
            x = self.k * self.beta_fuction(x)
            L.append(int(math.floor(x * 10 ** (14) % n)))
        return L

    def list_reduced(self, L):
        R = []
        for i in L:
            if i not in R:
                R.append(i)
        return R

    def perm(self, L, ind):
        pos = []
        n = len(ind)
        for i in range(n):
            pos.append(L[ind[i]])
        return pos

    def set_diff(self, L1, L2):
        n = len(L2)
        for i in range(n):
            L1.remove(L2[i])
        return L1

    def chaotic_positions(self, x, L):
        pos = []
        ind = []
        ind = self.list_reduced(self.beta_chaotic_map(x, len(L)))
        pos = self.perm(L, ind)
        if len(pos) == 1:
            return L
        elif len(pos) == len(L):
            return pos
        else:
            return pos + self.chaotic_positions(x, self.set_diff(L, pos))
        return pos
