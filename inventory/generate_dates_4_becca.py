'''
generating a list of folders for becca to copy
the idea is that any file that is missing --> we want the folder name of whatever
the most recent folder is that has that file 
'''
import pandas as pd 


inventory = pd.read_csv('inventory_2019.csv')
print(inventory)
print(inventory.columns)  

date_col = inventory.columns[0]
dates = inventory[date_col]
# dates = pd.to_datetime(dates, format='%Y-%m-%d')
print(dates)


previous = "Skip"

copy_date = []


inventory.set_index('Unnamed: 0', inplace=True)
print(inventory.columns)

values = inventory.values.ravel() 


nrows = len(inventory)
ncols = len(inventory.columns)

copy_date_ind = [] 

for ind,i in enumerate(values):
    # print("Looking at %d value = %s" % (ind, i))
    if ind<2: 
        continue
    if i==0:
        for k in range(6, 24):
            check_ = values[ind-k]
            if check_ == 1:
                print(k)
                print("Found a hour to fill the gap @ %d" % (ind-k))
                copy_date_ind.append(ind-(k+1))
                break


copy_date_ind = list(set(copy_date_ind))

# Convert to row + column index
copy_date_row = [i//ncols for i in copy_date_ind]
copy_date_col = [i%ncols for i in copy_date_ind]

date = [inventory.index[i] for i in copy_date_row]
hour = [inventory.columns[i] for i in copy_date_col]

combined = ["%s%s" % (date[i].replace('-',''), hour[i]) for i in range(len(date))]
print(combined)
# for date in dates:
#     converted = inventory.loc[inventory[date_col] == date]
#     for hour in range(0, 24):
#         hr = "%02d" % hour
#         exists = converted[hr].values
#         if exists == 1:
#             previous = "%s%s" % (date.replace("-",""), hr)
#         else: 
#             copy_date.append(previous) # print("%s %d doesn't exist" % (date, hour))

# # 2020090113
# copy_date = list(set(copy_date))        
# print(copy_date)
# # Write to text file 

with open('dates_2_copy_MSU_March2.txt', 'w') as f:
    for date in combined:
        f.write(date + '\n')
    