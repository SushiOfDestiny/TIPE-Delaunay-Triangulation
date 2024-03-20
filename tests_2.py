from calcul_angles_2 import *
from complexite_temporelle_2 import *

plt.rc('font', size=20)  # controls default text size
plt.rc('axes', titlesize=20)  # fontsize of the title
plt.rc('axes', labelsize=20)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)  # fontsize of the x tick labels
plt.rc('ytick', labelsize=20)  # fontsize of the y tick labels
plt.rc('legend', fontsize=20)  # fontsize of the legend


# coord = do.creer_coord_aleat(5000, 10000000)
# coord = do.N6
# coord = do.creer_coord_aleat_disque(100, 50, 50, 50)
# coord = do.creer_coord_aleat_cercle(100, 50, 50, 50, 1)
# coord = do.creer_coord_aleat_carre(100, 100)

# afficher_nuage(coord)

# liste_triangles, triangles = exporter_ndt(coord)
# afficher_triangulation(coord, liste_triangles)

# for i in range(10):
#     coord = do.creer_coord_aleat(100,100)
#     liste_triangles,triangles = exporter_ndt(coord)
#     afficher_triangulation(coord, liste_triangles)

# liste_triangles2, triangles2 = exporter_bw(coord, 1000, 0, 1000, 0)
# afficher_triangulation(coord, liste_triangles2)


# ndt
# affiche_temps_ndt_dc(10,10000,10,10,100,0)

# bw
affiche_temps_bw(10,1000,10,10,10000)

# dc
# affiche_temps_ndt_dc(10,10000,10,10,100,2)

# a = calcul_angles(triangles)
# b = calcul_angles(triangles2)

# x, y_bw, z_bw, y_ndt, z_ndt = angles(10, 1000, 10, 50, 100)
# affiche_angles(10, 1000, 10, 30, 100000)

# s = creer_dc(coord)
# afficher_triangulation_dc(s)


# x,y = temps(10,100,10,1,2,100)
# affiche_temps(x,y,10,100,10,1,2)
