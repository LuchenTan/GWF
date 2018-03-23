from osgeo import gdal
import numpy as np
import netCDF4
from datetime import datetime
from netCDF4 import date2num
import pyproj
import os

source_path = 'UW_NA_LST_7.1.1_001_2008.10.1_0.0.0_2008.10.31_23.59.59_NA_001.tif'
output_path = '2008.10.1_0.0.0_2008.10.31_23.59.59_NA_001.nc'
tmp_nc_path = 'tmp.nc'

# open source Geotiff file
source_dataset = gdal.Open(source_path)

# Construct the grid
meta = source_dataset.GetMetadata()
x0, xinc, _, y0, _, yinc = source_dataset.GetGeoTransform()
nx, ny = (source_dataset.RasterXSize, source_dataset.RasterYSize)
x = np.linspace(x0, x0 + xinc*nx, nx)
y = np.linspace(y0, y0 + yinc*ny, ny)
xv, yv = np.meshgrid(x, y)

# Reproject the coordinates out of lamaz into lat/lon.
lamaz = pyproj.Proj("+proj=laea +lat_0=90 +lon_0=0 k=1 +x_0=0 +y_0= 0 +units=m +a=6371228.0 +b=6371228.0")
wgs84 = pyproj.Proj("+init=EPSG:4326")
lon, lat = pyproj.transform(lamaz, wgs84, xv, yv)

# convert to a temp NetCDf file
gdal.Translate(tmp_nc_path, source_dataset, format='NetCDF')

# Modify converted temp NetCDF
converted_dataset = netCDF4.Dataset(tmp_nc_path, 'r+')

# Add time dimension and time variable
converted_dataset.createDimension('time', None)
times = converted_dataset.createVariable('time', 'i4', ('time', ))
times.units = 'hours since 1990-01-01 00:00:00'
times.calendar = 'gregorian'
times.long_name = 'time'
times.axis = 'T'

# Add value to time variable
times[:] = date2num([datetime(2008, 10, 1)], units=times.units, calendar=times.calendar)

# Add lat/lon variables
var_lat = converted_dataset.createVariable('lat', 'f4', ('y', 'x'))
var_lat.units = 'degree'
var_lat.long_name = 'Latitude. -90 to 90 degree'
var_lat[:] = lat[:]

var_lon = converted_dataset.createVariable('lon', 'f4', ('y', 'x'))
var_lon.units = 'degree'
var_lon.long_name = 'Longitude. -180 to 180 degree'
var_lon[:] = lon[:]

# Get Band1 variable
band1 = converted_dataset.variables['Band1']
#
#  Create new variable with time dimension
lst = converted_dataset.createVariable('LST_LWST_avg_daily', band1.datatype, ('time', 'y', 'x'))
# Copy attributes from Band1
lst.setncatts({k: band1.getncattr(k) for k in band1.ncattrs()})
lst.units = 'degree Kelvin'
lst.long_name = 'average daily temperature'
np.warnings.filterwarnings('ignore')
lst[:] = [band1[:]]

# # Check the grid mapping variable
# grid_mapping = converted_dataset.variables['lambert_azimuthal_equal_area']
# print(grid_mapping)

converted_dataset.close()


# To delete Band1, copy everything from the the temp NetCDF file to the final NetCDF file
with netCDF4.Dataset(tmp_nc_path) as src, netCDF4.Dataset(output_path, "w") as dst:
    # copy attributes
    for name in src.ncattrs():
        dst.setncattr(name, src.getncattr(name))

    # copy dimensions
    for name, dimension in src.dimensions.items():
        dst.createDimension(name, (len(dimension) if not dimension.isunlimited() else None))

    # copy all file data except for Band1
    for name, variable in src.variables.items():
        if name != 'Band1':
            x = dst.createVariable(name, variable.datatype, variable.dimensions)
            x.setncatts({k: variable.getncattr(k) for k in variable.ncattrs()})
            dst.variables[name][:] = src.variables[name][:]

# delete temp NetCDF file
os.remove(tmp_nc_path)