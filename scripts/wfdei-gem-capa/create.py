#!/usr/bin/env python
# coding: utf-8
from netCDF4 import Dataset
import numpy as np
import sys
import re


def create_file(_year):
    file_path = '../../../cuizinart/data/wfdei-gem-capa/' + _year + '.nc'

    # Create an empty file
    nc = Dataset(file_path, 'w', format='NETCDF4_CLASSIC')

    # Create dimensions
    nc.createDimension('rlon', 800)
    nc.createDimension('rlat', 328)
    nc.createDimension('time', None)

    # Create variables
    # Create rlon
    v_rlon = nc.createVariable('rlon', np.float32, ('rlon',), zlib=True)
    v_rlon.standard_name = "grid_longitude"
    v_rlon.long_name =  "longitude"
    v_rlon.units = "degrees"
    v_rlon.axis = "X"

    # Create rlat
    v_rlat = nc.createVariable('rlat', np.float32, ('rlat',), zlib=True)
    v_rlat.standard_name = "grid_latitude"
    v_rlat.long_name = "latitude"
    v_rlat.units = "degrees"
    v_rlat.axis = "Y"

    # Create lon
    v_lon = nc.createVariable('lon', np.float32, ('rlat','rlon'), zlib=True)
    v_lon.standard_name = "longitude"
    v_lon.long_name = "longitude"
    v_lon.units = "degrees_east"

    # Create lat
    v_lat = nc.createVariable('lat', np.float32, ('rlat','rlon'), zlib=True)
    v_lat.standard_name = "latitude"
    v_lat.long_name = "latitude"
    v_lat.units = "degrees_north"

    # Create time
    v_time = nc.createVariable('time', np.int32, ('time',), zlib=True)
    v_time.standard_name = "time"
    v_time.long_name = "time"
    v_time.units = "hours since 1979-01-01 00:00:00"
    v_time.calendar = "365_day"
    v_time.axis = "T"

    # Create hus
    v_hus = nc.createVariable('hus', np.float32, ('time', 'rlat', 'rlon'), zlib=True)
    v_hus.long_name = "Specific Humidity at Lowest Model Level (sigma=0.995 = lowest model level = approx 40 m) in kg kg-1"
    v_hus.units = "1"
    v_hus.coordinates = "lon lat"
    v_hus.standard_name = "specific_humidity"

    # Create pr
    v_pr = nc.createVariable('pr', np.float32, ('time', 'rlat', 'rlon'), zlib=True)
    v_pr.long_name = "Precipitation (surface)"
    v_pr.units = "kg m-2 s-1"
    v_pr.coordinates = "lon lat"
    v_pr.standard_name = "precipitation_flux"

    # Create ps
    v_ps = nc.createVariable('ps', np.float32, ('time', 'rlat', 'rlon'), zlib=True)
    v_ps.long_name = "Surface Pressure (surface)"
    v_ps.units = "Pa"
    v_ps.coordinates = "lon lat"
    v_ps.standard_name = "surface_air_pressure"

    # Create rlds
    v_rlds = nc.createVariable('rlds', np.float32, ('time', 'rlat', 'rlon'), fill_value=1e+20, zlib=True)
    v_rlds.standard_name = "surface_downwelling_longwave_flux_in_air"
    v_rlds.long_name = "Surface Downwelling Longwave Radiation"
    v_rlds.units = "W m-2"
    v_rlds.missing_value = np.float32(1e20)
    v_rlds.coordinates = "lon lat"

    # Create rsds
    v_rsds = nc.createVariable('rsds', np.float32, ('time', 'rlat', 'rlon'), fill_value=1e+20, zlib=True)
    v_rsds.standard_name = "surface_downwelling_shortwave_flux_in_air"
    v_rsds.long_name = "Surface Downwelling Shortwave Radiation"
    v_rsds.units = "W m-2"
    v_rsds.missing_value = np.float32(1e20)
    v_rsds.coordinates = "lon lat"

    # Create rsds_thresholded
    v_rsds = nc.createVariable('rsds_thresholded', np.float32, ('time', 'rlat', 'rlon'), fill_value=1e+20, zlib=True)
    v_rsds.standard_name = "surface_downwelling_shortwave_flux_in_air"
    v_rsds.long_name = "Surface Downwelling Shortwave Radiation (rsds) variable post-processed setting values to zeros if they were zero in WFDEI"
    v_rsds.units = "W m-2"
    v_rsds.missing_value = np.float32(1e20)
    v_rsds.coordinates = "lon lat"

    # Create wind_speed
    v_wind = nc.createVariable('wind_speed', np.float32, ('time', 'rlat', 'rlon'), zlib=True)
    v_wind.long_name = "Zonal (Eastward) Wind (sigma=0.995 = lowest model level = approx 40 m)"
    v_wind.units = "m s**-1"
    v_wind.coordinates = "lon lat"
    v_wind.standard_name = "wind_speed"

    # Create ta
    v_ta = nc.createVariable('ta', np.float32, ('time', 'rlat', 'rlon'), zlib=True)
    v_ta.long_name = "Air Temperature (sigma=0.995 = lowest model level = approx 40 m)"
    v_ta.units = "K"
    v_ta.coordinates = "lon lat"
    v_ta.standard_name = "air_temperature"

    # Create global attributes
    nc.Conventions = "CF-1.6" ;
    nc.Title = "A Bias-Corrected 3-hourly 0.125 Gridded Meteorological Forcing Data Set (1979 – 2016) for Land Surface Modeling in North America (WFDEI-GEM-CaPA)" ;
    nc.Methodology = "https://www.frdr.ca/repo/handle/doi:10.20383/101.0111" ;
    nc.Author1 = "Asong, Zilefac Elvis; University of Saskatchewan; https://orcid.org/0000-0001-7086-6764" ;
    nc.Author2 = "Wheater, Howard; University of Saskatchewan" ;
    nc.Author3 = "Pomeroy, John; University of Saskatchewan" ;
    nc.Author4 = "Pietroniro, Alain; Environment and Climate Change Canada" ;
    nc.Author5 = "Elshamy, Mohamed; University of Saskatchewan; https://orcid.org/0000-0002-3621-0021" ;
    nc.gwf_product = "wfdei-gem-capa"
    nc.frequency = "3hr"
    nc.Descrption = "Cold regions hydrology is very sensitive to the impacts of climate warming. Future warming is expected to increase the proportion of winter precipitation falling as rainfall. Snowpacks are expected to undergo less sublimation, form later and melt earlier and possibly more slowly, leading to earlier spring peak streamflow. More physically realistic and sophisticated hydrological models driven by reliable climate forcing can provide the capability to assess hydrologic responses to climate change. However, hydrological processes in cold regions involve complex phase changes and so are very sensitive to small biases in the driving meteorology, particularly temperature and precipitation. Cold regions often have sparse surface observations, particularly at high elevations that generate the major amount of runoff. The effects of mountain topography and high latitudes are not well reflected in the observational record. The best available gridded data in these regions is from the high resolution forecasts of the Global Environmental Multiscale (GEM) atmospheric model and the Canadian Precipitation Analysis (CaPA) reanalysis but this dataset has a short historical record. The EU WATCH ERA-Interim reanalysis (WFDEI) has a longer historical record, but has often been found to be biased relative to observations over Canada. The aim of this study, therefore, is to blend the strengths of both datasets (GEM-CaPA and WFDEI) to produce a less-biased long record product (WFDEI-GEM-CaPA). First, a multivariate generalization of the quantile mapping technique was implemented to bias-correct WFDEI against GEM-CaPA at 3h x 0.125 deg resolution during the 2005-2016 period, followed by a hindcast of WFDEI-GEM-CaPA from 1979."
    nc.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('arg1: year')

    year = sys.argv[1]

    create_file(year)
