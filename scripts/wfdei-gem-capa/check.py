from random import randint
from netCDF4 import Dataset
import sys


def generate_points(_year):
    _points = []

    for i in range(10):
        point = []
        new_time = randint(0, 2919)
        old_time = new_time + (_year - 1979) * 2920
        lat = randint(0, 327)
        lon = randint(0, 799)

        point.append(new_time)
        point.append(old_time)
        point.append(lat)
        point.append(lon)

        _points.append(point)

    return _points


def check_data(_new_data, _old_data):
    for point in points:
        new_time = point[0]
        old_time = point[1]
        lat = point[2]
        lon = point[3]
        if _new_data[new_time][lat][lon] != _old_data[old_time][lat][lon]:
            return False

    return True


def check_hus():
    new_ds = Dataset(new_file, 'r')
    old_ds = Dataset(hus_file, 'r')

    new_data = new_ds['hus']
    old_data = old_ds['huss']

    result = check_data(new_data, old_data)

    new_ds.close()
    old_ds.close()

    return result


def check_pr():
    new_ds = Dataset(new_file, 'r')
    old_ds = Dataset(pr_file, 'r')

    new_data = new_ds['pr']
    old_data = old_ds['pr']

    result = check_data(new_data, old_data)

    new_ds.close()
    old_ds.close()

    return result


def check_ps():
    new_ds = Dataset(new_file, 'r')
    old_ds = Dataset(ps_file, 'r')

    new_data = new_ds['ps']
    old_data = old_ds['ps']

    result = check_data(new_data, old_data)

    new_ds.close()
    old_ds.close()

    return result


def check_rlds():
    new_ds = Dataset(new_file, 'r')
    old_ds = Dataset(rlds_file, 'r')

    new_data = new_ds['rlds']
    old_data = old_ds['rlds']

    result = check_data(new_data, old_data)

    new_ds.close()
    old_ds.close()

    return result


def check_rsds():
    new_ds = Dataset(new_file, 'r')
    old_ds = Dataset(rsds_file, 'r')

    new_data = new_ds['rsds']
    old_data = old_ds['rsds']

    result = check_data(new_data, old_data)

    new_ds.close()
    old_ds.close()

    return result


def check_rsds_thresholded():
    new_ds = Dataset(new_file, 'r')
    old_ds = Dataset(rsds_thres_file, 'r')

    new_data = new_ds['rsds_thresholded']
    old_data = old_ds['rsds']

    result = check_data(new_data, old_data)

    new_ds.close()
    old_ds.close()

    return result


def check_wind_speed():
    new_ds = Dataset(new_file, 'r')
    old_ds = Dataset(wind_speed_file, 'r')

    new_data = new_ds['wind_speed']
    old_data = old_ds['sfcWind']

    result = check_data(new_data, old_data)

    new_ds.close()
    old_ds.close()

    return result


def check_ta():
    new_ds = Dataset(new_file, 'r')
    old_ds = Dataset(ta_file, 'r')

    new_data = new_ds['ta']
    old_data = old_ds['tas']

    result = check_data(new_data, old_data)

    new_ds.close()
    old_ds.close()

    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('arg1: year')

    year = sys.argv[1]

    new_file        =    '../../../cuizinart/data/wfdei-gem-capa/' + year + '/' + year + '.nc'
    hus_file        =    '../../../cuizinart/data/wfdei-gem-capa/original/huss_WFDEI_GEM_1979_2016-final.nc'
    pr_file         =      '../../../cuizinart/data/wfdei-gem-capa/original/pr_WFDEI_GEM_1979_2016-final.nc'
    ps_file         =      '../../../cuizinart/data/wfdei-gem-capa/original/ps_WFDEI_GEM_1979_2016-final.nc'
    rlds_file       =    '../../../cuizinart/data/wfdei-gem-capa/original/rlds_WFDEI_GEM_1979_2016-final.nc'
    rsds_file       =    '../../../cuizinart/data/wfdei-gem-capa/original/rsds_WFDEI_GEM_1979_2016-final.nc'
    rsds_thres_file =    '../../../cuizinart/data/wfdei-gem-capa/original/rsds_WFDEI_GEM_1979_2016-final_thresholded.nc'
    wind_speed_file = '../../../cuizinart/data/wfdei-gem-capa/original/sfcWind_WFDEI_GEM_1979_2016-final.nc'
    ta_file         =     '../../../cuizinart/data/wfdei-gem-capa/original/tas_WFDEI_GEM_1979_2016-final.nc'

    points = generate_points(int(year))

    if (check_hus() and check_pr() and check_ps() and check_rlds() and
            check_rsds() and check_rsds_thresholded() and check_wind_speed() and check_ta()):
        print(new_file + ': ok')
    else:
        print(new_file + ': corrupted')
