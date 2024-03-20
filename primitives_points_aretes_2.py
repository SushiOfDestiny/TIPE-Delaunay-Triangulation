import numpy as np
import math
import copy

# les Points, Vecteurs et arêtes sont des float tuples
# Point contient x y qui sont les l'abscisse et l'ordonnée du point
# un objet de type Arete est un couple de Points (depart, arrivee) et représente une arête orientée

# coord : un tableau bidimensionnel 1ère ligne : abscisse, 2ème ligne : ordonnée
# nuage : un tableau de points de float tuple array

Point = tuple
Vecteur = tuple


def echange(t, i, j):
    """Echange en place les éléments aux indices i et j dans le tableau t"""
    t[i], t[j] = t[j], t[i]


# Tri rapide

def ind_piv(t, i, j):
    """ tab est un tableau de points t[i] est le point i. Déplace tous les éléments <= au pivot dans la partie gauche du sous-tableau t[i:j+1], et
    tous ceux > au pivot dans celle de droite, puis le pivot entre les 2 et renvoie son indice"""
    p = t[i]
    g = i + 1
    d = j
    while g <= d:
        if t[g] < p:
            g += 1
        else:
            echange(t, g, d)
            d -= 1
    if i < d:
        echange(t, i, d)
    return d


def tri_aux(t, i, j):
    """Tri le tableau t[k,j+1] en place"""
    if i < j:
        k = ind_piv(t, i, j)
        tri_aux(t, i, k - 1)
        tri_aux(t, k + 1, j)


def tri_rapide(nuage):
    """Trie par ordre lexicographique les points de coordonnées dans le tableau 2D 
    numpy coord"""
    n = len(nuage)
    tab_points = copy.deepcopy(nuage)  # liste des points
    tri_aux(tab_points, 0, n - 1)
    return tab_points


def recherche_ind(p: Point, coord) -> None or int:
    """
    Renvoie, s'il existe, l'indice de la première occurrence de p dans coord
    """
    for i, q in enumerate(coord):
        if p == q:
            return i
    return None


def intervalle(u, v):
    """Pour u < v deux entiers, il y a v - u - 1 entiers dans ]u,v["""
    return v-u-1


def vec(A: Point, B: Point) -> Vecteur:
    return (B[0] - A[0], B[1] - A[1])


def norme(v: Vecteur) -> float:
    return math.sqrt(np.dot(v, v))


def egalite_aretes(a1, a2):
    """Teste l'égalité de 2 arêtes, sans tenir compte de l'orientation"""
    return (a1 == a2) or (a1 == (a2[1], a2[0]))


# Soient 3 points non alignés a,b,c.
# Alors le triangle abc est direct ssi
# l'angle orienté entre les vecteurs ab et ac est > 0


def orientation(a, b, c) -> bool:
    """le signe du déterminant renvoyé est celui de l'angle entre les vecteurs ab et ac.
    Renvoie True ssi a,b,c sont dans le sens trigonométrique. On ne traite pas le cas où ils sont alignés.
    """
    M = [[a[0], a[1], 1],
         [b[0], b[1], 1],
         [c[0], c[1], 1]]
    det = np.linalg.det(M)
    return det > 0


def orientation2(a: Point, b, c) -> bool:
    """le signe du déterminant calculé est celui de l'angle entre les vecteurs ab et ac.
    Renvoie True ssi a,b,c sont dans le sens trigonométrique. On ne traite pas le cas où ils sont alignés."""

    m = [[a[0] - c[0], a[1] - c[1]],
         [b[0] - c[0], b[1] - c[1]]]
    det = np.linalg.det(m)
    return det > 0


def a_droite_de(p, arete) -> bool:
    """est vrai ssi le point p est à droite de l'arête orientée arete"""
    (a, b) = arete
    return orientation2(a, p, b)


def contient(a, b, c, d) -> bool:
    """Renvoie True ssi le point d est à l'intérieur du Cercle Circonscrit au triangle abc 
    (ordre trigo). 
    """
    x, y = d
    M = [[a[0], a[1], a[0]**2 + a[1]**2, 1],
         [b[0], b[1], b[0]**2 + b[1]**2, 1],
         [c[0], c[1], c[0]**2 + c[1]**2, 1],
         [x, y, x**2 + y**2, 1]]
    det = np.linalg.det(M)
    return (det > 0)


def contient2(a, b, c, d) -> bool:
    """Renvoie True ssi le point d est à l'intérieur du Cercle Circonscrit au triangle abc 
    (ordre trigo). """
    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = d
    m = [[ax - dx, ay - dy, (ax - dx) ** 2 + (ay - dy) ** 2],
         [bx - dx, by - dy, (bx - dx) ** 2 + (by - dy) ** 2],
         [cx - dx, cy - dy, (cx - dx) ** 2 + (cy - dy) ** 2]]
    d = np.linalg.det(m)
    return (d > 0)


class Triangle:
    def __init__(self, a, b, c):
        """a,b,c sont des points, on les stocke dans le sens trigonométrique"""
        if orientation2(a, b, c):
            self.sommets = [a, b, c]
        else:
            self.sommets = [b, a, c]

        self.aretes = [(a, b),
                       (b, c),
                       (c, a)]

    def __repr__(self):
        return f"[{self.sommets[0]}, {self.sommets[1]}, {self.sommets[2]}]"

    def a_pour_sommet(self, points):
        """Renvoie True si self a pour sommet un des points de la liste points.
        Sert pour supprimer les triangles touchant le supertriangle"""
        res = False
        for point in points:
            res = res or (point in self.sommets)
        return res

    def aretesNonPartagees(self, triangles):
        """Renvoie la liste des arêtes de self n'appartenant à aucun des triangles de la liste 'triangles' """
        nonPartagees = []
        for arete1 in self.aretes:
            estPartagee = False
            for triangle2 in triangles:
                if self == triangle2:
                    continue
                for arete2 in triangle2.aretes:  # on considère les 2 orientations de l'arête
                    if egalite_aretes(arete1, arete2):
                        estPartagee = True
            if not estPartagee:
                nonPartagees.append(arete1)
        return nonPartagees


def creer_nuage(listeX, listeY):
    """renvoie les points du nuage comme float tuple à partir de leurs coordonnées."""
    nuage = [(x, y) for (x, y) in zip(listeX, listeY)]
    return nuage

