#!/bin/bash

# Path to the file you want to symlink
SOURCE="/global/home/users/siennaw/scratch/gsi_2024/convert_grib2nc/wps_files/blank_wrfinput.nc"

# Target parent directory (adjust if needed)
PARENT_DIR="/global/scratch/users/siennaw/gsi_2024/grib2nc/2021/working"

# Loop through each subdirectory in the parent directory
for dir in "$PARENT_DIR"/*/; do
    # Check if it is actually a directory
    [ -d "$dir" ] || continue

    # Create symlink inside the subdirectory
    ln -sf "$(realpath "$SOURCE")" "$dir/blank_wrfinput.nc"
    echo "Linked $SOURCE into $dir"
done