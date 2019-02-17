from osgeo import osr
import numpy as np
import sys
import netCDF4
import os
import ntpath
from datetime import datetime
from netCDF4 import date2num

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.conversion_util import get_coordinates, read_file, unproject, create_nc_file, populate_nc_file


# parse file name
def parse_filename(filename):
    f_head, f_tail = ntpath.split(filename)
    f_name, ext = os.path.splitext(f_tail)
    if ext != '.tif':
        print('Please select a GeoTIFF file')
        return False
    items = f_name.split('_')
    start_date, start_time = items[5], items[6]
    end_date, end_time = items[7], items[8]
    tail = items[-1]
    if tail not in ['001', '002', '003', '004', '005', '006']:
        print(f_name + ' is not valid!', 'Please select a GeoTIFF file named of 001 to 006')
        return False
    basename = items[0:5]
    return start_date, start_time, end_date, end_time, f_name, basename, tail


# set up data variable based on file name tail
def data_variablename(tail):
    unit_1, unit_k = '1', 'degree_kelvin'
    var_name_pre_avg = 'LST_LWST_avg_'
    long_name_pre_avg = ' average temperature'
    var_name_pre_num = 'N_obs_avg_'
    long_name_pre_num = 'number of observations used to calculate '
    var_name, units, long_name = '', '', ''
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
    return var_name, units, long_name


# do the conversion
def convert(in_source, out_dir, out_source_name=None, nc_custom_meta=[]):
    if not parse_filename(in_source):
        return

    # parse the in source file name
    start_date, start_time, end_date, end_time, fname, basename, tail = parse_filename(in_source)
    if not out_source_name:
        out_source = os.path.join(out_dir, '_'.join(basename) + '.nc')
    else:
        out_source = os.path.join(out_dir, out_source_name)

    # read in source file
    x_size, y_size, band1data, geotransform, geoproj, meta = read_file(in_source)
    x_coordinates, y_coordinates = get_coordinates(x_size, y_size, geotransform)

    # get projection info and do the unprojection
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromWkt(geoproj)
    lons, lats, proj4 = unproject(x_coordinates, y_coordinates, spatial_ref)

    nc_file_exists = os.path.isfile(out_source)

    time_units = 'hours since 1990-01-01 00:00:00'
    time_calendar = 'gregorian'

    if not nc_file_exists:
        out_nc = create_nc_file(out_source, x_size, y_size, x_coordinates, y_coordinates, lats, lons, proj4,
                                spatial_ref, meta, nc_custom_meta, time_units, time_calendar)
    else:
        out_nc = netCDF4.Dataset(out_source, 'r+')

    # data for time variable
    file_date = datetime.strptime(' '.join([start_date, start_time]), '%Y.%m.%d %H.%M.%S')
    file_date_num = date2num([file_date], units=time_units, calendar=time_calendar)[0]
    if len(out_nc['time'][:]) == 0 or file_date_num != out_nc['time'][-1]:
        out_nc['time'][:] = np.append(out_nc['time'][:], file_date_num)

    data = np.ma.masked_invalid(band1data)
    data.set_fill_value(netCDF4.default_fillvals[band1data.dtype.str[1:]])

    var_name, units, long_name = data_variablename(tail)
    file_end_datetime = datetime.strptime(' '.join([end_date, end_time]), '%Y.%m.%d %H.%M.%S')

    populate_nc_file(out_nc, data, file_date, file_end_datetime, units, band1data, var_name, long_name, proj4)

    out_nc.close()


if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        print('Usage: python geotiff2netcdf.py <geotiff_dir> <output_dir> nc_attribute1_name attr1_value nc_attribute2_name attr2_value ...')
        sys.exit(1)
    
    geotiff_dir = sys.argv[1]
    out_dir = sys.argv[2]
    nc_metadata_attrs = dict(zip(sys.argv[3::2], sys.argv[4::2]))

    files = filter((lambda f: f[0] is not False), ((parse_filename(f), f) for f in os.listdir(geotiff_dir)))
    files = list((datetime.strptime(f[0][0] + f[0][1], '%Y.%m.%d%H.%M.%S'), f[1]) for f in files)

    # process in sorted order so we can subsequently append to the netcdf output file
    for _, f in sorted(files):
        print('Next file: {}'.format(f))
        convert(os.path.join(geotiff_dir, f), out_dir=out_dir, nc_custom_meta=nc_metadata_attrs)
