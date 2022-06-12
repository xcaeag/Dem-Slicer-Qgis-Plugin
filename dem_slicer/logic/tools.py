import math
import processing
from qgis.core import (QgsRasterLayer, QgsVectorLayer)
from qgis.PyQt.QtWidgets import QApplication
import os
from qgis.PyQt.QtCore import QLocale, QUrl, QDir
from qgis.PyQt.QtGui import QDesktopServices

DEFAULT_PARAMS = {
    "native:buffer": {'DISSOLVE' : False, 'END_CAP_STYLE' : 0, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2,'SEGMENTS' : 5},
    "native:bufferbym": {'SEGMENTS': 3},
    "native:difference": {'OPTIONS' : ''},
    "native:lineintersections": {'INPUT_FIELDS':[],'INTERSECT_FIELDS':[],'INTERSECT_FIELDS_PREFIX':''},
    "native:extenttolayer" : {}, # 'INPUT':'0.000000000,5760.000000000,-3840.000000000,0.000000000'
    "native:extractbyexpression" : {'EXPRESSION':' "DN" = 0'},
    "native:extractbyextent": {'CLIP' : True},
    "native:geometrybyexpression": {'OUTPUT_GEOMETRY':1,'WITH_Z':False,'WITH_M':True,'EXPRESSION':'$geometry'},
    "native:mergevectorlayers": {'CRS' : None},
    "native:multiparttosingleparts": {},
    "native:package": {'LAYERS':[],'OUTPUT':'/tmp/export.gpkg','OVERWRITE':False,'SAVE_STYLES':True,'SAVE_METADATA':True,'SELECTED_FEATURES_ONLY':False},
    "native:removeduplicatevertices" : {'USE_Z_VALUE' : False},
    "native:savefeatures": {'OUTPUT':'tmp.shp', 'LAYER_NAME':'tmp','DATASOURCE_OPTIONS':'','LAYER_OPTIONS':''},
    "native:setlayerstyle": {'STYLE':'xxx.qml'},
    "native:setmfromraster": {'BAND': 1,'SCALE': 1},
    "native:snappointstogrid": { 'HSPACING' : 1, 'MSPACING' : 0, 'VSPACING' : 1, 'ZSPACING' : 0 },
    "native:smoothgeometry": {'ITERATIONS':1,'OFFSET':0.3,'MAX_ANGLE':179},
    "native:transect": {'LENGTH':1,'ANGLE':90,'SIDE':0},
    "grass7:v.dissolve" : { 'GRASS_MIN_AREA_PARAMETER' : 0.0001, 'GRASS_OUTPUT_TYPE_PARAMETER' : 0, 'GRASS_REGION_PARAMETER' : None, 'GRASS_SNAP_TOLERANCE_PARAMETER' : -1, 'GRASS_VECTOR_DSCO' : '', 'GRASS_VECTOR_EXPORT_NOCAT' : False, 'GRASS_VECTOR_LCO' : '', 'column' : '' },
    "gdal:cliprasterbyextent" : {'OVERCRS':False,'NODATA':None,'OPTIONS':'','DATA_TYPE':0,'EXTRA':''}, # PROJWIN = extent
    "gdal:cliprasterbymasklayer": {'MASK':'','SOURCE_CRS':None,'TARGET_CRS':None,'TARGET_EXTENT':None,'NODATA':None,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,'KEEP_RESOLUTION':False,'SET_RESOLUTION':False,'X_RESOLUTION':None,'Y_RESOLUTION':None,'MULTITHREADING':False,'OPTIONS':'','DATA_TYPE':0,'EXTRA':''},
    "gdal:clipvectorbypolygon" :{'OPTIONS':''}, # 'INPUT':'memory://MultiLineString?crs=EPSG:3857&uid=.., 'MASK':'C:/...', ,'OUTPUT':'TEMPORARY_OUTPUT'
    "gdal:clipvectorbyextent": {'OPTIONS':''}, #
    "gdal:contour": {'BAND':1,'INTERVAL':10,'FIELD_NAME':'z','CREATE_3D':False,'IGNORE_NODATA':False,'NODATA':None,'OFFSET':0,'EXTRA':''},
    "gdal:contour_polygon": {'BAND':1,'INTERVAL':10,'CREATE_3D':False,'IGNORE_NODATA':False,'NODATA':None,'OFFSET':0,'EXTRA':'','FIELD_NAME_MIN':'ELEV_MIN','FIELD_NAME_MAX':'ELEV_MAX'},
    "gdal:hillshade": {'BAND':1,'Z_FACTOR':1,'SCALE':1,'AZIMUTH':315,'ALTITUDE':45,'COMPUTE_EDGES':False,'ZEVENBERGEN':False,'COMBINED':False,'MULTIDIRECTIONAL':False,'OPTIONS':'','EXTRA':''},
    "gdal:polygonize" : {'BAND':1,'FIELD':'DN','EIGHT_CONNECTEDNESS':False,'EXTRA':''}, # 'INPUT':'','OUTPUT':'TEMPORARY_OUTPUT'
    "gdal:rastercalculator" : {'BAND_A':1,'FORMULA':'A < 100','NO_DATA':None,'RTYPE':5,'OPTIONS':'','EXTRA':''}, # 'INPUT_A':'C:/...', 'INPUT_B':None,'BAND_B':None,'INPUT_C':None,'BAND_C':None,'INPUT_D':None,'BAND_D':None,'INPUT_E':None,'BAND_E':None,'INPUT_F':None,'BAND_F':None
    "gdal:translate" : {'TARGET_CRS':None,'NODATA':None,'COPY_SUBDATASETS':False,'OPTIONS':'','DATA_TYPE':0 },
    "grass7:v.out.svg": {'type':1,'precision':2,'attribute':['id', 'z'],'GRASS_REGION_PARAMETER':None,'GRASS_SNAP_TOLERANCE_PARAMETER':-1,'GRASS_MIN_AREA_PARAMETER':0.0001},
    "gdal:rasterize": {'FIELD':'id','BURN':0,'USE_Z':False,'UNITS':1,'WIDTH':5,'HEIGHT':5,'NODATA':0,'OPTIONS':'','DATA_TYPE':5,'INIT':None,'INVERT':False,'EXTRA':'', 'EXTENT':''},
    "gdal:fillnodata": {'BAND':1,'DISTANCE':10,'ITERATIONS':0,'NO_MASK':False,'MASK_LAYER':None,'OPTIONS':'','EXTRA':''},
    "gdal:warpreproject": {'SOURCE_CRS':None,'RESAMPLING':0,'NODATA':None,'TARGET_RESOLUTION':None,'OPTIONS':'','DATA_TYPE':0,'TARGET_EXTENT':None,'TARGET_EXTENT_CRS':None,'MULTITHREADING':False,'EXTRA':''}
}

def fcnExpScale(val, domainMin, domainMax, rangeMin, rangeMax, exponent):
    if val is None or (domainMin >= domainMax) or (exponent <= 0):
        return None

    if (val >= domainMax):
        return rangeMax
    elif (val <= domainMin):
        return rangeMin

    return ((float(rangeMax) - float(rangeMin)) / math.pow(domainMax - domainMin, exponent)) * math.pow(float(val) - domainMin, exponent) + rangeMin

def run(algo, input, params={}, name="", destCrs=None, feedback=None):
    global DEFAULT_PARAMS
    # print("{} {}".format(algo, name))
    abstract = ""
    try:
        abstract = input.abstract()
    except:
        pass

    if 'grass7:' in algo:
        p = {'input': input}
        if not 'output' in params:
            p['output'] = 'TEMPORARY_OUTPUT'
    elif 'gdal:' in algo:
        p = {'INPUT': input, 'OUTPUT': 'TEMPORARY_OUTPUT'}
    elif 'terrain_shading:' in algo:
        p = {'INPUT': input, 'OUTPUT': 'TEMPORARY_OUTPUT'}
    else:
        p = {'INPUT': input, 'OUTPUT': 'memory:'}

    try:
        p.update(DEFAULT_PARAMS[algo])
    except:
        #log("# Pas de paramètres par défaut pour {}".format(algo))
        pass

    p.update(params)

    r = processing.run(algo, p, feedback=feedback)
    QApplication.processEvents()

    layerName = name if name else algo
    try:
        #print("r ? {}".format(r['OUTPUT']))
        r = r['OUTPUT']
        r.name()
        if name is not None:
            r.setName(layerName)
    except:
        try:
            #print("GRASS ? {}".format(r['output']))
            if 'grass7:v.' in algo:
                r = QgsVectorLayer(r['output'], layerName)
            elif 'grass7:r.' in algo:
                r = QgsRasterLayer(r['output'], layerName)
            else:
                r = QgsVectorLayer(r['output'], layerName)
        except:
            # print("GDAL ? {}".format(r))
            if '.tif' in r:
                r = QgsRasterLayer(r, layerName)
                if not r.crs().isValid() and destCrs is not None:
                    r.setCrs(destCrs)
            elif '.gpkg' in r:
                r = QgsVectorLayer(r, layerName)
                if destCrs is not None:
                    r.setCrs(destCrs)

    try:
        r.setAbstract("{}\n{} {}".format(abstract, algo, params))
    except:
        pass

    return r

"""
    A problem it seems in the 'utils' module of QGis.
    The showPluginHelp function mixes '/' and '', and the Qt Url produced is invalid, under windows.
    This code, while waiting for a QGis API patch.
"""
def showPluginHelp(packageName: str = None, filename: str = "index", section: str = ""):
    try:
        source = ""
        if packageName is None:
            import inspect
            source = inspect.currentframe().f_back.f_code.co_filename
        else:
            import sys
            source = sys.modules[packageName].__file__
    except:
        return
    path = os.path.dirname(source)
    locale = str(QLocale().name())
    helpfile = os.path.join(path, filename + "-" + locale + ".html")
    if not os.path.exists(helpfile):
        helpfile = os.path.join(path, filename + "-" + locale.split("_")[0] + ".html")
    if not os.path.exists(helpfile):
        helpfile = os.path.join(path, filename + "-en.html")
    if not os.path.exists(helpfile):
        helpfile = os.path.join(path, filename + "-en_US.html")
    if not os.path.exists(helpfile):
        helpfile = os.path.join(path, filename + ".html")
    if os.path.exists(helpfile):
        url = "file://" + QDir.fromNativeSeparators(helpfile)
        if section != "":
            url = url + "#" + section
        QDesktopServices.openUrl(QUrl(url, QUrl.TolerantMode))
