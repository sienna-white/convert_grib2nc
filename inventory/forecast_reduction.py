import os
import re
import shutil

# where all the original forecast files are
source_dir = "/global/scratch/users/siennaw/gsi_2024/grib2nc/2019/finished"

# where only the best forecast files are moving to 
destination_dir = "/global/scratch/users/siennaw/gsi_2024/grib2nc/2019/best_forecast"

# this dictionary will map each date to a tuple: (lowest_number_found, filename)
lowest_files = {}

# this captures the date (10 digits) and the number (one or more digits) after the underscore.
pattern = re.compile(r'wrfinput_d01_(\d{10})_(\d+)\.nc')

# loop over every file in the source directory
for filename in os.listdir(source_dir):
    match = pattern.match(filename)
    if match:
        date_str = match.group(1)
        file_number = int(match.group(2))

        print("File is %s / date=%s / number=%d" % (filename, date_str, file_number))

        # If this date hasn't been seen yet or this file has a lower number, record it.
        if date_str not in lowest_files:
            print("Adding %s to dict %s" % (filename, date_str))
            lowest_files[date_str] = (file_number, filename)

        elif file_number < lowest_files[date_str][0]:
            print("REPLACING FH=%d --> Saving %s " % (lowest_files[date_str][0], filename))
            lowest_files[date_str] = (file_number, filename)


# write dictionary to a text file 
lowest_files = dict(sorted(lowest_files.items()))
with open("best_forecast_files.txt", "w") as f:
    for date_str, (num, filename) in lowest_files.items():
        f.write(f"{date_str} {num} {filename}\n")
        print(f"Date: {date_str}, FH: {num}, Filename: {filename}")

# move the file with the lowest number for each date to the destination directory
for date_str, (num, filename) in lowest_files.items():
    src_path = os.path.join(source_dir, filename)
    dest_path = os.path.join(destination_dir, filename)

    # Check if the destination file already exists
    if os.path.exists(dest_path):
        print(f"File {filename} already exists in destination. Skipping.")
        continue
    else:
        os.symlink(src_path, dest_path)
    # shutil.move(src_path, dest_path)
    print(f"Created symlink for {filename} to {destination_dir}")
    # assert(False)

