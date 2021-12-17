import pandas as pd
import numpy as np


# remove users if height<100cm or weight<30kg，target weight<10kg，target weight>initial weight
# save result to temp4.csv
f = pd.read_csv('temp3.csv')

index = np.where(f['height'].values < 100, False, True)
f = f[index]

index = np.where(f['weight'].values < 30, False, True)
f = f[index]

index = np.where(f['target_weight'].values < 10, False, True)
f = f[index]

#
index = f['weight'].values >= f['target_weight'].values
f = f[index]

f.to_csv('temp4.csv', index=False)