from osgeo import gdal
import numpy as np
import sys
import pyproj
import netCDF4

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
    'longlat': "latitude_longitude",
    # 'Rotated_Latitude_Longitude': 'rotated_latitude_longitude'
    # vertical_perspective
}

PARAM_LST = {
    '+x_0': 'false_easting',
    '+y_0': 'false_northing',
    '+k_0': {'lcc': 'scale_factor',
             'merc': 'scale_factor_at_projection_origin',
             'stere': 'scale_factor_at_projection_origin',
             'tmerc': 'scale_factor_at_central_meridian',
             'default': 'scale_factor'
             },
    '+lat_1': {'aea': 'standard_parallel[1]',
               'lcc': 'standard_parallel',
               'default': 'standard_parallel[1]'
               },
    '+lat_2': {'aea': 'standard_parallel[2]',
               'lcc': 'standard_parallel[2]',
               'default': 'standard_parallel[2]'
               },
    '+lon_0': {'aea': 'longitude_of_central_meridian',
               'aeqd': 'longitude_of_projection_origin',
               'laea': 'longitude_of_projection_origin',
               'lcc': 'longitude_of_central_meridian',
               'cea': 'longitude_of_central_meridian',
               'merc': 'longitude_of_projection_origin',
               'ortho': 'longitude_of_projection_origin',
               'stere': 'straight_vertical_longitude_from_pole',
               'tmerc': 'longitude_of_central_meridian',
               'default': 'longitude_of_projection_origin'
               },
    '+lat_0': 'latitude_of_projection_origin',
    '+lat_ts': {'cea': 'standard_parallel[1]',
                'merc': 'standard_parallel[1]',
                'stere': 'standard_parallel',
                'default': 'standard_parallel'},
    '+units': 'units',
    '+a': 'semi_major_axis',
    '+b': 'semi_minor_axis'
}


# read asc file
def read_file(filename):
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
    # bandtype = gdal.GetDataTypeName(band1.DataType)
    band1data = band1.ReadAsArray()
    masked_band1 = np.ma.masked_where(band1data == band1.GetNoDataValue(), band1data)
    masked_band1.set_fill_value(band1.GetNoDataValue())
    x_size = ds.RasterXSize
    y_size = ds.RasterYSize
    return x_size, y_size, masked_band1, geotransform, geoproj, meta


# get coordinate values
def get_coordinates(x_size, y_size, geotransform):
    x_topleft, x_res, dx_rotation, y_topleft, dy_rotation, y_res = geotransform
    if dx_rotation == 0 and dy_rotation == 0:
        x_coordinates = np.arange(start=x_topleft, stop=x_topleft + x_res * x_size, step=x_res,
                                 dtype=np.float32)[:x_size]
        y_coordinates = np.arange(start=y_topleft, stop=y_topleft + y_res * y_size, step=y_res,
                                 dtype=np.float32)[:y_size]
        return x_coordinates, y_coordinates
    else:
        ## TODO: need rotation
        print("x and y coordinates need rotation!")
        sys.exit(1)


# unproject to lat/lon
def unproject(x_coords, y_coords, spatial_ref):
    xv, yv = np.meshgrid(x_coords, y_coords)

    proj4_str = spatial_ref.ExportToProj4()
    inproj = pyproj.Proj(proj4_str, preserve_units=True)
    lons, lats = inproj(xv, yv, inverse=True)
    return lons, lats, proj4_str


def proj4_to_dict(proj4_str):
    items = proj4_str.split(' ')
    proj_dict = {}
    for item in items:
        if '=' in item:
            proj_dict[item.split('=')[0]] = item.split('=')[1]
    if '+units' not in proj_dict:
        print('Unit name is missing in the proj.4 string')
        proj_dict['+units'] = 'UNKNOWN'
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
            if isinstance(cf_name, dict):
                try:
                    setattr(var_grid_mapping, cf_name[projection], value)
                except KeyError:
                    setattr(var_grid_mapping, cf_name['default'], value)
            else:
                setattr(var_grid_mapping, cf_name, value)
        except KeyError:
            pass
    setattr(var_grid_mapping, 'crs_wkt', str(spatial_reference))
    return


def create_nc_file(out_source, x_size, y_size, x_coordinates, y_coordinates, lats, lons, proj4, spatial_ref,
                   meta, nc_custom_meta, time_units, time_calendar, lat_name='lat', lon_name='lon',
                   dim_x_name='rlon', dim_y_name='rlat'):
    out_nc = netCDF4.Dataset(out_source, 'w')

    # define dimensions
    dim_x = out_nc.createDimension(dim_x_name, x_size)
    dim_y = out_nc.createDimension(dim_y_name, y_size)
    dim_time = out_nc.createDimension('time', None)

    proj_info_dict, proj_units = proj4_to_dict(proj4)

    # create variables
    # original coordinate variables
    proj_x = out_nc.createVariable(dim_x_name, x_coordinates.dtype, (dim_x_name,))
    proj_x.units = proj_units
    proj_x.standard_name = 'projection_x_coordinate'
    proj_x.long_name = 'x coordinate of projection'
    proj_x[:] = x_coordinates

    proj_y = out_nc.createVariable(dim_y_name, y_coordinates.dtype, (dim_y_name,))
    proj_y.units = proj_units
    proj_y.standard_name = 'projection_y_coordinate'
    proj_y.long_name = 'y coordinate of projection'
    proj_y[:] = y_coordinates

    # auxiliary coordinate variables lat and lon
    lat = out_nc.createVariable(lat_name, 'f4', (dim_y_name, dim_x_name,))
    lat.units = 'degrees_north'
    lat.standard_name = 'latitude'
    lat.long_name = 'latitude coordinate'
    lat[:] = lats[:]

    lon = out_nc.createVariable(lon_name, 'f4', (dim_y_name, dim_x_name,))
    lon.units = 'degrees_east'
    lon.standard_name = 'longitude'
    lon.long_name = 'longitude coordinate'
    lon[:] = lons[:]

    # time variable
    var_time = out_nc.createVariable('time', 'i4', ('time',))
    var_time.units = time_units
    var_time.calendar = time_calendar
    var_time.standard_name = 'time'
    var_time.axis = 'T'

    # grid mapping variable
    grid_map_name = PROJ_LST[proj_info_dict['+proj']]
    grid_map = out_nc.createVariable(grid_map_name, 'c', )
    create_grid_mapping_variable(grid_map, proj_info_dict, spatial_ref)

    out_nc.Conventions = 'CF-1.6'
    out_nc.institution = 'University of Waterloo'
    for key, value in meta.items():
        key_name = key.split('_')[1]
        if key_name not in ['DATETIME', 'DOCUMENTNAME']:
            setattr(out_nc, key, value)

    # set additional nc attributes as specified by user
    for key, value in nc_custom_meta.items():
        setattr(out_nc, key, value)

    return out_nc


def populate_nc_file(out_nc, data, start_date, end_date, units, band1data, var_name, long_name, proj4,
                     lat_name='lat', lon_name='lon', dim_x_name='rlon', dim_y_name='rlat'):
    if var_name not in out_nc.variables.keys():
        # create data variable
        var_data = out_nc.createVariable(var_name, band1data.dtype,
                                         ('time', dim_y_name, dim_x_name,),
                                         fill_value=band1data.get_fill_value())

        # assign the masked array to data variable
        var_data[:] = [data]

        var_data.units = units
        var_data.long_name = long_name
        var_data.coordinates = lat_name + ' ' + lon_name

        proj_info_dict, proj_units = proj4_to_dict(proj4)
        var_data.grid_mapping = PROJ_LST[proj_info_dict['+proj']]

        # temporal resolution attribute for the data variable
        delta = (end_date - start_date).days
        if delta == 1:
            temp_res = 'daily'
        elif delta == 7:
            temp_res = 'weekly'
        elif delta == 14:
            temp_res = 'biweekly'
        elif 28 <= delta <= 31:
            temp_res = 'monthly'
        else:
            temp_res = 'UNKNOWN'
        setattr(var_data, 'temporal_resolution', temp_res)
    else:
        out_nc[var_name][-1] = data
