import pandas as pd
import numpy as np


# remove gender != 0 or 1
# save result to "temp6.csv"
f = pd.read_csv('temp5.csv')
f['gendar'] = f['gendar'].astype(np.int16)
index = np.where(f['gendar'] == 0, False, True)
f.to_csv('temp6.csv', index=False)