from primitives_points_aretes_2 import *
import matplotlib.pyplot as plt
import matplotlib.tri as triang
import random as rd
import donnees_2 as do
import time as tm
import bw_classes_3 as bw
import ndt_algo4 as ndt
import dc_valide as dc

import sys
sys.setrecursionlimit(100000)


def afficher_nuage(coord):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    plt.scatter(coord[0], coord[1])
    plt.show()


def creer_ndt(coord):
    """Créer la triangulation avec l'algorithme NDT, de complexité celle de NDT."""
    nuage = creer_nuage(coord[0], coord[1])
    triangulation = ndt.TriangulationNDT(nuage)
    triangulation.creer()


def creer_bw(coord, xmax, xmin, ymax, ymin):
    """Créer la triangulation avec l'algorithme BW, de complexité celle de BW."""
    nuage = creer_nuage(coord[0], coord[1])
    triangulation = bw.delaunay_triangulation(xmax, xmin, ymax, ymin, nuage)
    triangulation.creer()


def creer_dc(coord):
    """Créer la triangulation avec l'algorithme SL, de complexité celle de SL."""
    nuage = creer_nuage(coord[0], coord[1])
    triangulation = dc.delaunay_triangulation(nuage)
    triangulation.creer(triangulation.nuage_trie)
    return triangulation.succ


def exporter_bw(coord, xmax, xmin, ymax, ymin):
    """Renvoie 2 listes : celle des indices des points de sommets des triangles 
    pour l'affichage matplotlib et celle des triangles de la triangulation.
    En O(n**2)"""
    nuage = creer_nuage(coord[0], coord[1])
    triangulation = bw.delaunay_triangulation(xmax, xmin, ymax, ymin, nuage)
    triangulation.creer()
    return triangulation.exportation()


def exporter_ndt(coord):
    """Renvoie 2 listes : celle des indices des points de sommets des triangles 
    pour l'affichage matplotlib et celle des triangles de la triangulation.
    En O(n**2)"""
    nuage = creer_nuage(coord[0], coord[1])
    triangulation = ndt.TriangulationNDT(nuage)
    triangulation.creer()
    return triangulation.exportation()


def afficher_triangulation(coord, liste_triangles):
    """Utilise le module matplotlib"""
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.triplot(triang.Triangulation(
        coord[0], coord[1], liste_triangles), 'bo--', color='C0')

    plt.show()


def tracer_segment(a, b):
    """Trace sur une figure matplotlib le segment entre les points a et b, 
    de type float tuple"""
    x, y = [a[0], b[0]], [a[1], b[1]]
    plt.plot(x, y, marker='o', color='C0')


def afficher_triangulation_dc(succ):
    """Entrée : le dictionnaire succ d'une triangulation dc.
    Sortie : affiche avec Matplotlib la triangulation en traçant les arêtes une par une.
    Remarque : je ne sais pas comment former les triangles de la triangulation à partir
    de succ. """
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    for (a, b) in succ:
        tracer_segment(a, b)

    plt.show()
