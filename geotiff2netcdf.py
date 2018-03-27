from osgeo import gdal, osr
import numpy as np
import netCDF4
from datetime import datetime
from netCDF4 import date2num
import pyproj


source_path = 'UW_NA_LST_7.1.1_001_2008.10.1_0.0.0_2008.10.31_23.59.59_NA_001.tif'
output_path = '2008.10.1_0.0.0_2008.10.31_23.59.59_NA_001.nc'
date = datetime(2008, 10, 1)

# open source Geotiff file
source_dataset = gdal.Open(source_path)

# Construct the grid
meta = source_dataset.GetMetadata()
x0, xinc, _, y0, _, yinc = source_dataset.GetGeoTransform()
nx, ny = (source_dataset.RasterXSize, source_dataset.RasterYSize)
x = np.linspace(x0, x0 + xinc * nx, nx)
y = np.linspace(y0, y0 + yinc * ny, ny)
xv, yv = np.meshgrid(x, y)

data = source_dataset.ReadAsArray()

# get projection wkt
prj = source_dataset.GetProjection()
# get proj4 of the projected system
sr = osr.SpatialReference(wkt=prj)
#sr.ImportFromWkt(prj)
proj4 = sr.ExportToProj4()

# Convert to lat/lon
inproj = pyproj.Proj(proj4)
lons, lats = inproj(xv, yv, inverse=True)

with netCDF4.Dataset(output_path, 'w') as outnc:
    # create dimensions
    outnc.createDimension('nlon', nx)
    outnc.createDimension('nlat', ny)
    outnc.createDimension('time', None)

    var_x = outnc.createVariable('nlon', 'f4', ('nlon',))
    var_x.long_name = 'longitude in laea'
    var_x.units = 'm'
    var_x.standard_name = 'grid_longitude'
    var_x.axis = 'X'
    var_x[:] = x[:]

    var_y = outnc.createVariable('nlat', 'f4', ('nlat',))
    var_y.long_name = 'latitude in laea'
    var_y.units = 'm'
    var_y.standard_name = 'grid_latitude'
    var_y.axis = 'Y'
    var_y[:] = y[:]

    # create variables
    var_time = outnc.createVariable('time', 'i4', ('time',))
    var_time.long_name = 'time'
    var_time.units = 'hours since 1990-01-01 00:00:00'
    var_time.calendar = 'gregorian'
    var_time.standard_name = 'time'
    var_time.axis = 'T'

    # Add value to time variable
    var_time[:] = date2num([date],
                           units=var_time.units,
                           calendar=var_time.calendar)

    var_lat = outnc.createVariable('lat', 'f4', ('nlat', 'nlon'))
    var_lat.long_name = 'latitude'
    var_lat.units = 'degrees_north'
    var_lat.standard_name = 'latitude'
    var_lat[:] = lats[:]

    var_lon = outnc.createVariable('lon', 'f4', ('nlat', 'nlon'))
    var_lon.long_name = 'longitude'
    var_lon.units = 'degrees_east'
    var_lon.standard_name = 'longitude'
    var_lon[:] = lons[:]

    var_lst = outnc.createVariable('LST_LWST_avg_daily', 'f4', ('time', 'nlat', 'nlon'))
    var_lst.units = 'degree_kelvin'
    var_lst.long_name = 'average daily temperature'
    var_lst.coordinates = "lon lat"
    var_lst[:] = [data[:]]



