import math
import processing
from qgis.core import QgsRasterLayer, QgsVectorLayer, QgsMessageLog
from qgis.PyQt.QtWidgets import QApplication
import os
from qgis.PyQt.QtCore import QLocale, QUrl, QDir
from qgis.PyQt.QtGui import QDesktopServices

DEFAULT_PARAMS = {
    "native:lineintersections": {
        "INPUT_FIELDS": [],
        "INTERSECT_FIELDS": [],
        "INTERSECT_FIELDS_PREFIX": "",
    },
    "native:extractbyexpression": {"EXPRESSION": ' "DN" = 0'},
    "native:geometrybyexpression": {
        "OUTPUT_GEOMETRY": 1,
        "WITH_Z": False,
        "WITH_M": True,
        "EXPRESSION": "$geometry",
    },
    "native:multiparttosingleparts": {},
    "native:setmfromraster": {"BAND": 1, "SCALE": 1},
}

def run(algo, input, params={}, name="", destCrs=None, feedback=None):
    global DEFAULT_PARAMS
    # print("{} {}".format(algo, name))
    abstract = ""
    try:
        abstract = input.serverProperties().abstract()
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
        pass

    p.update(params)

    r = processing.run(algo, p, feedback=feedback)
    QApplication.processEvents()

    layerName = name if name else algo
    try:
        r = r['OUTPUT']
        r.name()
        if name is not None:
            r.setName(layerName)
    except:
        try:
            if 'grass7:v.' in algo:
                r = QgsVectorLayer(r['output'], layerName)
            elif 'grass7:r.' in algo:
                r = QgsRasterLayer(r['output'], layerName)
            else:
                r = QgsVectorLayer(r['output'], layerName)
        except:
            if '.tif' in r:
                r = QgsRasterLayer(r, layerName)
                if not r.crs().isValid() and destCrs is not None:
                    r.setCrs(destCrs)
            elif '.gpkg' in r:
                r = QgsVectorLayer(r, layerName)
                if destCrs is not None:
                    r.setCrs(destCrs)

    try:
        r.serverProperties().setAbstract("{}\n{} {}".format(abstract, algo, params))
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
        url = QDir.fromNativeSeparators(helpfile)

        if section != "":
            url = url + "#" + section

        if not QDesktopServices.openUrl(
            QUrl("file:///" + url, QUrl.ParsingMode.TolerantMode)
        ):
            QDesktopServices.openUrl(
                QUrl("file://" + url, QUrl.ParsingMode.TolerantMode)
            )
    else:
        QgsMessageLog.logMessage(str(f"{helpfile} not found"), "Extensions")
