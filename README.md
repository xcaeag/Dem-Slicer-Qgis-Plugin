[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Flake8](https://img.shields.io/badge/flake8-enabled-yellowgreen)](https://flake8.pycqa.org/)

a QGis (3.10) plugin...

Attention : doc for v0.1. Adaptations are coming soon !

- [D.E.M. Slicer (en)](#dem-slicer-en)
  - [Prerequisites](#prerequisites)
  - [Examples](#examples)
    - [Basic use](#basic-use)
    - [Orthogonal view](#orthogonal-view)
    - [Ornementations](#ornementations)
  - [The layers produced](#the-layers-produced)
    - [Lines](#lines)
    - [Polygons](#polygons)
    - [Ridges](#ridges)
    - [Ornementation (points)](#ornementation-points)
    - [Compass](#compass)
  - [The parameters in detail](#the-parameters-in-detail)
  - [The styles](#the-styles)
- [D.E.M. Slicer (fr)](#dem-slicer-fr)
  - [Les prérequis](#les-prérequis)
  - [Exemples](#exemples)
    - [Un fonctionnement basique.](#un-fonctionnement-basique)
    - [Ergonomie](#ergonomie)
    - [La vue orthogonale](#la-vue-orthogonale)
    - [Ornementations](#ornementations-1)
  - [Les couches produites](#les-couches-produites)
    - [Lignes](#lignes)
    - [Polygones](#polygones)
    - [Crêtes](#crêtes)
    - [Ornementation (points)](#ornementation-points-1)
    - [Boussole](#boussole)
  - [Les paramètres en détail](#les-paramètres-en-détail)
  - [Les styles](#les-styles)


# D.E.M. Slicer (en)

It is a simple cutting tool (in slices) of DEM data, to draw pretty postcards, for lovers of reliefs.

The principle is to build a series of altitude profiles (lines or polygons), to juxtapose them to give the illusion of a 3D view. Here, no calculation of the atmospheric refractive index, no consideration of the Earth's curvature ... just a little geometry, and the styles do the rest. The resulting layers are positioned where you want, the coordinate system used is that of the map (prefer 3857 rather than 4326 -in degrees-).

The offsets (varied according to the parameters chosen) in height of each cut simulate parallel or perspective views, a 'radial' vision attempts to get closer to the vision that an observer can have.

A 'ridge line' calculation enhances the reliefs.


## Prerequisites
- have an altitude raster image. different possible sources: https://dwtkns.com/srtm30m/, https://opendem.info, https://grindgis.com/data/free-world-dem-data
- to work in a projection whose unit coincides with the altimetric unit of the DEM (3857, WGS 84 / Pseudo-Mercator for example).

## Examples

### Basic use
Choice of the zone (use of the handles), selection of the layer which carries the altitudes, adjustment of some parameters and results.

Default view : the profiles follow arcs of an iso-distance to the observer.

![Basic use](dem_slicer/help/dem-demo-1.gif)

### Orthogonal view

![Vue ortho](dem_slicer/help/dem-demo-2.gif)

### Ornementations

The selected point layer will be 'projected' on the profiles. An attribute indicates whether the point thus projected is visible (hidden or not by a section). The default style uses the fields 'name' or 'label' for labeling.

A line layer or polygons will be cut by the profile lines, each vertex replaced in altitude. Result often badly done and very time consuming. Please note: cancellation is not possible, test on small data set.

![P.O.I.](dem_slicer/help/dem-demo-3.gif)

## The layers produced

### Lines
Attributes :

    "demslicer_num" - line number. Zero starting at the bottom.

![layer line](dem_slicer/help/ex_line.png)

### Polygons
Attributes :

    "demslicer_num" - polygone number.

![layer polygon](dem_slicer/help/ex_poly.png)

### Ridges
Attributes :

    "demslicer_gaz" - number of profiles that this crest hides
    "demslicer_prof" - 'depth' of the ridge (0 = close...)

![layer ridge](dem_slicer/help/ex_ridge.png)

### Ornementation (points)
Attributes (added to the attributes of the original layer) :

    "demslicer_num" - point number.
    "demslicer_z" - calculated altitude.  
    "demslicer_depth" - distance to observer
    "demslicer_visi" - visibility in the cutting series (0: hidden, 1: visible)
    "demslicer_prof" - 
    "demslicer_azimuth" - azimuth from observer

### Compass 

## The parameters in detail

linecount : it is simply the number of profiles (sections) generated.

![linecount](dem_slicer/help/dem-demo-linecount.gif)

xStep : distance between two altitude measurements, along the profiles.

![xstep](dem_slicer/help/dem-demo-xstep.gif)

zShift : vertical offset of the profiles. Makes the cuts in the background more visible. 'Aerial view' effect.

![zshift](dem_slicer/help/dem-demo-zshift.gif)

zFactor : accentuation of the relief.

![zfactor](dem_slicer/help/dem-demo-zfactor.gif)

elevation : Altitude of the observer relative to the ground. Like 'zShift', influences the vertical offset of the sections, more faithful to reality.

![elevation](dem_slicer/help/dem-demo-elevation.gif)

## The styles

Colors, transparency, texture ... everything is possible with QGis!

The attributes carried by the geometries can be used to adjust styles. For example, the thickness of the ridge lines can vary depending on the number of profiles that are hidden by the ridge (attribute 'gaz') :

    scale_linear( coalesce( "gaz", maximum("gaz")/3) , 0, maximum("gaz"), 0.05, 0.8)

![style line](dem_slicer/help/ex_line.png)

![style polygon](dem_slicer/help/ex_polygon.png)

![style polygon](dem_slicer/help/ex_texture.png)


# D.E.M. Slicer (fr)

![ex1](dem_slicer/help/all.png)

Il s'agit d'un outil simple de découpe (en tranches !) de Modèle numérique de terrain (MNT), pour produire de belles images à destination des amoureux de reliefs.

Le principe est de construire une série de profils d'altitudes (sous forme de lignes ou de polygones), de les juxtaposer pour donner l'illusion d'une vue 3D. Ici, pas de calcul de l'indice de réfraction atmosphérique, pas de prise en compte de la courbure terrestre... juste un peu de géométrie, et les styles font le reste. Les couches résultantes sont positionnées où bon vous semble, le système de coordonnées utilisé est celui de la carte (métrique).

La vue 'perspective' par défaut propose un rendu plus proche de la réalité (par rapport aux versions précédentes, et à la vue orthogonale).

Un calcul de 'ligne de crête' rehausse les reliefs.

La projection de points (sommets par exemple), de lignes (rivières ?), de polygones est vraiment une fonctionalité expérimentale (se méfier de la volumétrie).

## Les prérequis
- disposer d'un image (raster) d'altitude (MNT). différentes sources possibles : https://dwtkns.com/srtm30m/, https://opendem.info, https://grindgis.com/data/free-world-dem-data
- de travailler dans une projection dont l'unité coïncide avec l'unité altimétrique du MNT (le mètre par exemple pour la projection Lambert93 ou 3857, pseudo mercator).

## Exemples

### Un fonctionnement basique.
Choix de la zone (utilisation des poignées), sélection de la couche qui porte les altitudes, ajustement de quelques paramètres et résultats  :

![Démo simple](dem_slicer/help/dem-demo-1.gif)

### Ergonomie

Les différentes poignées permettent de dimensionner, positionner les coupes et le rendu final.

Les profils "échantillons" se dessinent immédiatement.

![ergonomie-fr](dem_slicer/help/ergonomie-fr.png)


### La vue orthogonale
Les coupes suivent alors des lignes droites, l'observateur n'est plus le "point bleu" mais se déplace latéralement. Les options de décalage des profils peuvent simuler une prise d'altitude.

![Vue ortho](dem_slicer/help/dem-demo-2.gif)

### Ornementations

La couche de points choisie sera 'projetée' sur les coupes. Un attribut indique si le point ainsi projeté est masqué ou non par une coupe. Le style par défaut utilise les champs 'nom', 'name' ou 'label' pour étiquetage.

Une couche de ligne ou polygones sera découpée par les lignes de profils, chaque sommet de la géométrie replacé en altitude. Résultat souvent imparfait. Attention : annulation impossible, faire des tests sur petit jeu de données.

![P.O.I.](dem_slicer/help/dem-demo-3.gif)

## Les couches produites

### Lignes
Attributs :

    "demslicer_num" - numéro de la ligne. Le zéro commençant au fond.

![layer line](dem_slicer/help/ex_line.png)

### Polygones
Attributs :

    "demslicer_num" - numéro du polygone. Le zéro commençant au fond.

![layer polygon](dem_slicer/help/ex_poly.png)

### Crêtes
Attributs :

    "demslicer_gaz" - nombre de profils que cette crête cache.
    "demslicer_prof" - 'profondeur' de la crête (0 = proche...)

![layer ridge](dem_slicer/help/ex_ridge.png)

### Ornementation (points)
Attributs (ajoutés aux attributs de la couche originale) :

    "demslicer_num" - numéro du point.
    "demslicer_z" - altitude calculée.  
    "demslicer_depth" - distance à l'observateur
    "demslicer_visi" - visibilité dans la série de coupe (0 : masqué, 1 : visible)

![layer POI](dem_slicer/help/ex_ornement.png)

### Boussole

## Les paramètres en détail

Nombre de profils : c'est tout simplement le nombre de coupes générées.

![linecount](dem_slicer/help/dem-demo-linecount.gif)

Ecart entre deux mesures d'altitude : distance entre deux points, le long des profils.

![xstep](dem_slicer/help/dem-demo-xstep.gif)

Décalage des profils : décalage vertical des coupes. Rend plus visible les coupes qui sont en arrière plan. Effet 'vue aérienne'.

![zshift](dem_slicer/help/dem-demo-zshift.gif)

Accentuation du relief : Exagération du relief (multiplication).

![zfactor](dem_slicer/help/dem-demo-zfactor.gif)

Obs : Altitude de l'observateur par rapport au sol. Comme le 'décalage en z', influ sur le décalage vertical des coupes, en plus fidèle à la réalité.

![elevation](dem_slicer/help/dem-demo-elevation.gif)

## Les styles

Couleurs, transparence, texture... tout est possible avec QGis !

Les attributs que portent les géométries peuvent servir à ajuster les styles. Par exemple, l'épaisseur des lignes de crête peut varier selon le nombre de profils qui sont cachés par la crête (attribut 'gaz') :

    scale_linear( coalesce( "gaz", maximum("gaz")/3) , 0, maximum("gaz"), 0.05, 0.8)
