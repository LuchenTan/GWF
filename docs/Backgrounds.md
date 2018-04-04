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
* **[ncview](http://meteora.ucsd.edu/~pierce/ncview_home_page.html)** is a visual browser for netCDF format files. 
```
ncview example.nc
```
*Tips: when showing a netCDF file, if the coordinate systems are correctly identified, the values for x and y axes should change as the cursor moving on the plot.*
### Other Viewer Tools
* **[Panoply](https://www.giss.nasa.gov/tools/panoply/)** can output CDL descriptions as well as plot variable data. Download and installation [here](https://www.giss.nasa.gov/tools/panoply/download/). 

*Tips: if lon-lat coordinates are correctly identified, it can plot data on a global or regional map using lon/lat variable data.
With a projection system, if the grid mapping variable is correctly described, it can plot data on the global map even without lon/lat variable data(Panoply will do the unprojection for you).*

## 4. What can be seen in a NetCDF file (file structure and components)?
A netCDF file comprises two parts: a header part and a data part:
* **Header part**: contains all the information/metadata about **Dimensions**, **Attributes** and **Variables**. 
* **Data part**: fixed-size data (the data for variables without unlimited dimension); variable-size data (the data for variables with unlimited dimension)

An example netCDF file read by ```ncdump```.
```
netcdf sfc_pres_temp {
dimensions:
   latitude = 6 ;
   longitude = 12 ;
variables:
   float latitude(latitude) ;
       latitude:units = "degrees_north" ;
   float longitude(longitude) ;
       longitude:units = "degrees_east" ;
   float pressure(latitude, longitude) ;
       pressure:units = "hPa" ;
data:
 latitude = 25, 30, 35, 40, 45, 50 ;
 longitude = -125, -120, -115, -110, -105, -100, -95, -90, -85, -80, -75, -70 ;
 pressure =
  900, 906, 912, 918, 924, 930, 936, 942, 948, 954, 960, 966,
  901, 907, 913, 919, 925, 931, 937, 943, 949, 955, 961, 967,
  902, 908, 914, 920, 926, 932, 938, 944, 950, 956, 962, 968,
  903, 909, 915, 921, 927, 933, 939, 945, 951, 957, 963, 969,
  904, 910, 916, 922, 928, 934, 940, 946, 952, 958, 964, 970,
  905, 911, 917, 923, 929, 935, 941, 947, 953, 959, 965, 971 ;
}
```
*In fact, data in netCDF files is a group of functions(called variables) with zero to multiple dimensions. Each variable has some meta data to self-describe the meaning of this variable, the meta data is called attributes. *

**NAMING:** ```letter_digit_seperated_by_underscores```. Starting from letter, no hyphon(-), case sensitive, ```_reserved``` for system names. 

### Dimensions
A dimension represents a quantity. It can be a physical spatiotemporal dimension: date or time (T), height or depth (Z), latitude (Y), longitude (X); or other user-defined quantities. 

Each dimension has a **name** and a **length**. There is not standard dimension names. Dimensions should be named meaningful.
Dimension length is an arbitrary positive integer or UNLIMITED.

# GeoTiff
## 1. What is GeoTiff?

## 2. How to view a GeoTiff file?

# GDAL
