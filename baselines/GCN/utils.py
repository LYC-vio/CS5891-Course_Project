from torch_geometric.data import Data
import pandas as pd
import torch as th
import numpy as np


def load_data(path_node, path_edge, path_label, train_ratio, test_ratio):
    '''
    path_node: user feature csv path
    path_edge: edge csv path
    path_label: label csv path
    train_ratio: train ratio（0 - 1）
    test_ratio: test ratio（0 - 1）
    '''
    # GPU OOM
    # device = th.device('cuda' if th.cuda.is_available() else 'cpu')
    device = th.device('cpu')

    node_features: pd.DataFrame = pd.read_csv(path_node)
    edges: pd.DataFrame = pd.read_csv(path_edge)
    label: pd.DataFrame = pd.read_csv(path_label)
    x = th.tensor(node_features.values[:, 1:], dtype=th.float32)
    y = label['y'].values
    y = np.where(y > 0.5, 1, 0)
    y = th.tensor(y, dtype=th.int64)
    edge_index = th.tensor(edges.values[:, :2], dtype=th.int64)
    edge_attr = th.tensor(edges.values[:, 2:], dtype=th.float32)
    #
    node_nums = x.shape[0]
    cnt1 = sum(y)
    cnt0 = node_nums - cnt1

    train_mask = np.full(node_nums, False)
    test_mask = np.full(node_nums, False)

    index = np.arange(node_nums, dtype=np.int64)
    index_0_mask = np.where(y < 0.5, True, False)
    index_1_mask = np.where(y > 0.5, True, False)
    #
    index_0 = index[index_0_mask]
    index_1 = index[index_1_mask]

    idx0 = np.random.choice(index_0, size=int(cnt0 * train_ratio), replace=False)
    idx1 = np.random.choice(index_1, size=int(cnt1 * train_ratio), replace=False)
    idx = np.hstack((idx0, idx1))
    train_mask[idx] = True

    idx0 = np.random.choice(index_0, size=int(cnt0 * test_ratio), replace=False)
    idx1 = np.random.choice(index_1, size=int(cnt1 * test_ratio), replace=False)
    idx = np.hstack((idx0, idx1))
    test_mask[idx] = True

    data = Data(x=x, y=y, edge_index=edge_index.t().contiguous(), edge_attr=edge_attr,\
                train_mask=train_mask, test_mask=test_mask)
    data.to(device)
    return data
