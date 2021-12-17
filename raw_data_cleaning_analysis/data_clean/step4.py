import pandas as pd
import numpy as np

f = pd.read_csv('temp4.csv')

# calculate bmi(use height and width) and remove users if bmi<18.5
# save result in file "temp5.csv"
bmi = f['weight'].values / (f['height'].values / 100) ** 2
f['bmi'] = bmi
index = np.where(f['bmi'].values < 18.5, False, True)
f = f[index]
f = f.round({'bmi': 1})
f.to_csv('temp5.csv', index=False)