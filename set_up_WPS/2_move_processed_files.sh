#!/bin/bash

# Where the processed grib / netcdf files live 
SOURCE_DIR='/global/scratch/users/siennaw/gsi_2024/grib2nc/2017/working/'

# Where we want to move all the finished files 
DEST_DIR="/global/scratch/users/siennaw/gsi_2024/grib2nc/2017/finished/" #'/global/scratch/users/siennaw/gsi_2024/grib2nc/finished/'

# Ensure the destination directory exists
#mkdir -p "$DEST_DIR"

# Loop through each folder in the source directory
for folder in "$SOURCE_DIR"/*; do
    if [ -d "$folder" ]; then
        # Find and move files starting with 'wrfinput_' to the destination directory
        # thank you chatgpt for this line of code
        echo $folder
        find "$folder" -maxdepth 1 -type f -name "wrfinput_*" -exec mv {} "$DEST_DIR" \;
    fi
done 