from osgeo import osr
import numpy as np
import sys
import netCDF4
import os
import ntpath
import datetime
from netCDF4 import date2num

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.conversion_util import unproject, read_file, get_coordinates, create_nc_file, populate_nc_file


# parse file name
def parse_filename(filename, prefix):
    f_head, f_tail = ntpath.split(filename)
    f_name, ext = os.path.splitext(f_tail)
    if ext != '.asc':
        print('Please select an asc file')
        return False
    items = f_name.replace(prefix, '').split('_')
    year, day = int(items[0]), int(items[1])
    start_date = datetime.datetime(year, 1, 1) + datetime.timedelta(day - 1)
    end_date = datetime.datetime(year, 1, 1) + datetime.timedelta(day)

    return start_date, end_date


# set up data variable based on file name prefix
def data_variablename(prefix):
    unit_pcp, unit_temp = 'mm', 'Celsius degrees'
    var_name, units, long_name = '', '', ''
    if prefix == 'pcp':
        var_name = 'pcp'
        units = unit_pcp
        long_name = 'Precipitation'
    elif prefix == 'max':
        var_name = 'maxtemperature'
        units = unit_temp
        long_name = 'Temperature'
    elif prefix == 'min':
        var_name = 'mintemperature'
        units = unit_temp
        long_name = 'Temperature'
    return var_name, units, long_name


# do the conversion
def convert(prefix, in_source, out_dir, proj_str, out_source_name=None, nc_custom_meta=[]):
    if not parse_filename(in_source, prefix):
        return

    # parse the in source file name
    start_date, end_date = parse_filename(in_source, prefix)
    if not out_source_name:
        out_source = os.path.join(out_dir, prefix + '.nc')
    else:
        out_source = os.path.join(out_dir, out_source_name)

    # read in source file
    x_size, y_size, band1data, geotransform, geoproj, meta = read_file(in_source)
    x_coordinates, y_coordinates = get_coordinates(x_size, y_size, geotransform)


    # get projection info and do the unprojection
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromWkt(proj_str)
    proj4 = spatial_ref.ExportToProj4()
    if not spatial_ref.IsProjected():
        lats = np.repeat(y_coordinates, x_size).reshape(x_size, y_size)
        lons = np.repeat(x_coordinates, y_size).reshape(x_size, y_size).T
    else:
        lats, lons, proj4 = unproject(x_coordinates, y_coordinates, spatial_ref)

    nc_file_exists = os.path.isfile(out_source)

    time_units = 'hours since 1900-01-01 00:00:00'
    time_calendar = 'gregorian'

    if not nc_file_exists:
        out_nc = create_nc_file(out_source, x_size, y_size, x_coordinates, y_coordinates, lats, lons, proj4,
                                spatial_ref, meta, nc_custom_meta, time_units, time_calendar)
    else:
        out_nc = netCDF4.Dataset(out_source, 'r+')

    # data for time variable
    file_date_num = date2num([start_date], units=time_units, calendar=time_calendar)[0]
    if len(out_nc['time'][:]) == 0 or file_date_num != out_nc['time'][-1]:
        out_nc['time'][:] = np.append(out_nc['time'][:], file_date_num)

    data = np.ma.masked_invalid(band1data)
    data.set_fill_value(netCDF4.default_fillvals[band1data.dtype.str[1:]])

    var_name, units, long_name = data_variablename(prefix)

    populate_nc_file(out_nc, data, start_date, end_date, units, band1data, var_name, long_name, proj4)

    out_nc.close()


if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        print('Usage: python asc2netcdf.py <asc_dir> <output_dir> filename_prefix projection_file nc_attribute1_name attr1_value nc_attribute2_name attr2_value ...')
        sys.exit(1)
    
    asc_dir = sys.argv[1]
    out_dir = sys.argv[2]
    prefix = sys.argv[3]
    proj_file = sys.argv[4]
    nc_metadata_attrs = dict(zip(sys.argv[5::2], sys.argv[6::2]))

    with open(proj_file, 'r') as f:
        proj_str = f.read()

    files = filter((lambda f: f[0] is not False), ((parse_filename(f, prefix), f) for f in os.listdir(asc_dir)))

    # process in sorted order so we can subsequently append to the netcdf output file
    for _, f in sorted(files):
        print('Next file: {}'.format(f))
        convert(prefix, os.path.join(asc_dir, f), out_dir, proj_str, nc_custom_meta=nc_metadata_attrs)
