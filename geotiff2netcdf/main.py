from os.path import dirname, abspath
from glob import glob
from osgeo import gdal
from utils import *

import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
from datetime import datetime, timedelta
from netCDF4 import num2date, date2num, date2index


par_dir = dirname(dirname(abspath(__file__)))
dir_name_sst = '/media/mwilson/My Passport/GWF/MODIS_1km_LST/Daily/'
days_list = sorted(glob(dir_name_sst+'*_NA_001.tif'))

days_list = ['UW_NA_LST_7.1.1_001_2008.10.1_0.0.0_2008.10.31_23.59.59_NA_001.tif']
date = datetime(2008, 10, 1)

latcorners = [ 39.861, 49.284]
loncorners = [-94.004,-71.671]

nx = 1178
ny = 1771

x_tif = np.arange(0,nx*1*1000, 1000) #(latitude)
y_tif = np.arange(0,-ny*1*1000, -1000) #(longitude)

map = create_map(loncorners, latcorners, 'i', 'laea', lat_0=90, lon_0=0)

x_tif,y_tif = np.meshgrid(x_tif,y_tif)
lon,lat = map(x_tif,y_tif,inverse=True)

def create_netcdf(file_name,nx,ny,lat,lon,content):
    outgrp = nc.Dataset(file_name,'w',format='NETCDF4')
    
    description =  'Driver: {}/{}\n Size is: {}, {}\n Bands = {}\n Coordinate System is:{}\n \n GetGeoTransform() = {}\n \n GetMetadata() = {}'.format(im.GetDriver().ShortName, im.GetDriver().LongName,im.RasterXSize, im.RasterYSize,im.RasterCount, im.GetProjectionRef (), im.GetGeoTransform (), im.GetMetadata ())
    
    outgrp.description = description
    
    dim_nx = outgrp.createDimension('nx', nx)
    dim_ny = outgrp.createDimension('ny', ny)
    dim_time = outgrp.createDimension('time', 1)
    
    var_time = outgrp.createVariable('time', 'i4', ('time'))
    var_time.long_name = 'Time attribute'
    var_time.units = "hours since 1990-01-01 00:00:00.0"
    var_time.calendar = "gregorian"
    var_time.axis = "T"

    var_lat = outgrp.createVariable('lat', 'f4', ('ny','nx'))
    var_lat.units = "degree" 
    var_lat.long_name = 'Latitude. -90 to 90 deg.'
    
    var_lon = outgrp.createVariable('lon', 'f4', ('ny','nx'))
    var_lon.units = "degree"
    var_lon.long_name = 'Longitude. -180 to 180 deg.'
    
    var_content = outgrp.createVariable('LST_LWST_avg_daily', 'f4', ('time','ny','nx'))
    var_content.units = 'degree Kelvin'
    var_content.long_name = 'Average daily temperature'
    
    var_lon[:,:] = lon[:,:]
    var_lat[:,:] = lat[:,:]
    var_content[:,:,:] = content[:,:,:]
    var_time[:] = date2num([date],units=var_time.units,calendar=var_time.calendar)
    outgrp.close()


for day in days_list:
    im = gdal.Open(day) # reads in tiff file
    content = im.ReadAsArray()
    gt = im.GetGeoTransform()
    
    
    if gt[3] < 400000:  # the latter half of the files cover a bigger extent of land, so the content needs to be cropped.
        pass
    else:
        content = content[94:ny+94,0:nx]  #cropping
    
    d3_array = np.zeros([1,ny,nx])
    d3_array[0,:,:] = content[:,:]
    
    create_netcdf('thing.nc',nx,ny,lat,lon,d3_array)
    break

