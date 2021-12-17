import pandas as pd
import numpy as np

# result saved to temp1.csv and temp2.csv
path1 = r'D:\vscode\github\graph_network\user_reserved_regression.csv'  # user record data after removing outliers
path2 = r"D:\BaiduNetdiskDownload\WeightLoss\users_consolidated.csv"  # original user feature file
f1 = pd.read_csv(path1, dtype = {'user_id': np.int64})
f1.set_index('user_id', inplace=True)
f2 = pd.read_csv(path2, na_values = {'$null$'}, dtype={'id': np.int64})
f2.set_index('id', inplace=True)

index = np.intersect1d(f1.index, f2.index)
temp1 = f1.loc[index, ['last_record_weight']]
temp1.to_csv('temp1.csv', index=True)
temp2 = f2.loc[index, ['gendar', 'height', 'weight', 'target_weight', 'bmi']]
temp2.to_csv('temp2.csv', na_rep='$null$', index=True)