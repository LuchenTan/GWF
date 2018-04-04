# NetCDF
## 1. What is NetCDF?
The Network Comman Data Form, or [NetCDF](https://www.unidata.ucar.edu/software/netcdf/docs/) is **a set of software libraries** 
and self-describing, machine-independant **data formats**. It supports the creation, access and sharing of scientific data. 

To make data "self-describing" and meaningful to both humans and machines, the names, units of measure and other metadata should be meaningful and conform to **Conventions**. 

## 2. How to install NetCDF?
To install NetCDF is to install the base NetCDF libraries and associated tools. Setting up NetCDF on Ubuntu follows [here](https://skygiant.com.au/setting-up-netcdf-on-ubuntu/).

```
sudo apt-get install libnetcdf-dev netcdf-bin
sudo apt-get install ncview
```
To install Python's netCDF4 lib:
```
pip install netCDF4
```
## 3. How to open a NetCDF file?
NetCDF files should have the file name extension "**.nc**". A classic netCDF format file should not be larger than 2GB, except on platforms that have "Large File Support"(LFS). 

### Command line Tools
* **[ncdump](https://www.unidata.ucar.edu/software/netcdf/docs/netcdf_utilities_guide.html#ncdump_guide)**

The ncdump command is used to show the contents of netCDF files. It reads a netCDF file and outputs text. The output text is in a format called Common Data Language ([CDL](https://www.unidata.ucar.edu/software/netcdf/docs/netcdf_utilities_guide.html#cdl_guide)), describing netCDF objects and data. 
```
ncdump [-h] example.nc
```
* **[ncview](http://meteora.ucsd.edu/~pierce/ncview_home_page.html)**

ncview is a visual browser for netCDF format files. 
```
ncview example.nc
```
## 4. What can be seen in a NetCDF file (file structure and components)?
A netCDF file comprises two parts: a header part and a data part:
* Header part: contains all the information/metadata about dimensions, attributes and variables. 
* Data part: fixed-size data (the data for variables without unlimited dimension); variable-size data (the data for variables with unlimited dimension)

An example netCDF file read by ```ncdump```.
```
netcdf foo {    // example netCDF specification in CDL
dimensions:
lat = 10, lon = 5, time = unlimited;
variables:
  int     lat(lat), lon(lon), time(time);
  float   z(time,lat,lon), t(time,lat,lon);
  double  p(time,lat,lon);
  int     rh(time,lat,lon);
  lat:units = "degrees_north";
  lon:units = "degrees_east";
  time:units = "seconds";
  z:units = "meters";
  z:valid_range = 0., 5000.;
  p:_FillValue = -9999.;
  rh:_FillValue = -1;
data:
  lat   = 0, 10, 20, 30, 40, 50, 60, 70, 80, 90;
  lon   = -140, -118, -96, -84, -52;
}
```


# GeoTiff
## 1. What is GeoTiff?

## 2. How to view a GeoTiff file?

# GDAL
