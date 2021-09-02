from random import shuffle

from optisolveapi.vector import Vector

_shuffle = shuffle


class Constraints:
    """Mix-in for CNF"""

    def constraint_unary(self, vec):
        for a, b in zip(vec, vec[1:]):
            self.add_clause([a, -b])

    def constraint_and(self, a, b, ab):
        # a=1 b=1 => ab=1
        self.add_clause([-a, -b, ab])
        # a=0 => ab=0
        self.add_clause([a, -ab])
        # b=0 => ab=0
        self.add_clause([b, -ab])

    def constraint_or(self, a, b, ab):
        # a=0 b=0 => ab=0
        self.add_clause([a, b, -ab])
        # a=1 => ab=1
        self.add_clause([-a, ab])
        # b=1 => ab=1
        self.add_clause([-b, ab])

    def constraint_eq(self, a, b, ab):
        # a=1 => b=1
        self.add_clause([-a, b])
        # b=0 => a=1
        self.add_clause([-b, a])

    # def SeqInc(self, vec):
    #     return [self.ONE] + list(vec)

    # def SeqAddConst(self, vec, c):
    #     return [self.ONE] * c + list(vec)

    # def SeqAdd(self, vec1, vec2):
    #     n1 = len(vec1)
    #     n2 = len(vec2)
    #     vec3 = [self.var() for i in range(n1 + n2)]
    #     ands = {}

    #     # self.constraint_unary(vec1)  # optional
    #     # self.constraint_unary(vec2)  # optional
    #     self.constraint_unary(vec3)

    #     for i in range(n1):
    #         ands[i, -1] = vec1[i]
    #         for j in range(n2):
    #             ands[i, j] = self.var()
    #             self.constraint_and(vec1[i], vec2[j], ands[i, j])
    #             ands[-1, j] = vec2[j]

    #     for isum in range(1, n1+n2+1):
    #         clause0 = [-vec3[isum-1]]
    #         for i in range(min(isum + 1, n1 + 1)):
    #             vi = vec1[i-1] if i else 0
    #             j = isum - i
    #             if j > n2:
    #                 continue
    #             vj = vec2[j-1] if j else 0

    #             # vec1[i] = 1, vec2[j] = 1 => vec3[i][isum] = 1
    #             clause = [vec3[isum-1], -vi, -vj]

    #             clause = [c for c in clause if c]
    #             self.add_clause(clause)

    #             clause0.append(ands[i-1, j-1])

    #         # FORALL i, j vec1[i] & vec2[j] = 0 => vec3[i][isum] = 0
    #         clause0 = [c for c in clause0 if c]
    #         self.add_clause(clause0)
    #     return vec3

    # def SeqAddMany(self, *vecs):
    #     lst = list(vecs)
    #     while len(lst) >= 2:
    #         lst2 = []
    #         shuffle(lst)
    #         while len(lst) >= 2:
    #             lst2.append(self.SeqAdd(lst.pop(), lst.pop()))
    #         if lst:
    #             lst2.append(lst.pop())
    #         lst = lst2
    #     return lst[0]

    # def SeqEq(self, vec1, vec2):
    #     if len(vec1) < len(vec2):
    #         self.add_clause([-vec2[len(vec1)]])
    #     elif len(vec2) < len(vec1):
    #         self.add_clause([-vec1[len(vec2)]])
    #     for a, b in zip(vec1, vec2):
    #         self.add_clause([a, -b])
    #         self.add_clause([-a, b])

    # def SeqEqConst(self, vec, c):
    #     assert 0 <= c <= len(vec)
    #     if c == 0:
    #         self.add_clause([-vec[0]])
    #     elif c == len(vec):
    #         self.add_clause([vec[-1]])
    #     else:
    #         self.add_clause(vec[c-1])
    #         self.add_clause(-vec[c])

    def Card(self, vec, limit=None, shuffle=False):
        """
        [Sinz2005]-like cardinality.
        Returns:
        [>=0, >=1, >=2, ..., >= len(vec)+1]
        =
        [TRUE, ..., ..., ..., FALSE]
        if limit is less, then the last one may not be added
        [>=0, >=1, >=2, ..., >= limit]

        limit = 2
        [0, 1, 2] l=3
        limit = 3
        [0, 1, 2, Z] l=4
        """
        if limit is None:
            nvars = len(vec)
            limit = len(vec) + 1
        else:
            nvars = min(limit, len(vec))

        assert vec
        if len(vec) == 1:
            res = [self.ONE, vec[0]]
            res += [self.ZERO] * (limit + 1 - len(res))
            return res

        if shuffle:
            vec = list(vec)
            _shuffle(vec)

        sub = self.Card(vec[:-1], limit=limit, shuffle=False)
        res = [self.ONE] + [self.var() for _ in range(nvars)]
        res += [self.ZERO] * (limit + 1 - len(res))
        var = vec[-1]

        # res[i] = card >= i

        # res[0] = True
        # res[1] = sub[1] | var
        self.constraint_or(sub[1], var, res[1])
        for i in range(2, nvars + 1):
            # res[i] = sub[i] | (sub[i-1] & var)
            if len(sub) >= i + 1 and sub[i] != self.ZERO:
                x0, x1, x2, x3 = sub[i], sub[i-1], var, res[i]

                # Sinz claims that if we encode Cardinality <= k
                # then clauses with -x3 can be dropped.
                # Indeed, this only would allow a bad assignment,
                # but a good one would still exist if and only if card <= k.
                # However, this seems to contradict with his claim
                # that LT_SEQ is decided by unit propagation.
                self.add_clause([x1, -x3])  # full is [x0, x1, -x3] but unarity gives x1 <= x0
                self.add_clause([x0, x2, -x3])
                self.add_clause([-x1, -x2, x3])
                self.add_clause([-x0, x3])
            else:
                assert i in (len(vec), limit)
                assert sub[i] == self.ZERO
                self.constraint_and(sub[i-1], var, res[i])
        return res

    def CardNeg(self, card):
        assert card[0] == self.ONE
        return card[:1] + [-v for v in card[1:][::-1]]

    def CardScale(self, card, k):
        assert card[0] == self.ONE
        n = len(card) - 1
        return card[:1] + [card[1+i//k] for i in range(n * k)]

    def CardLEk(self, card, k):
        n = len(card) - 1
        assert card[0] == self.ONE
        assert 0 <= k < n
        for i in range(k + 1, len(card)):
            if card[i] is self.ZERO:
                continue
            self.add_clause([-card[i]])

    def CardGEk(self, card, k):
        n = len(card) - 1
        assert card[0] == self.ONE
        assert 0 <= k <= n
        for i in range(k + 1):
            if card[i] is self.ONE:
                continue
            self.add_clause([card[i]])

    def CardAlignPad(self, a, b):
        n = min(len(a), len(b)) + 1
        a = list(a) + [self.ZERO] * (n - len(a))
        b = list(b) + [self.ZERO] * (n - len(b))
        return a, b

    def CardLE(self, a, b):
        # 1 0
        # 0 0
        a, b = self.CardAlignPad(a, b)
        n = len(a)

        # Bad (greater):
        # 1
        # 0
        for i in range(n):
            self.add_clause([-a[i], b[i]])

    # def SeqFloor(src, c):
    #     n = len(src)
    #     m = n // c
    #     dst = VarVec(m)
    #     for i in range(0, len(src), n):
    #         sub = src[i:i+c]
    #         if len(sub) != c:
    #             continue
    #         # dst = a & b & c

    #         # dst = 1 => a = 1
    #         # dst = 1 => b = 1
    #         vdst = dst[i//c]
    #         for vsrc in sub:
    #             S.add_clause([-vdst, vsrc])
    #         # dst = 0 => a = 0 v b = 0 v ...
    #         S.add_clause([vdst] + [-vsrc for vsrc in sub])
    #     return dst

    # def SeqCeil(src, c):
    #     n = len(src)
    #     m = (n + c - 1) // c
    #     dst = VarVec(m)
    #     for i in range(0, len(src), n):
    #         sub = src[i:i+c]
    #         # dst = a v b v c

    #         # dst = 0 => a = 0
    #         # dst = 0 => b = 0
    #         vdst = dst[i//c]
    #         for vsrc in sub:
    #             S.add_clause([vdst, -vsrc])
    #         # dst = 1 => a = 1 v b = 1 v ...
    #         S.add_clause([-vdst] + [vsrc for vsrc in sub])
    #     return dst

    # def SeqMultConst(self, src, c):
    #     res = []
    #     for v in src:
    #         res += [v] * c
    #     return res

    # def SeqLess(self, a, b):
    #     # 1 0
    #     # 0 0
    #     a, b = self.AlignPad(a, b)
    #     n = len(a)

    #     # Bad (equal):
    #     # 1 0
    #     # 1 0
    #     for i in range(n-1):
    #         self.add_clause([-a[i], -b[i], a[i+1], b[i+1]])

    #     # Bad (greater):
    #     # 1
    #     # 0
    #     for i in range(n):
    #         self.add_clause([-a[i], b[i]])

    def constraint_remove_lower(self, x: list, mx: int):
        clause = []
        x = list(x)
        while x:
            xx = x.pop()
            if mx & 1 == 0:
                clause.append(xx)
            mx >>= 1
        assert not mx
        self.add_clause(clause)

    def constraint_remove_upper(self, x: list, mn: int):
        clause = []
        x = list(x)
        while x:
            xx = x.pop()
            if mn & 1 == 1:
                clause.append(-xx)
            mn >>= 1
        assert not mn
        self.add_clause(clause)

    def constraint_convex(self, xs, lb=None, ub=None):
        if lb:
            for mx in lb:
                self.constraint_remove_lower(xs, mx)
        if ub:
            for mn in ub:
                self.constraint_remove_upper(xs, mn)

    def Convex(self, xs, m=None, lb=None, ub=None):
        if m is None:
            m = len(xs)
        ys = self.vars(m)
        self.constraint_convex(Vector(xs).concat(ys), lb=lb, ub=ub)
        return ys

    def constraint_matching(S, u, v, mat, UB=True):
        assert len(mat) == len(v)
        assert len(mat[0]) == len(u)
        e = [
            [None] * len(u) for _ in range(len(v))
        ]

        for y in range(len(v)):
            for x in range(len(u)):
                if mat[y][x]:
                    e[y][x] = S.var()
                    # e_yx => v_y
                    # e_yx => u_x
                    S.add_clause([-e[y][x], v[y]])
                    S.add_clause([-e[y][x], u[x]])
        # copy
        for x in range(len(u)):
            col = [e[y][x] for y in range(len(v)) if mat[y][x]]
            card = S.Card(col, limit=2)
            S.CardLEk(card, 1)
            # enforce outgoing
            # u[x] => card >= 1
            S.add_clause([-u[x], card[1]])

        # xor
        for y in range(len(v)):
            row = [e[y][x] for x in range(len(u)) if mat[y][x]]
            card = S.Card(row, limit=2)
            S.CardLEk(card, 1)
            # enforce incoming (UB)
            # v[y] => card >= 1
            if UB:
                S.add_clause([-v[y], card[1]])
