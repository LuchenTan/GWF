import argparse
import pathlib 
import os

from PIL import Image
from netCDF4 import Dataset

parser = argparse.ArgumentParser()
parser.add_argument("image_directory_name", help="The name of the directory containing the .cr2 images.")
args = parser.parse_args()

character_to_month_mapping = {

    "J": "January",
    "F": "February",
    "M": "March",
    "A": "April",
    "Y": "May",
    "U": "June",
    "L": "July",
    "G": "August",
    "S": "September",
    "O": "October",
    "N": "November",
    "D": "December"

}

image_directory = pathlib.Path(args.image_directory_name)
image_files = []

for (directory_path, _, filenames) in os.walk(image_directory):

    for filename in filenames:

        _, filename_extension = os.path.splitext(filename)
        if filename_extension == ".cr2":

            path = pathlib.Path(os.path.join(directory_path, filename))

            year = int(filename[0:4])
            month = character_to_month_mapping[filename[4]]
            day = int(filename[5:7])
            hour = int(filename[7:9])
            minute = int(filename[9:11])

            image_files += [(path, year, month, day, hour, minute)]

root = Dataset("test.nc", "w", format="NETCDF4")
root.createDimension("time", None)
root.createDimension("rlat", None)
root.createDimension("rlon", None)
root.createDimension("A1", None)
root.createDimension("A2", None)
root.createDimension("A3", None)
root.createDimension("A4", None)
root.createDimension("B1", None)
root.createDimension("B2", None)
root.createDimension("B3", None)
root.createDimension("B4", None)
root.createDimension("C1", None)
root.createDimension("C2", None)
root.createDimension("C3", None)
root.createDimension("C4", None)
root.createDimension("D1", None)
root.createDimension("D2", None)
root.createDimension("D3", None)
root.createDimension("D4", None)

time = root.createVariable("time", "float64", dimensions=("time",))
time.units = "hours since 2000-10-1 00:00:00"
time.calendar = "proleptic_gregorian"

lat = root.createVariable("lat", "float32", dimensions=("rlat", "rlon"))
lat.units = "degree north"
lat.long_name = "Latitude on mass grid"

lon = root.createVariable("lon", "float32", dimensions=("rlat", "rlon"))
lat.units = "degree east"
lat.long_name = "Longitude on mass grid"

lon = root.createVariable("lon", "float32", dimensions=("rlat", "rlon"))
lat.units = "degree east"
lat.long_name = "Longitude on mass grid"
