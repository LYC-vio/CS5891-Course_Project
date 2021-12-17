import pandas as pd
import numpy as np

# encode gender as 0/1 vector
# temp7 = temp6 + encoded gender
# temp8 has user id, AvgPost, AvgComment, AvgMention, lastdays, age
f = pd.read_csv('temp6.csv')
a = np.where(f['gendar'] == 1, 1, 0)
b = np.where(f['gendar'] == 2, 1, 0)
f['man'] = a
f['women'] = b
f.drop(['gendar'], axis=1, inplace=True)
f.to_csv('temp7.csv', index=False)

path1 = r"D:\BaiduNetdiskDownload\WeightLoss\userprofile.csv"
f1 = pd.read_csv(path1, na_values=['$null$'])
f1.set_index('user_id', inplace=True)
temp = f1.loc[f['id'].values, ['AvgPost', 'AvgComment', 'AvgMention', 'lastdays', 'age']]
temp.to_csv('temp8.csv', index=True)
