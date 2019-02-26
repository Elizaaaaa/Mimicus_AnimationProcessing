import glob
import os
import pandas as pd

path = './output/csv/'
move_types = os.listdir(path)
for move in move_types:
	move_path = path + move + '/'
	all_files = glob.glob(os.path.join(move_path, "*.csv"))
	df_from_each_file = (pd.read_csv(f) for f in sorted(all_files))
  	concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)

  	concatenated_df['frame'] = concatenated_df.index+1
  	concatenated_df.to_csv(move_path + "/csv_joined.csv", index=False)

#movement_types = []
#all_files = glob.glob(os.path.join(path, "*.csv"))

#for files in sorted(all_files):
#	nameLen = len(files) - 7
#	move_name = files[0:nameLen]
#	if move_name not in movement_types:
#		movement_types.append(move_name)

#print(movement_types)

#for move in movement_types:
#	for f in sorted(all_files):
#		if f[0:len(f)-7] == move:
#			df_from_file = pd.read_csv(f)
#			print(df_from_file)
#	concatenated_df = pd.concat(df_from_file, ignore_index=True)
#	concatenated_df['frame'] = concatenated_df.index+1
 # 	concatenated_df.to_csv("./output/csv_joined/csv_"+move+".csv", index=False)
#	df_from_file = df_from_file.reset_index(drop=True)




