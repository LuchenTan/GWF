from osgeo import gdal, osr
import numpy as np
import sys
import pyproj
from .CFGridMapping import *
import netCDF4

# read GeoTiff file
def readFile(filename):
    ds = gdal.Open(filename)
    if ds is None:
        print('Could not open ' + filename)
        sys.exit(1)

    band_cnt = ds.RasterCount
    if band_cnt > 1:
        pass  # TODO: do something else
    band1 = ds.GetRasterBand(1)
    geotransform = ds.GetGeoTransform()
    geoproj = ds.GetProjection()
    meta = ds.GetMetadata()
    band1data = band1.ReadAsArray()
    xsize = ds.RasterXSize
    ysize = ds.RasterYSize
    return xsize, ysize, band1data, geotransform, geoproj, meta


# get coordinate values
def getCoordinates(xsize, ysize, geotransform):
    x_topleft, x_res, dx_rotation, y_topleft, dy_rotation, y_res = geotransform
    xcoordinates = np.arange(start=x_topleft, stop=x_topleft + x_res * xsize, step=x_res)
    ycoordinates = np.arange(start=y_topleft, stop=y_topleft + y_res * ysize, step=y_res)
    return xcoordinates, ycoordinates


# unprojec to lat/lon
def unproject(x_coords, y_coords, geoproj):
    xv, yv = np.meshgrid(x_coords, y_coords)

    proj4_str = geoproj.ExportToProj4()
    inproj = pyproj.Proj(proj4_str, preserve_units=True)
    lons, lats = inproj(xv, yv, inverse=True)
    return lons, lats, proj4_str


def proj4TOdict(proj4_str):
    items = proj4_str.split(' ')
    proj_dict = {}
    for item in items:
        if '=' in item:
            proj_dict[item.split('=')[0]] = item.split('=')[1]
    return proj_dict


# translate projection proj.4 dictionary to grid mapping variable
# TODO: might be able to find a written translater
def create_grid_mapping_variable(var_grid_mapping, proj_dict):

    projection = spatial_reference.GetAttrValue('PROJECTION')
    if projection:
        try:
            cf_grid_mapping_name = PROJ_LST[projection]
        except KeyError:
            print(projection + ' is not supported by CF-1.6')
            return
        setattr(var_grid_mapping, 'grid_mapping_name', cf_grid_mapping_name)
    else:
        return
    for key in PARAM_LST.keys():
        try:
            value = spatial_reference.GetProjParm(key)
            setattr(var_grid_mapping, PARAM_LST[key], value)
        except KeyError:
            pass
    inv_flatten = spatial_reference.GetInvFlattening()
    if inv_flatten != 0.0:
        setattr(var_grid_mapping, 'inverse_flattening', inv_flatten)
    setattr(var_grid_mapping, 'semi_major_axis', spatial_reference.GetSemiMajor())
    setattr(var_grid_mapping, 'semi_minor_axis', spatial_reference.GetSemiMinor())
    setattr(var_grid_mapping, 'unit', spatial_reference.GetLinearUnitsName())
    setattr(var_grid_mapping, 'crs_wkt', str(spatial_reference))


# do the conversion
def convert(in_source, out_source):
    xsize, ysize, band1data, geotransform, geoproj, meta = readFile(in_source)
    xcoordinates, ycoordinates = getCoordinates(xsize, ysize, geotransform)

    out_nc = netCDF4.Dataset(out_source, 'w')
    dim_x = out_nc.createDimension('x', xsize)
    dim_y = out_nc.createDimension('y', ysize)
    dim_time = out_nc.createDimension('time', None)

    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromWkt(geoproj)
    lons, lats, proj4 = unproject(xcoordinates, ycoordinates, geoproj)

    if geoproj.IsProjected():

        create_grid_mapping_variable(var_grid, spatial_ref)


proj_x = out_nc.createVariable('x', 'i4', ('x', ))