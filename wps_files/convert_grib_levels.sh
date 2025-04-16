# Loop through each matching file
for file in GRIBFILE.A*; do
    # Check if the file exists to avoid issues if no matches are found
    [ -e "$file" ] || continue

    echo "Processing $file"
    mv $file ${file}_old

    # Replace the line below with your actual command
    /global/scratch/users/siennaw/gsi_2024/compiling/wrf_executables/wgrib2 -set_lev "1 hybrid level" ${file}_old -GRIB $file

    rm ${file}_old

done



