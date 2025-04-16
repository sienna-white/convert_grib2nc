BASE_DIR="/global/scratch/users/siennaw/gsi_2024/grib2nc/2018/working2"  # replace with your target directory
OLD_PATH="./global/scratch/users/siennaw/gsi_2024/compiling/wrf_executables/wgrib2"
NEW_PATH="/global/scratch/users/siennaw/gsi_2024/compiling/wrf_executables/wgrib2"

grep -rl "$OLD_PATH" "$BASE_DIR" --include="*.sh" | while read -r file; do
    echo "Fixing $file"
    sed -i.bak "s|^$OLD_PATH\$|$NEW_PATH|" "$file"
done