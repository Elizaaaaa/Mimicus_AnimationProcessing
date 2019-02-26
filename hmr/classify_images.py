import glob
import os
import shutil

path = './output/csv/'
movement_types = []
all_files = glob.glob(os.path.join(path, "*.csv"))

for files in sorted(all_files):
	nameLen = len(files) - 7
	move_name = files[0:nameLen]
	if move_name not in movement_types:
		movement_types.append(move_name)
		if os.path.exists(move_name):
			shutil.rmtree(move_name)
		os.mkdir(move_name)
	
	newname = move_name+"/"+files[nameLen:len(files)]
	os.rename(files, newname)
	#print("filename:{0}, newpath:{1}\n".format(files, newname)) 





