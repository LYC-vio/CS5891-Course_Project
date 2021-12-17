import pandas as pd
import numpy as np


# label assigning save to label.csv
# result saved to temp10.csv
f = pd.read_csv('temp9.csv')
label = pd.DataFrame(data=[])
y = np.where(f['last_record_weight'] <= f['target_weight'], 1, 0)
label['y'] = y
label.to_csv('label.csv', index=False)
f.drop('last_record_weight', axis=1, inplace=True)
f.to_csv('temp10.csv', index=False)