import os
import pandas as pd
import scipy.signal as signal

path = 'hmr/output/csv/'
move_types = os.listdir(path)
for move in move_types:
    filename = path + move + '/csv_joined.csv'
    df = pd.read_csv(filename)

    for x in range(df.shape[1]):
        if x == 0:
            continue
        data = pd.read_csv(filename, usecols=[x])
        y = data.values.ravel()

        N = 1
        Wn = 0.3
        B, A = signal.butter(N, Wn, output='ba')
        fy = signal.filtfilt(B,A,y)
        df.replace(df[data.columns].values, fy, inplace=True)

    df.to_csv(filename, index=False)
