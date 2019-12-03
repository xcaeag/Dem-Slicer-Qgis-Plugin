# D.E.M. Slicer

![ex1](ex_poi.png)

Il s'agit d'un outil simple de découpe (en tranches !) de MNT, pour dessiner de jolies cartes postales, pour les amoureux de reliefs. 

Le principe est de générer une série de profils d'altitudes (sous forme de lignes ou de polygones), de les juxtaposer pour donner l'illusion d'une vue 3D. Ici, pas de calcul de l'indice de réfraction atmosphérique, pas de prise en compte de la courbure terrestre... juste un peu de géométrie, et les styles font le reste. Les couches résultantes sont positionnées où bon vous semble, le système de coordonnées utilisé est celui de la carte.

Les décalages (variés selon les paramètres retenus) en hauteur de chaque coupe simulent des vues parallèles ou 'perspective', une vision 'panoramique' tente de se rapprocher de la vision que peut avoir un observateur.

## Les prérequis
- disposer d'un image (raster) d'altitude (MNT). différentes sources possibles : https://dwtkns.com/srtm30m/, https://opendem.info, https://grindgis.com/data/free-world-dem-data
- de travailler dans une projection dont l'unité coincide avec l'unité altimétrique du MNT (le mètre par exemple pour la projection Lambert93). 

## Exemples

### Un fonctionnement basique. 
Choix de la zone (utilisation des poignées), sélection de la couche qui porte les altitudes, ajustement de quelques paramètres et résultats  : 

![ex1](dem-demo-1.gif)

### La vue 'panoramique' :
Les tranches de terrain suivent alors des arcs de cercle d'iso-distance à l'observateur.

![ex1](dem-demo-2.gif)

### Ornementations...

La couche de points choisie sera 'projetée' sur les coupes. Un attribut indique si le point ainsi projeté est visible (masqué ou non par une coupe). Le style par défaut utilise les champs 'nom', 'name' ou 'label' pour étiquetage.
Une couche de ligne ou polygones sera découpée par les lignes de profils, chaque sommet replacé en altitude. Résultat souvent mal fichu et très gourmant. Attention : annulation impossible, faire des tests sur petit jeu de données.

![ex1](dem-demo-3.gif)

## Les couches produites 

### Lignes
Attributs : 

    "num" - numéro de la ligne. Le zéro commençant au fond.

![ex1](ex_line.png)

### Polygones 
Attributs : 

    "num" - numéro du polygone. Le zéro commençant au fond.

![ex1](ex_poly.png)

### Crêtes
Attributs : 

    "num" - numéro de la ligne. 
    "gaz" - nombre de coupes que cette crête masque.  
    "prof" - 'profondeur' de la crête (0 = proche...)

![ex1](ex_ridge.png)

### Ornementation (points)
Attributs (ajoutés aux attributs de la couche originale) : 

    "num" - numéro du point. 
    "z" - altitude calculée.  
    "depth" - distance à l'observateur
    "visi" - visibilité dans la série de coupe (0 : masqué, 1 : visible)

![ex1](ex_ornement.png)

## Les paramètres en détail

linecount : c'est tout simplement le nombre de profils (de coupes) générés.
![linecount](dem-demo-linecount.gif)

xStep : distance entre deux mesures d'altitude, le long des profils. 
![xstep](dem-demo-xstep.gif)

zShift : décalage vertical des coupes. Rend plus visible les coupes qui sont en arrière plan. Effet 'vue aérienne'.
![zshift](dem-demo-zshift.gif)

zFactor : Exagération du relief.
![zfactor](dem-demo-zfactor.gif)

elevation : Altitude de l'observateur par rapport au sol. Comme 'zShift', influe sur le décalage vertical des coupes, en plus fidèle à la réalité. 
![elevation](dem-demo-elevation.gif)

## Les styles... 

![ex1](ex_line.png)

![ex1](ex_polygon.png)




