import pandas as pd
import numpy as np


# 制作滑动标签，按照25%，50%，75%，100%的比例制作
# 同时发现前面清洗时保留了f['weight'] == f['target_weight']的用户，这里给予清除
# 结果保存在temp11中

# 最终结果
# 范围             用户个数       比例
# (-00, 0.25]      1024561        0.756
# (0.25, 0.5]      216167         0.159
# (0.5, 0.75]      77287          0.057
# (0.75, +00)      37890          0.028
# total            1355905        1
# 结果保存在label中
f = pd.read_csv('data_clean\\temp9.csv')
index = np.where(f['weight'] == f['target_weight'], False, True)
f = f[index]
f.to_csv('temp11.csv', index = False)
a = (f['weight'] - f['last_record_weight']) / (f['weight'] - f['target_weight'])
y = np.array([10000] * a.size)
index = np.where(a > 0.75, True, False)
y[index] = 3
t1 = sum(index)
print(t1)
index = np.where((0.5 < a) & (a <= 0.75), True, False)
y[index] = 2
t2 = sum(index)
print(t2)
index = np.where((0.25 < a) & (a <= 0.5), True, False)
y[index] = 1
t3 = sum(index)
print(t3)
index = np.where(a <= 0.25, True, False)
y[index] = 0
t4 = sum(index)
print(t4)
label = pd.DataFrame(data=[])
print(t1 + t2 + t3 + t4)
print(y.shape)
label['y'] = y
label['y'] = label['y'].astype(np.int16)
label.to_csv('label.csv', index=False)

