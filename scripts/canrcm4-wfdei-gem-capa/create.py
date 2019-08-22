#!/usr/bin/env python
# coding: utf-8
from netCDF4 import Dataset
import numpy as np
import sys
import re


def create_file(_ensemble, _year):
    file_path = './' + _year + '_' + _ensemble + '.nc'

    # Create an empty file
    nc = Dataset(file_path, 'w', format='NETCDF4_CLASSIC')

    # Create dimensions
    nc.createDimension('rlon', 800)
    nc.createDimension('rlat', 328)
    nc.createDimension('time', None)

    # Create variables
    # Create rlon
    v_rlon = nc.createVariable('rlon', np.float32, ('rlon',), zlib=True)
    v_rlon.standard_name = "longitude"
    v_rlon.long_name =  "longitude"
    v_rlon.units = "degrees_east"
    v_rlon.axis = "X"

    # Create rlat
    v_rlat = nc.createVariable('rlat', np.float32, ('rlat',), zlib=True)
    v_rlat.standard_name = "latitude"
    v_rlat.long_name = "latitude"
    v_rlat.units = "degrees_north"
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
    v_time.units = "hours since 1951-1-1 00:00:00"
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
    args = re.findall(r"\d+\.?\d*", _ensemble)
    realization = args[0]
    initialization = args[1]
    physics = args[2]
    eid = args[3]
    
    if _ensemble == 'r8i2p1r1':
        nc.CCCma_runid = "nam44_v002_eia-008"
        nc.creation_date = "2016-12-13-T17:48:26Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eia-008"
    if _ensemble == 'r8i2p1r2':
        nc.CCCma_runid = "nam44_v002_eib-008"
        nc.creation_date = "2016-12-13-T01:51:35Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eib-008"
    if _ensemble == 'r8i2p1r3':
        nc.CCCma_runid = "nam44_v002_eic-008"
        nc.creation_date = "2016-12-12-T21:03:35Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eic-008"
    if _ensemble == 'r8i2p1r4':
        nc.CCCma_runid = "nam44_v002_eid-008"
        nc.creation_date = "2016-12-13-T17:48:47Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eid-008"
    if _ensemble == 'r8i2p1r5':
        nc.CCCma_runid = "nam44_v002_eie-008"
        nc.creation_date = "2016-12-13-T17:49:10Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eie-008"
    if _ensemble == 'r9i2p1r1':
        nc.CCCma_runid = "nam44_v002_eia-009"
        nc.creation_date = "2016-12-12-T18:28:25Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eia-009"
    if _ensemble == 'r9i2p1r2':
        nc.CCCma_runid = "nam44_v002_eib-009"
        nc.creation_date = "2016-12-14-T17:57:55Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eib-009"
    if _ensemble == 'r9i2p1r3':
        nc.CCCma_runid = "nam44_v002_eic-009"
        nc.creation_date = "2016-12-13-T19:09:00Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eic-009"
    if _ensemble == 'r9i2p1r4':
        nc.CCCma_runid = "nam44_v002_eid-009"
        nc.creation_date = "2016-12-13-T19:08:35Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eid-009"
    if _ensemble == 'r9i2p1r5':
        nc.CCCma_runid = "nam44_v002_eie-009"
        nc.creation_date = "2016-12-13-T00:39:10Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eie-009"
    if _ensemble == 'r10i2p1r1':
        nc.CCCma_runid = "nam44_v002_eia-010"
        nc.creation_date = "2016-12-13-T21:38:22Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eia-010"
    if _ensemble == 'r10i2p1r2':
        nc.CCCma_runid = "nam44_v002_eib-010"
        nc.creation_date = "2016-12-12-T18:32:27Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eib-010"
    if _ensemble == 'r10i2p1r3':
        nc.CCCma_runid = "nam44_v002_eic-010"
        nc.creation_date = "2016-12-13-T00:38:21Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eic-010"
    if _ensemble == 'r10i2p1r4':
        nc.CCCma_runid = "nam44_v002_eid-010"
        nc.creation_date = "2016-12-12-T18:32:51Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eid-010"
    if _ensemble == 'r10i2p1r5':
        nc.CCCma_runid = "nam44_v002_eie-010"
        nc.creation_date = "2016-12-15-T00:01:21Z"
        nc.experiment = "CanSISE downscaling run driven by CCCma-CanESM2 eie-010"

    nc.experiment_id = "historical-r"+eid
    nc.driving_experiment = "CCCma-CanESM2, historical-r"+eid+", r"+realization+"i"+initialization+"p"+physics
    nc.driving_experiment_name = "historical-r"+eid
    nc.driving_model_ensemble_member = "r"+realization+"i"+initialization+"p"+physics
    nc.realization = realization
    nc.initialization_method = initialization
    nc.physics_version = physics
    nc.gwf_product = "canrcm4-wfdei-gem-capa"
    nc.CDI = "Climate Data Interface version 1.7.2 (http://mpimet.mpg.de/cdi)"
    nc.institution = "CCCma (Canadian Centre for Climate Modelling and Analysis, Victoria, BC, Canada)"
    nc.Conventions = "CF-1.6"
    nc.title = "CanRCM4 model output prepared for CanSISE Project"
    nc.institute_id = "CCCma"
    nc.driving_model_id = "CCCma-CanESM2"
    nc.forcing = "GHG,Oz,SA,BC,OC,LU,Vl (GHG includes CO2,CH4,N2O,CFC11,effective CFC12)"
    nc.project_id = "CanSISE"
    nc.model_id = "CCCma-CanRCM4"
    nc.CORDEX_domain = "NAM-44"
    nc.rcm_version_id = "r2"
    nc.frequency = "1hr"
    nc.product = "output"
    nc.contact = "cccma_info@ec.gc.ca"
    nc.references = "http://www.cccma.ec.gc.ca/models"
    nc.data_licence = "1) GRANT OF LICENCE - The Government of Canada (Environment Canada) is the \n""owner of all intellectual property rights (including copyright) that may exist in this Data \n""product. You (as \"The Licensee\") are hereby granted a non-exclusive, non-assignable, \n""non-transferable unrestricted licence to use this data product for any purpose including \n""the right to share these data with others and to make value-added and derivative \n""products from it. This licence is not a sale of any or all of the owner\'s rights.\n""2) NO WARRANTY - This Data product is provided \"as-is\"; it has not been designed or \n""prepared to meet the Licensee\'s particular requirements. Environment Canada makes no \n""warranty, either express or implied, including but not limited to, warranties of \n""merchantability and fitness for a particular purpose. In no event will Environment Canada \n""be liable for any indirect, special, consequential or other damages attributed to the \n""Licensee\'s use of the Data product."
    nc.CDO = "Climate Data Operators version 1.7.2 (http://mpimet.mpg.de/cdo)"
    nc.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('arg1: ensemble\narg2: year')

    ensemble = sys.argv[1]
    year = sys.argv[2]

    create_file(ensemble, year)
