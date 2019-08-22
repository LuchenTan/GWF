#!/usr/bin/env python
# coding: utf-8

from netCDF4 import Dataset
import sys
import logging


def merge_file(ensemble, yyyy, log):
    file_path = './' + yyyy + '_' + ensemble + '.nc'
    hus_path = './huss_' + ensemble + '_final.nc'
    pr_path = './pr_' + ensemble + '_final.nc'
    ps_path = './ps_' + ensemble + '_final.nc'
    rlds_path = './rlds_' + ensemble + '_final.nc'
    rsds_path = './rsds_' + ensemble + '_final.nc'
    wind_speed_path = './sfcWind_' + ensemble + '_final.nc'
    ta_path = './tas_' + ensemble + '_final.nc'

    all_file = Dataset(file_path, 'a')

    # Merge rlon, rlat, time
    log.info('Merging rlon, rlat, time, lon, lat')
    part_file = Dataset(hus_path, 'r')

    part_data = part_file['lon'][:]
    all_file['rlon'][:] = part_data

    part_data = part_file['lat'][:]
    all_file['rlat'][:] = part_data

    start = (int(yyyy) - 1951) * 2920
    end = start + 2919

    part_data = part_file['time']
    all_data = all_file['time']
    index = 0
    for i in range(start, end + 1):
        all_data[index] = part_data[i]
        index += 1

    part_file.close()

    rlon_data = all_file['rlon']
    rlat_data = all_file['rlat']
    lon_data = all_file['lon']
    lat_data = all_file['lat']

    for ilat in range(len(lon_data)):
        lon_data[ilat] = rlon_data[:]

    for ilat in range(len(lat_data)):
        lat_data[ilat] = rlat_data[ilat]

    # Merge huss
    log.info('Merging hus')
    part_file = Dataset(hus_path, 'r')

    index = 0
    for i in range(start, end + 1):
        all_file['hus'][index] = part_file['huss'][i]
        index += 1

    part_file.close()

    # Merge pr
    log.info('Merging pr')
    part_file = Dataset(pr_path, 'r')

    part_data = part_file['pr']
    all_data = all_file['pr']
    index = 0
    for i in range(start, end + 1):
        all_data[index] = part_data[i]
        index += 1

    part_file.close()

    # Merge ps
    log.info('Merging ps')
    part_file = Dataset(ps_path, 'r')

    part_data = part_file['ps']
    all_data = all_file['ps']
    index = 0
    for i in range(start, end + 1):
        all_data[index] = part_data[i]
        index += 1

    part_file.close()

    # Merge rlds
    log.info('Merging rlds')
    part_file = Dataset(rlds_path, 'r')

    part_data = part_file['rlds']
    all_data = all_file['rlds']
    index = 0
    for i in range(start, end + 1):
        all_data[index] = part_data[i]
        index += 1

    part_file.close()

    # Merge rsds
    log.info('Merging rsds')
    part_file = Dataset(rsds_path, 'r')

    part_data = part_file['rsds']
    all_data = all_file['rsds']
    index = 0
    for i in range(start, end + 1):
        all_data[index] = part_data[i]
        index += 1

    part_file.close()

    # Merge wind_speed
    log.info('Merging wind_speed')
    part_file = Dataset(wind_speed_path, 'r')

    part_data = part_file['sfcWind']
    all_data = all_file['wind_speed']
    index = 0
    for i in range(start, end + 1):
        all_data[index] = part_data[i]
        index += 1

    part_file.close()

    # Merge tas
    log.info('Merging ta')
    part_file = Dataset(ta_path, 'r')

    part_data = part_file['tas']
    all_data = all_file['ta']
    index = 0
    for i in range(start, end + 1):
        all_data[index] = part_data[i]
        index += 1

    part_file.close()
    all_file.close()

    log.info(yyyy+'_'+ensemble+'.nc Done!')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('arg1: ensemble membler\narg2: year')

    ensemble_member = sys.argv[1]
    year = sys.argv[2]

    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(
        filename=ensemble_member + '.log',
        filemode='a',
        level=logging.INFO,
        format=FORMAT,
        datefmt='%a, %d %b %Y %H:%M:%S'
    )
    logging.info('Starting to merge data of ' + year)

    merge_file(ensemble_member, year, logging)
