from osgeo import gdal, osr
import numpy as np
import sys
import pyproj
import netCDF4
import os
import ntpath
from datetime import datetime
from netCDF4 import date2num


PROJ_LST = {
    'aea': 'albers_conical_equal_area',
    'aeqd': 'azimuthal_equidistant',
    'laea': 'lambert_azimuthal_equal_area',
    'lcc': 'lambert_conformal_conic',
    'cea': 'lambert_cylindrical_equal_area',
    'merc': 'mercator',
    'ortho': 'orthographic',
    'stere': 'polar_stereographic',
    'tmerc': 'transverse_mercator',
    'Latitude_Longitude': 'latitude_longitude',
    'lonlat': "latitude_longitude",
    'latlon': "latitude_longitude",
    'latlong': "latitude_longitude",
    'longlat': "latitude_longitude)",
    # 'Rotated_Latitude_Longitude': 'rotated_latitude_longitude'
    # vertical_perspective
}

PARAM_LST = {
    '+x_0': 'false_easting',
    '+y_0': 'false_northing',
    '+k_0': 'scale_factor_at_projection_origin',
    '+lat_1': 'standard_parallel![1]',
    '+lat_2': 'standard_parallel![2]',
    '+lon_0': 'longitude_of_projection_origin',
    '+lat_0': 'latitude_of_projection_origin',
    '+units': 'units',
    '+a': 'semi_major_axis',
    '+b': 'semi_minor_axis'
}


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
def unproject(x_coords, y_coords, spatial_ref):
    xv, yv = np.meshgrid(x_coords, y_coords)

    proj4_str = spatial_ref.ExportToProj4()
    inproj = pyproj.Proj(proj4_str, preserve_units=True)
    lons, lats = inproj(xv, yv, inverse=True)
    return lons, lats, proj4_str


def proj4TOdict(proj4_str):
    items = proj4_str.split(' ')
    proj_dict = {}
    for item in items:
        if '=' in item:
            proj_dict[item.split('=')[0]] = item.split('=')[1]
    if '+units' not in proj_dict:
        print('Unit name is missing in the proj.4 string')
        proj_dict['+units'] = 'm'
    if '+proj' not in proj_dict:
        print('Projection name is missing in the proj.4 string')
        proj_dict['+proj'] = 'UNKNOWN'
    return proj_dict, proj_dict['+units']


# translate projection proj.4 dictionary to grid mapping variable
# TODO: might be able to find a written translater
def create_grid_mapping_variable(var_grid_mapping, proj_dict, spatial_reference):
    projection = proj_dict['+proj']
    if projection not in PROJ_LST:
        print(projection + ' is not supported by CF-1.6')
        setattr(var_grid_mapping, 'crs_wkt', str(spatial_reference))
        return
    setattr(var_grid_mapping, 'grid_mapping_name', PROJ_LST[projection])
    for key, value in proj_dict.items():
        try:
            cf_name = PARAM_LST[key]
            setattr(var_grid_mapping, cf_name, value)
        except KeyError:
            pass
    setattr(var_grid_mapping, 'crs_wkt', str(spatial_reference))
    return


# parse file name
def parseFilename(filename):
    fhead, ftail = ntpath.split(filename)
    fname, ext = os.path.splitext(ftail)
    if ext != '.tif':
        print('Please select a GeoTIFF file')
        return False
    items = fname.split('_')
    start_date, start_time = items[5], items[6]
    end_date, end_time = items[7], items[8]
    tail = items[-1]
    if tail not in ['001', '002', '003', '004', '005', '006']:
        print(fname + ' is not valid!', 'Please select a GeoTIFF file named of 001 to 006')
        return False
    return start_date, start_time, end_date, end_time, fname, tail


# set up data variable based on file name tail
def dataVariable(tail, nc_handle, data, dim_y_name, dim_x_name, lat_name, lon_name):
    unit_1, unit_k = '1', 'degree_kelvin'
    var_name_pre_avg = 'LST_LWST_avg_'
    long_name_pre_avg = ' average temperature'
    var_name_pre_num = 'N_obs_avg_'
    long_name_pre_num = 'number of observations used to calculate '
    var_name, units, long_name = '', '', ''
    missing_value_num = 0
    if tail == '001':
        var_name = var_name_pre_avg + 'daily'
        units = unit_k
        long_name = 'daily' + long_name_pre_avg
    elif tail == '002':
        var_name = var_name_pre_num + 'daily'
        units = unit_1
        long_name = long_name_pre_num + 'daily' + long_name_pre_avg
    elif tail == '003':
        var_name = var_name_pre_avg + 'day'
        units = unit_k
        long_name = 'day' + long_name_pre_avg
    elif tail == '004':
        var_name = var_name_pre_num + 'day'
        units = unit_1
        long_name = long_name_pre_num + 'day' + long_name_pre_avg
    elif tail == '005':
        var_name = var_name_pre_avg + 'night'
        units = unit_k
        long_name = 'night' + long_name_pre_avg
    elif tail == '006':
        var_name = var_name_pre_num + 'night'
        units = unit_1
        long_name = long_name_pre_num + 'night' + long_name_pre_avg

    var = nc_handle.createVariable(var_name, 'f4', ('time', dim_y_name, dim_x_name,))
    # assign the masked array to data variable
    var[:] = [np.ma.masked_invalid(data)]

    setattr(var, 'units', units)
    setattr(var, 'long_name', long_name)
    setattr(var, 'coordinates', lat_name + ' ' + lon_name)
    return var


# do the conversion
def convert(in_source, out_dir, out_source_name=None, dim_x_name='x', dim_y_name='y', lat_name='lat', lon_name='lon'):
    if not parseFilename(in_source):
        return

    # parse the in source file name
    start_date, start_time, end_date, end_time, fname, tail = parseFilename(in_source)
    if not out_source_name:
        out_source = os.path.join(out_dir, fname + '.nc')
    else:
        out_source = os.path.join(out_dir, out_source_name)

    # read in source file
    xsize, ysize, band1data, geotransform, geoproj, meta = readFile(in_source)
    xcoordinates, ycoordinates = getCoordinates(xsize, ysize, geotransform)

    # create netCDF file
    out_nc = netCDF4.Dataset(out_source, 'w')
    # define dimensions
    dim_x = out_nc.createDimension(dim_x_name, xsize)
    dim_y = out_nc.createDimension(dim_y_name, ysize)
    dim_time = out_nc.createDimension('time', None)

    # get projection info and do the unprojection
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromWkt(geoproj)
    lons, lats, proj4 = unproject(xcoordinates, ycoordinates, spatial_ref)

    proj_info_dict, proj_units = proj4TOdict(proj4)
    # create variables
    # original coordinate variables
    proj_x = out_nc.createVariable('x', 'i4', (dim_x_name, ))
    proj_x.units = proj_units
    proj_x.standard_name = 'projection_x_coordinate'
    proj_x.long_name = 'x coordinate of projection'
    proj_x[:] = xcoordinates

    proj_y = out_nc.createVariable('y', 'i4', (dim_y_name, ))
    proj_y.units = proj_units
    proj_y.standard_name = 'projection_y_coordinate'
    proj_y.long_name = 'y coordinate of projection'
    proj_y[:] = ycoordinates

    # auxiliary coordinate variables lat and lon
    lat = out_nc.createVariable(lat_name, 'f4', (dim_y_name, dim_x_name, ))
    lat.units = 'degrees_north'
    lat.standard_name = 'latitude'
    lat.long_name = 'latitude coordinate'
    lat[:] = lats[:]

    lon = out_nc.createVariable(lon_name, 'f4', (dim_y_name, dim_x_name, ))
    lon.units = 'degrees_east'
    lon.standard_name = 'longitude'
    lon.long_name = 'longitude coordinate'
    lon[:] = lons[:]

    # time variable
    var_time = out_nc.createVariable('time', 'i4', ('time', ))
    var_time.units = 'hours since 1990-01-01 00:00:00'
    var_time.calendar = 'gregorian'
    var_time.standard_name = 'time'
    var_time.axis = 'T'

    # data for time variable
    file_date = datetime.strptime(' '.join([start_date, start_time]), '%Y.%m.%d %H.%M.%S')
    var_time[:] = date2num([file_date], units=var_time.units, calendar=var_time.calendar)

    # grid mapping variable
    grid_map_name = PROJ_LST[proj_info_dict['+proj']]
    grid_map = out_nc.createVariable(grid_map_name, 'c', )
    create_grid_mapping_variable(grid_map, proj_info_dict, spatial_ref)

    # create data variable
    var_data = dataVariable(tail, out_nc, band1data, dim_y_name, dim_x_name, lat_name, lon_name)
    var_data.grid_mapping = grid_map_name
    # temporal resolution attribute for the data variable
    file_end_datetime = datetime.strptime(' '.join([end_date, end_time]), '%Y.%m.%d %H.%M.%S')
    temp_res = ''
    delta = (file_end_datetime - file_date).days
    if delta == 1:
        temp_res = 'daily'
    elif delta == 7:
        temp_res = 'weekly'
    else:
        temp_res = 'monthly'
    setattr(var_data, 'temporal_resolution', temp_res)


    out_nc.Conventions = 'CF-1.6'
    out_nc.institution = 'University of Waterloo'
    for key, value in meta.items():
        key_name = key.split('_')[1]
        if not key_name in ['DATETIME', 'DOCUMENTNAME']:
            setattr(out_nc, key, value)

    out_nc.close()


if __name__ == '__main__':
    for f in os.listdir('../data'):
        convert(os.path.join('../data', f), out_dir='../converted_data')