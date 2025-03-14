#!/bin/bash

# start drafting where we want to store these folders ... 
# Specify the directory containing the files

directory="/global/home/users/siennaw/scratch/data/wrf/"

cd $directory 
# Create subfolders for each year and month
for year in {2018..2023}; do
    for month in {01..12}; do
        mkdir -p "year_$year/month_$month"
    done
done

# # Move files to corresponding subfolders
# for file in "$directory"/wrfinput_d01_*.nc; do
#     if [[ -f "$file" ]]; then
#         # Extract the date part from the filename (assuming NUMBER is the last 9 characters)
#         date_part="${file: -9:9}"
#         # Extract the year and month parts from the date
#         year="${date_part:0:4}"
#         month="${date_part:4:2}"
#         # Move the file to the corresponding subfolder
#         mv "$file" "$directory/year_$year/month_$month/"
#     fi
# done
