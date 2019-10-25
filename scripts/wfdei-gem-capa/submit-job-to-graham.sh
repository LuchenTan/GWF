#!/bin/bash

# submit with:
#       sbatch submit-job-to-graham.sh

# takes about 10min/year
# 38 * 10min = 6h 20min

#SBATCH --account=rpp-hwheater                     # your group NOT SURE IF THAT IS CALLED LIKE THIS
#SBATCH --mem-per-cpu=10G                          # memory; default unit is megabytes
#SBATCH --mail-user=juliane.mai@uwaterloo.ca       # email address for notifications
#SBATCH --mail-type=FAIL                           # email send only in case of failure
#SBATCH --time=0-08:00                             # time (DD-HH:MM);  here 8hr
#SBATCH --job-name=wfdei-gem-capa                  # name of job in queque

# chnage to where the Python scripts sit
cd /home/julemai/projects/rpp-hwheater/julemai/kitchen-sink/scripts/wfdei-gem-capa

# activate Python environment
source /home/julemai/projects/rpp-hwheater/julemai/cuizinart/env-3.5/bin/activate

# loop over all years
for (( ii=1979; ii<= 2016; ii++ )) ; do
    python create.py ${ii}
    python merge.py ${ii}
done
