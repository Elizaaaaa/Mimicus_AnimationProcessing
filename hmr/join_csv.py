import os
import glob
import pandas as pd
import gc

path = './output/csv/'
move_types = os.listdir(path)
#TODO: concated_df.index is growing, stop it
for move in move_types:
    move_path = path + move + '/'
    print("Working on {0}: {1}".format(move, move_path))

    all_files = glob.glob(os.path.join(move_path, "*.csv"))

    df_from_each_file = (pd.read_csv(f) for f in sorted(all_files))
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
    print(len(concatenated_df))

    concatenated_df['frame'] = concatenated_df.index+1
    print("The frame number is: {0}".format(concatenated_df.index+1))
    file_name = move_path + "csv_joined.csv"

    if os.path.isfile(file_name):
        print("{0} exist! remove the existing file.\n".format(file_name))
        os.remove(file_name)

    concatenated_df.to_csv(file_name, index=False)


