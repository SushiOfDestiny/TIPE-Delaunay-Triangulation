import numpy as np
import random as rd

# Format d'un tableau de coordonnées coord: 2 lignes, n colonnes.
# coord[:,i] = [x,y] sont les coordonnées du i-ième point du nuage


def creer_coord_aleat(n, m):
    """Renvoie un tableau avec n points aléatoires de coordonnées réelles dans [0,m["""
    return [[rd.uniform(0, m) for i in range(n)],
            [rd.uniform(0, m) for i in range(n)]]


def dans_disque(x, y, x0, y0, r) -> bool:
    """Renvoie True ssi le point de coordonnées (x,y) est dans 
    le disque de centre (x0,y0) de rayon r"""
    return (x-x0)**2 + (y-y0)**2 <= r**2


def sur_cercle(x, y, x0, y0, r, eps) -> bool:
    """Renvoie True ssi le point de coordonnées (x,y) est sur le cercle de 
    centre (x0,y0) de rayon r, à la précision eps"""
    return abs((x-x0)**2 + (y-y0)**2 - r**2) <= eps


def creer_coord_aleat_disque(n, x0, y0, r):
    """Renvoie un tableau avec n points aléatoires dans le disque.
    Conditions : tous les points du disque sont à coordonnées positives. """
    listeX, listeY = [], []

    m = 0  # nombre de points
    while m < n:
        x, y = rd.uniform(0, 2*r), rd.uniform(0, 2*r)
        if dans_disque(x, y, x0, y0, r):
            listeX.append(x)
            listeY.append(y)
            m += 1

    return np.array([listeX, listeY])


def creer_coord_aleat_cercle(n, x0, y0, r, eps):
    """Renvoie un tableau avec n points aléatoires sur le cercle à eps près.
    Conditions : tous les points du disque sont à coordonnées positives. """
    listeX, listeY = [], []

    m = 0  # nombre de points
    while m < n:
        x, y = rd.uniform(0, 2*r), rd.uniform(0, 2*r)
        if sur_cercle(x, y, x0, y0, r, eps):
            listeX.append(x)
            listeY.append(y)
            m += 1

    return [listeX, listeY]


def creer_coord_aleat_carre(n, a):
    """Renvoie un tableau avec 4n points aléatoires sur le carré  à coordonnées positives et de côté a."""
    listeX, listeY = [], []
    for i in range(n):
        z = rd.uniform(0, a)

        listeX.append(z)
        listeY.append(0)
        listeX.append(z)
        listeY.append(a)

        listeX.append(0)
        listeY.append(z)
        listeX.append(a)
        listeY.append(z)

    return [listeX, listeY]
