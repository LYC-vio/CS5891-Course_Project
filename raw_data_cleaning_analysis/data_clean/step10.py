import pandas as pd
import numpy as np


# add goal difficulty
# save to temp12.csv
f = pd.read_csv('data_clean/temp11.csv')
diffcult = (f['weight'] - f['target_weight']) / f['weight']
f.drop(['last_record_weight'], axis=1, inplace=True)
f['diffcult'] = diffcult
f = f.round({'diffcult': 3})
f.to_csv('data_clean/temp12.csv', index=False)