from osgeo import gdal
from osgeo import ogr
from osgeo import osr

# Avoid the regressing from https://github.com/conda-forge/gdal-feedstock/pull/129
# See https://github.com/conda-forge/gdal-feedstock/issues/131
from osgeo.gdal_array import *

drivers = ['netCDF', 'HDF4', 'HDF5', 'GTiff', 'PNG', 'JPEG', 'GPKG', 'KEA', 'JP2OpenJPEG', 'WCS']
for driver in drivers:
    print(driver)
    assert gdal.GetDriverByName(driver)

drivers = ['GML', 'XLS', 'KML', 'SQLite', 'PostgreSQL']
for driver in drivers:
    print(driver)
    assert ogr.GetDriverByName(driver)

def has_geos():
    pnt1 = ogr.CreateGeometryFromWkt( 'POINT(10 20)' )
    pnt2 = ogr.CreateGeometryFromWkt( 'POINT(30 20)' )
    ogrex = ogr.GetUseExceptions()
    ogr.DontUseExceptions()
    hasgeos = pnt1.Union(pnt2) is not None
    if ogrex:
        ogr.UseExceptions()
    return hasgeos

assert has_geos(), 'GEOS not available within GDAL'

def has_proj():
    sr1 = osr.SpatialReference()
    sr1.ImportFromEPSG(4326) # lat, lon.
    sr2 = osr.SpatialReference()
    sr2.ImportFromEPSG(28355) # GDA94/MGA zone 55.
    osrex = osr.GetUseExceptions()
    osr.UseExceptions()
    hasproj = True
    # Use exceptions to determine if we have proj and epsg files
    # otherwise we can't reliably determine if it has failed.
    try:
        trans = osr.CoordinateTransformation(sr1, sr2)
    except RuntimeError:
        hasproj = False
    return hasproj

assert has_proj(), 'PROJ not available within GDAL'

# Test https://github.com/swig/swig/issues/567
def make_geom():
    geom = ogr.Geometry(ogr.wkbPoint)
    geom.AddPoint_2D(0, 0)
    return geom

def gen_list(N):
    for i in range(N):
        geom = make_geom()
        yield i

N = 10
assert list(gen_list(N)) == list(range(N))

# This module does some additional tests.
import extra_tests
