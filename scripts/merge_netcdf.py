import sys
import numpy as np
import netCDF4


def merge_files(main_file_name, second_file_name, variables_to_merge, x_name='rlon', y_name='rlat'):
    """
    Merges the time slices of the second file into the first one. The files need to contain the same variables
    and dimensions (except for the time dimension)
    :param main_file_name:
        File containing the older time slices.
        Contents of the second file will be merged into this one.
    :param second_file_name:
        File containing the newer time slices.
    :param variables_to_merge:
        Variables to be merged into the first file.
    :param x_name: Name of x dimension
    :param y_name: Name of y dimension
    """
    main_file = netCDF4.Dataset(main_file_name, 'r+')
    second_file = netCDF4.Dataset(second_file_name, 'r')

    main_times = main_file['time'][:]
    second_times = second_file['time'][:]

    if main_times[-1] >= second_times[0]:
        raise Exception('main file time ends after start of second file')

    if sorted(main_file.variables.keys()) != sorted(second_file.variables.keys()):
        raise Exception('Variables don\'t match')

    if (main_file[x_name][:] != second_file[x_name][:]).any() \
            or (main_file[y_name][:] != second_file[y_name][:]).any() \
            or (main_file['lat'][:] != second_file['lat'][:]).any() \
            or (main_file['lon'][:] != second_file['lon'][:]).any():
        raise Exception('x/y or lat/lon dimensions don\'t match')

    if main_file.ncattrs() != second_file.ncattrs() or main_file.dimensions.keys() != second_file.dimensions.keys():
        raise Exception('File attributes or dimensions don\'t match')

    print('Appending time slices')
    main_file['time'][:] = np.append(main_file['time'][:], second_file['time'][:])

    for var_name in variables_to_merge:

        if main_file[var_name].ncattrs() != second_file[var_name].ncattrs():
            raise Exception('Variable {} has different attributes'.format(var_name))

        print('Appending variable {}'.format(var_name))
        second_data = second_file[var_name][:]
        main_file[var_name][len(main_times):len(main_times) + len(second_times)] = second_data

    main_file.close()
    second_file.close()


if __name__ == '__main__':

    if len(sys.argv) < 6:
        raise Exception('Usage: python merge-netcdf.py mainFile.nc secondFile.nc x_dim_name y_dim_name '
                        'var_to_merge_1 var_to_merge_2 ...')

    file_main = sys.argv[1]
    file_two = sys.argv[2]
    x_dim_name = sys.argv[3]
    y_dim_name = sys.argv[4]

    variables_to_merge = sys.argv[5:]

    merge_files(file_main, file_two, variables_to_merge, x_dim_name, y_dim_name)
