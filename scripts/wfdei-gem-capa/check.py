from random import randint
from netCDF4 import Dataset
import sys


def generate_points(_year):
    _points = []

    for i in range(10):
        point = []
        new_time = randint(0, 2919)
        old_time = new_time + (_year - 1951) * 2920
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
    if len(sys.argv) < 3:
        raise Exception('arg1: ensemble membler\narg2: year')

    ensemble_member = sys.argv[1]
    year = sys.argv[2]

    new_file = './' + year + '_' + ensemble_member + '.nc'
    hus_file = './' + 'huss_'+ ensemble_member + '_final.nc'
    pr_file = './' + 'pr_' + ensemble_member + '_final.nc'
    ps_file = './' + 'ps_' + ensemble_member + '_final.nc'
    rlds_file = './' + 'rlds_' + ensemble_member + '_final.nc'
    rsds_file = './' + 'rsds_' + ensemble_member + '_final.nc'
    wind_speed_file = './' + 'sfcWind_' + ensemble_member + '_final.nc'
    ta_file = './' + 'tas_' + ensemble_member + '_final.nc'

    points = generate_points(int(year))

    if (check_hus() and check_pr() and check_ps() and check_rlds() and
            check_rsds() and check_wind_speed() and check_ta()):
        print(new_file + ': ok')
    else:
        print(new_file + ': corrupted')
