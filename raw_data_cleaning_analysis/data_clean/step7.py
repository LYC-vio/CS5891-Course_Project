import pandas as pd
import numpy as np


# remove users if lastdays < 10
# save result to temp9.csv
f1 = pd.read_csv('temp7.csv')
f2 = pd.read_csv('temp8.csv')
temp = pd.concat([f1, f2], axis=1)
index = np.where(temp['lastdays'] < 10, False, True)
temp = temp[index]
temp.drop('user_id', axis=1, inplace=True)
temp.to_csv('temp9.csv', index=False)