from primitives_points_aretes_2 import *


class delaunay_triangulation:
    def __init__(self, nuage):
        self.succ = {}
        self.pred = {}
        self.first = {}
        self.nuage_trie = tri_rapide(nuage)

    def supprimer(self, a, b):
        sa = self.succ.pop((a, b))
        sb = self.succ.pop((b, a))
        pa = self.pred.pop((a, b))
        pb = self.pred.pop((b, a))
        self.succ[a, pa] = sa
        self.succ[b, pb] = sb
        self.pred[a, sa] = pa
        self.pred[b, sb] = pb

    def inserer(self, a, b, sa, pb):
        """sa tel que succ[a,b]=sa, pb tel que pred[b,a] = pb"""
        pa = self.pred[a, sa]
        sb = self.succ[b, pb]
        self.succ[a, pa] = b
        self.succ[a, b] = sa
        self.pred[a, sa] = b
        self.pred[a, b] = pa
        self.pred[b, sb] = a
        self.pred[b, a] = pb
        self.succ[b, pb] = a
        self.succ[b, a] = sb

    def plus_basse_tangente_commune(self, x0, y0) -> (float, float):
        """abrégée bt"""
        x, y = x0, y0
        z0 = self.first[y]
        z1 = self.first[x]

        z2 = self.pred[x, z1]
        while True:
            if a_droite_de(z0, (x, y)):
                y, z0 = z0, self.succ[z0, y]
            elif a_droite_de(z2, (x, y)):
                x, z2 = z2, self.pred[z2, x]
            else:
                return (x, y)

    def fusionner(self, x, y):
        """plus_haute_tangente_commune abrégée ht.
        On fait monter une arête entre les 2 triangulations"""

        # insertion de (x,y)
        sx = self.first[x]
        py = self.pred[y, self.first[y]]
        self.inserer(x, y, sx, py)

        # màj du bas de l'enveloppe convexe commune
        self.first[x] = y

        while True:  # tant que la plus haute tangente commune n'est pas atteinte
            if not a_droite_de(self.pred[y, x], (x, y)):  # balayage à droite
                y1 = self.pred[y, x]
                y2 = self.pred[y, y1]
                while contient2(x, y, y1, y2):  # suppression des triangles non de delaunay
                    self.supprimer(y, y1)
                    y1 = y2
                    y2 = self.pred[y, y1]
            else:
                y1 = None  # y est le point de droite de ht

            if not a_droite_de(self.succ[x, y], (x, y)):
                x1 = self.succ[x, y]
                x2 = self.succ[x, x1]
                while contient2(x, y, x1, x2):
                    self.supprimer(x, x1)
                    x1 = x2
                    x2 = self.succ[x, x1]
            else:
                x1 = None  # x est le point de gauche de ht

            if x1 is None and y1 is None:
                break
            elif x1 is None:  # cas particulier où l'un des points est extrémal
                self.inserer(y1, x, y, y)
                y = y1
            elif y1 is None:
                self.inserer(y, x1, x, x)
                x = x1

            elif contient2(x, y, y1, x1):  # aucun point n'est extrémal
                self.inserer(y, x1, x, x)
                x = x1  # on màj l'arête
            else:
                self.inserer(y1, x, y, y)
                y = y1

        # màj des informations sur le haut de l'enveloppe convexe commune.
        self.first[y] = x

    def creer(self, points):
        """points est un tableau de tuples triés par ordre lexicographique. Le 1er appel se fait sans paramètre donc
        sur le nuage initial trié."""
        n = len(points)

        if n == 2:
            [a, b] = points
            self.succ[a, b] = self.pred[a, b] = b
            self.succ[b, a] = self.pred[b, a] = a
            self.first[a] = b
            self.first[b] = a

        elif n == 3:
            [a, b, c] = points
            if orientation2(a, b, c):
                self.succ[a, c] = self.succ[c,a] = self.pred[a, c] = self.pred[c, a] = b
                self.succ[a, b] = self.succ[b,
                                            a] = self.pred[a, b] = self.pred[b, a] = c
                self.succ[b, c] = self.succ[c,
                                            b] = self.pred[b, c] = self.pred[c, b] = a
                self.first[a] = b
                self.first[b] = c
                self.first[c] = a
            else:
                self.succ[a, b] = self.succ[b, a] = self.pred[a, b] = self.pred[b, a] = c
                self.succ[a, c] = self.succ[c, a] = self.pred[a, c] = self.pred[c, a] = b
                self.succ[b, c] = self.succ[c, b] = self.pred[b, c] = self.pred[c, b] = a
                self.first[a] = c
                self.first[b] = a
                self.first[c] = b

        else:
            med = points[n//2]
            gauche = [p for p in points if p < med]
            droite = [p for p in points if p >= med]
            self.creer(gauche)
            self.creer(droite)
            x, y = self.plus_basse_tangente_commune(max(gauche), min(droite))
            self.fusionner(x, y)
