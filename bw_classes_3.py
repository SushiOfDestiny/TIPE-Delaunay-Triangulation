from primitives_points_aretes_2 import *


class delaunay_triangulation:
    def __init__(self, xmax, xmin, ymax, ymin, nuage):
        """xmax, xmin, ymax, ymin sont les dimensions du nuage"""
        self.triangles = []
        self.nuage = nuage
        # attributs du supertriangle
        self.e = 1
        self.A = (xmin-self.e, ymin-self.e)
        self.B = (xmin + 2*(xmax-xmin) + 3*self.e, ymin - self.e)
        self.C = (xmin - self.e, ymin + 2*(ymax-ymin)+3*self.e)

        superTriangle = Triangle(self.A, self.B, self.C)

        self.triangles.append(superTriangle)

    def __repr__(self):
        return f"{self.triangles}"

    def ajouterPoint(self, point: Point):
        """met à jour la triangulation avec point"""
        # recherche des triangles dont le CC contient le point à insérer
        mauvaisTriangles = []
        for triangle in self.triangles:
            [a, b, c] = triangle.sommets
            if contient2(a, b, c, point):
                mauvaisTriangles.append(triangle)

        # bord de l'enveloppe convexe des mauvais triangles = "trou polygonal".
        bordure = []
        for triangle in mauvaisTriangles:
            bordure.extend(triangle.aretesNonPartagees(mauvaisTriangles))

        for triangle in mauvaisTriangles:  # on supprime les mauvais triangles
            self.triangles.remove(triangle)

        for arete in bordure:
            nvTriangle = Triangle(arete[0], arete[1], point)
            self.triangles.append(nvTriangle)

    def supprimerSuperTriangle(self):
        """Suppression du super triangle initial"""
        for triangle in tuple(self.triangles):
            if triangle.a_pour_sommet([self.A, self.B, self.C]):
                self.triangles.remove(triangle)

    def creer(self):
        """ajoute les points du nuage et supprime le super triangle"""
        for point in self.nuage:
            self.ajouterPoint(point)
        self.supprimerSuperTriangle()

    def exportation(self):
        """Renvoie la liste des triangles comme liste de listes de taille 3 comprenant les indices des sommets dans la liste
        nuage. C'est pour afficher avec matplotlib"""

        ts = [[recherche_ind(t.sommets[0], self.nuage),
               recherche_ind(t.sommets[1], self.nuage),
               recherche_ind(t.sommets[2], self.nuage)]
              for t in self.triangles]

        return ts, self.triangles
