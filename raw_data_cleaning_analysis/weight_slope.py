import pandas as pd
import numpy as np
from tqdm import tqdm


RATE = 0.1

#
path = r"D:\BaiduNetdiskDownload\WeightLoss\weight_record_consolidated.csv"
f = pd.read_csv(path, nrows=10000)
fg = f.groupby('user_id')

nweight_record = pd.DataFrame(data=[], columns=['user_id', 'weight', 'record_on', 'date'])
record = []
user = pd.DataFrame(data=[], columns=['user_id', 'last_record_weight'])

for index, g in tqdm(fg):
    gn = g.values

    # remove users with only 1 record
    if gn.size == 4:
        continue
    # skip if there are missing values
    try:
        a = gn[:-1, 1].astype("float64")
        b = gn[1:, 1].astype("float64")
        c = gn[:-1, 2].astype('M8[D]').astype("int32")
        d = gn[1:, 2].astype('M8[D]').astype("int32")
    except Exception:
        continue
    # get the slope of weight loss tendency. normally, this should not exceed 2-3kg per day
    # filter
    x = d - c
    y = np.abs(b - a)
    k = y / x
    res = np.where(k >= 3, 1, 0)
    # if the ratio of unreasonable data is too much, we just discard the user
    rate = np.sum(res) / (res.size + 1)
    if rate >= RATE:
        continue
    # save the data if all sanity tests been passed
    record.append(g)
    user.loc[index] = [gn[0][0], gn[-1][1]]

nweight_record = pd.concat(record, axis=0, ignore_index=True)
nweight_record.to_csv('weight_record_1.csv', index=False)
user.to_csv('user_1.csv', index=False)