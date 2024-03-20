from creation_triangulation_2 import *


def temps_1(n, m, algo):
    """Renvoie le temps d'exécution de triangulation sur 1 nuage de taille n, 
    dont les points sont dans le carré [0,m] x [0,m].
    algo indique l'algorithme utilisé :
    0 -> Non Delaunay
    1 -> Bowyer Watson
    2 -> Diviser Pour Régner"""
    coord = do.creer_coord_aleat(n, m)
    deb = tm.time()
    if algo == 0:
        creer_ndt(coord)
    elif algo == 1:
        creer_bw(coord, m, 0, m, 0)
    else:
        creer_dc(coord)

    fin = tm.time()
    return fin - deb


def temps(n_min, n_max, pas, nb_mes, algo, m):
    """Renvoie l'abscisse et l'ordonnée x,y tel que y[i] est le temps moyen 
    d'exécution de l'algorithme choisi sur nb_mes nuages de points de taille x[i]
    où x[i] varie de n_min à n_max avec un pas de pas.
    algo défini dans temps_1.
    m est un majorant des coordonnées des points pour l'algorithme BW."""
    x = np.linspace(n_min, n_max, pas).astype(int)
    y = []

    for n in x:
        tps_moy = 0
        for mesure in range(nb_mes):
            tps_moy += temps_1(n, m, algo)
        tps_moy /= nb_mes
        y.append(tps_moy)

    return x, y


def affiche_temps_ndt_dc(n_min, n_max, pas, nb_mes, m, algo):
    """Affiche la courbe f(x) = y et effectue une regression pour la comparer avec la 
    courbe théorique de complexité. 
    algo défini dans temps_1.
    m tel que les points sont dans [0,m[*[0,m[."""

    x, y = temps(n_min, n_max, pas, nb_mes, algo, m)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    nom = ["NDT", "BW", "DC"]
    ax1.set_title(nom[algo] + " n_min= " + str(n_min) + " n_max= " +
                  str(n_max) + " pas= " + str(pas) + " nb_mes= " + str(nb_mes), loc='left')

    ax1.set_xlabel("taille du nuage")
    ax1.set_ylabel("temps d'exécution (en secondes)")
    ax1.plot(x, y, label="empirique")
    ax1.legend()

    # nlogn
    reg = [x0 * np.log(x0) for x0 in x]
    ax2.set_ylabel("rapport du temps d'exécution sur f(n) = nlog(n)")

    y2 = [y0/z0 for (z0, y0) in zip(reg, y)]

    ax2.set_xlabel("taille du nuage")

    ax2.plot(x, y2, label="comparaison")
    ax2.legend()

    plt.show()


def affiche_temps_bw(n_min, n_max, pas, nb_mes, m):
    """Affiche la courbe f(x) = y et effectue une regression pour la comparer avec la 
    courbe théorique de complexité. 
    algo défini dans temps_1.
    m tel que les points sont dans [0,m[*[0,m[."""

    x, y = temps(n_min, n_max, pas, nb_mes, 1, m)

    fig, ax = plt.subplots()

    ax.set_xlabel("taille du nuage")
    ax.set_ylabel("temps d'exécution (en secondes)")
    ax.plot(x, y, label="empirique")

    reg = np.poly1d(np.polyfit(x, y, 2))(x)
    ax.plot(x, reg, label="théorique : f(x) = x^2")

    plt.title("BW" + " n_min= " + str(n_min) + " n_max= " +
              str(n_max) + " pas= " + str(pas) + " nb_mes= " + str(nb_mes))
    ax.legend()
    plt.show()
