from creation_triangulation_2 import *


def angle(a, b, c) -> float:
    """Renvoie l'angle dans [0,pi] entre les 2 Vecteurs ab ac"""
    u, v = vec(a, b), vec(a, c)
    cos = np.dot(u, v) / (norme(u) * norme(v))
    return np.arccos(cos)


def angle2(u: Vecteur, v) -> float:
    """Renvoie l'angle dans [0,pi] entre les 2 Vecteurs u v"""
    cos = np.dot(u, v) / (norme(u) * norme(v))
    return np.arccos(cos)


def calcul_angles(triangles: [Triangle]) -> (float, float):
    """Renvoie le plus petit angle de la liste triangles"""
    a_min = math.pi
    for triangle in triangles:
        [a, b, c] = triangle.sommets
        angles = [angle(a, b, c), angle(b, c, a), angle(c, a, b)]
        a_min = min(a_min, min(angles))

    return a_min


def angles(n_min, n_max, pas, nb_mes, m):
    """Renvoie l'abscisse x et, pour les 2 algorithmes NDT et BW, les ordonnées y,z tels que y[i] est la moyenne de l'angle 
    minimal de la triangulation calculée sur nb_mes nuages de taille x[i].
    z[i] est la moyenne de l'angle moyen de la triangulation.
    m est un majorant des coordonnées des points pour l'algorithme BW.
    """
    x = np.linspace(n_min, n_max, pas).astype(int)
    y_bw = []
    y_ndt = []

    for n in x:
        angle_min_moy_bw = 0
        angle_min_moy_ndt = 0

        for mesure in range(nb_mes):
            coord = do.creer_coord_aleat(n, m)

            liste_triangles1_bw, liste_triangles2_bw = exporter_bw(
                coord, m, 0, m, 0)
            a_min_bw = calcul_angles(liste_triangles2_bw)
            angle_min_moy_bw += a_min_bw

            liste_triangles1_ndt, liste_triangles2_ndt = exporter_ndt(coord)
            a_min_ndt = calcul_angles(liste_triangles2_ndt)
            angle_min_moy_ndt += a_min_ndt

        angle_min_moy_bw /= nb_mes

        angle_min_moy_ndt /= nb_mes

        y_bw.append(angle_min_moy_bw)
        y_ndt.append(angle_min_moy_ndt)

    return x, y_bw, y_ndt


def affiche_angles(n_min, n_max, pas, nb_mes, m):
    """Affiche pour chaque algorithme NDT,BW, y et z en fonction de x (avec les définitions de la fonction angles)"""
    x, y_bw, y_ndt = angles(n_min, n_max, pas, nb_mes, m)

    fig, ax = plt.subplots()

    ax.plot(x, y_bw, label='bw')
    ax.plot(x, y_ndt, label='ndt')
    ax.legend()

    ax.set_xlabel("Taille du nuage")
    ax.set_ylabel("Angle (radian)")

    plt.title("Angle minimal." + " n_min= " + str(n_min) + " n_max= " + str(n_max) +
              " pas= " + str(pas) + " nb_mes= " + str(nb_mes) + " m= " + str(m))

    plt.show()
