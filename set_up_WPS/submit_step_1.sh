#!/bin/sh
#SBATCH --job-name=set_up_WPS_runs
#SBATCH --partition=savio3_htc
#SBATCH --account=co_aiolos 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:30:00

# split -l 400 folders2process.txt 
#####  // SBATCH --ntasks-per-node=6

# ~/.conda/envs/smoke_env/bin/python -u second_run_through.py 

# python -u 1_set_up_bkg.py # xaa # remaining_folders2process_0.txt  jobs2run_0.sh > set_up_0.log 
# python -u 1_set_up_bkg.py xab  jobs2run_2.sh > set_up_2.log  & 
# python -u 1_set_up_bkg.py xac  jobs2run_3.sh > set_up_3.log  & 
# python -u 1_set_up_bkg.py xad  jobs2run_4.sh > set_up_4.log  &
# python -u 1_set_up_bkg.py # folders2process.txt  run_jan.sh > set_up_1.log

#  jobs2run_5.sh > set_up_5.log  &
# python -u 1_set_up_bkg.py folders2process.txt  jobs2run_1.sh > set_up_1.log  &
python -u 1_set_up_bkg.py 2017_files.txt run_2017.sh > run_2017.log  
&
# python -u 1_set_up_bkg.py xaa  jobs2run_1.sh > set_up_1.log  &
# python -u 1_set_up_bkg.py xab  jobs2run_2.sh > set_up_2.log  & 
# python -u 1_set_up_bkg.py xac  jobs2run_3.sh > set_up_3.log  & 
# python -u 1_set_up_bkg.py xad  jobs2run_4.sh > set_up_4.log  &
# python -u 1_set_up_bkg.py xae  jobs2run_5.sh > set_up_5.log  &
# python -u 1_set_up_bkg.py xaf  jobs2run_6.sh > set_up_5.log  &
# python -u 1_set_up_bkg.py xag  jobs2run_7.sh > set_up_7.log  &
# python -u 1_set_up_bkg.py xah  jobs2run_8.sh > set_up_8.log  &
# # python -u 1_set_up_bkg.py xaj  jobs2run_10.sh > set_up_10.log  &


# # python -u 1_set_up_bkg.py remaining_folders2process_3.txt  jobs2run_3.sh > set_up_3.log 
# # python -u 1_set_up_bkg.py remaining_folders2process_4.txt  jobs2run_4.sh > set_up_4.log  
# # python -u 1_set_up_bkg.py remaining_folders2process_5.txt  jobs2run_5.sh > set_up_5.log  
# # python -u 1_set_up_bkg.py remaining_folders2process_6.txt  jobs2run_6.sh > set_up_6.log 
# # python -u 1_set_up_bkg.py remaining_folders2process_7.txt  jobs2run_7.sh > set_up_7.log 
# # python -u 1_set_up_bkg.py remaining_folders2process_8.txt  jobs2run_8.sh > set_up_8.log 
# # python -u 1_set_up_bkg.py remaining_folders2process_9.txt  jobs2run_9.sh > set_up_9.log 
# # python -u 1_set_up_bkg.py remaining_folders2process_10.txt jobs2run_10.sh > set_up_10.log  
# # python -u 1_set_up_bkg.py remaining_folders2process_11.txt jobs2run_11.sh > set_up_11.log 
# python -u 1_set_up_bkg.py remaining_folders2process_12.txt jobs2run_12.sh > set_up_12.log  

wait