#!/bin/sh
#SBATCH --job-name=set_up_WPS_runs
#SBATCH --partition=savio3_htc
#SBATCH --account=co_aiolos 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=1
#SBATCH --time=03:00:00


python -u 1_set_up_bkg.py