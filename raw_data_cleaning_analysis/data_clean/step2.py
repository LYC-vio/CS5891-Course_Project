import pandas as pd
import numpy as np


# combine temp1.csv and temp2.csv and remove users if have any missing values
# save result to temp3.csv
f1 = pd.read_csv('temp1.csv', na_values=['$null$'])
f2 = pd.read_csv('temp2.csv', na_values=['$null$'])
f3 = pd.concat([f2, f1.loc[:, ['last_record_weight']]], axis=1)

clean = f3.dropna()
clean.to_csv('temp3.csv', index=False)