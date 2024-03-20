from primitives_points_aretes_2 import *


class EnveloppeConvexe:
    def __init__(self, l):
        self.bord = l  # liste des sommets connexes sur la frontière de l'EC.
        # En parcourant les indices dans l'ordre croissant, on parcourt les sommets dans l'ordre trigonométrique
        self.m = 3  # nombre de sommets
        self.p = 2  # indice dans som du dernier sommet traité

    def elt(self, i: int) -> Point:
        """Renvoie le ième élément de la frontière modulo la taille de celle-ci"""
        return self.bord[i % self.m]

    def actualise(self, s_haut: int, s_bas, s: Point) -> None:
        """Remplace les sommets d'indices dans après s_bas et avant s_haut, strictement.
        par le point s.
        Complexité en temps constant.
        Met à jour self.p et self.m.
        nb est le nombre de sommets supprimés de self.bord"""

        # tentative 2
        if s_haut > s_bas:
            self.bord[s_bas + 1: s_haut] = [s]
            self.p = s_bas + 1
            nb = intervalle(s_bas, s_haut)

        else:  # s_haut < s_bas
            nb1 = intervalle(s_bas, self.m)
            self.bord[s_bas+1:] = [s]

            nb2 = s_haut
            self.bord[:s_haut] = []

            nb = nb1 + nb2

        self.p = s_bas + 1
        self.m += (1 - nb)  # 1 pour l'ajout de s


class TriangulationNDT:
    def __init__(self, nuage):
        self.points_non_tries = nuage  # on le garde pour l'exportation
        # nuage est un tableau numpy de n points
        # les points du nuage sont numérotés selon leur indice de ligne
        self.n = len(nuage)
        # tableau des points triés par ordre lexicographique
        self.points = tri_rapide(nuage)
        a, b, c = self.points[:3]
        self.triangles = [Triangle(a, b, c)]  # triangles
        self.conv = EnveloppeConvexe(self.points[:3])

    def ajouter_triangle(self, a: Point, b, c) -> None:
        """ajoute le triangle à la triangulation"""
        self.triangles.append(Triangle(a, b, c))

    def est_visible(self, M1: Point, M2, M3, S) -> bool:
        """Détermine si l'arête M1M2 est visible depuis S.
        M3 est le point suivant M2
        Renvoie True ssi les orientation_3s des triplets de points (M1,M2,M3) et (M1,M2;S) sont différentes"""
        return orientation2(M1, M2, M3) ^ orientation2(M1, M2, S)  # ^ signifie le OU exclusif

    def parcourir_enveloppe(self, S: Point, pas: int) -> int:
        """On parcourt la frontière à partir du dernier point tant que les arêtes sont
        rouges. On ajoute les triangles. 
        pas : incrémentation de l'indice, détermine le sens de parcours des indices des sommets de la frontière :
        pas = 1 ->  sens trigonométrique
        pas = -1 -> sens horaire"""
        i = self.conv.p
        iterer = True

        while iterer:
            M1 = self.conv.elt(i)
            M2 = self.conv.elt(i+pas)
            M3 = self.conv.elt(i+2*pas)
            # print(self.conv.bord)
            # print(self.est_visible(M1, M2,M3,S),M1,M2,M3,S)

            if self.est_visible(M1, M2, M3, S):
                self.ajouter_triangle(M1, M2, S)
                # print("ajout")
            else:
                iterer = False

            i += pas

        return i - pas
        # indice dans la frontière d'un des sommets violets.

    def inserer(self, s: Point):
        """Insère le sommet s dans la triangulation"""
        ind_s_haut = self.parcourir_enveloppe(s, 1)
        ind_s_bas = self.parcourir_enveloppe(s, -1)
        # self.conv.actualise(ind_s_haut, ind_s_hautas, s)
        self.conv.actualise(ind_s_haut, ind_s_bas, s)

    def creer(self):
        for i in range(3, self.n):
            self.inserer(self.points[i])
            # l'ordre triognométrique du bord de l'enveloppe convexe est assuré par le tri lexicographique

    def exportation(self):
        """Renvoie la liste des triangles comme liste de listes de taille 3 comprenant les indices des sommets dans la liste
        nuage. C'est pour afficher avec matplotlib.
        Fonctionne en O(n**2)"""

        ts = [[recherche_ind(t.sommets[0], self.points_non_tries),
               recherche_ind(t.sommets[1], self.points_non_tries),
               recherche_ind(t.sommets[2], self.points_non_tries)]
              for t in self.triangles]

        return ts, self.triangles
