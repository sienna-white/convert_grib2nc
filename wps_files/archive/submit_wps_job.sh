#!/bin/bash
# Job name:
#################################
#SBATCH --job-name=run_WPS
#
# Account:
#SBATCH --account=co_aiolos ## << this is the condo that tina bought // could also use fc_anemos#
#SBATCH --partition=savio
#
#SBATCH --nodes=5
# Wall clock limit (let's set to 10 mintes, 0 seconds)
#SBATCH --time=00:30:00
#
## Commands to run
cd /global/home/users/siennaw/scratch/WPS/test3/                 

# Set up + run ungrib
echo "LINKING GRIB FILES TO FOLDER..."
./link_grib.csh /global/home/users/siennaw/scratch/data/grib/2018110812/postprd/*

echo "LINKING HRR-SMOKE VTABLE...."
ln -sf ungrib/Variable_Tables/Vtable.hrrr_smoke.rap Vtable
#./ungrib.exe >> ungrib.out 

echo "RUNNING GEOGRID ..."
./geogrid.exe >>  geogrid.out          

echo "RUNNING METGRID ..."
./metgrid.exe >> metgrid.out
