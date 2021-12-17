import os.path as osp

from torch_geometric.data import Dataset, download_url, Data
from torchvision import datasets, transforms
from sklearn.neighbors import KDTree
import pandas as pd
import numpy as np


class KNN_graph(Dataset):
    def __init__(self, node_num, k, root, filename, transform=None, pre_transform=None):
        self.k = k
        self.filename = filename
        self.root = root
        self.node_num = node_num
        super().__init__(root, transform, pre_transform)

    @property
    def raw_file_names(self):
        return []

    @property
    def processed_file_names(self):
        return [self.filename+"_init_"+str(self.k)+".csv"]

    def download(self):
        pass

    def process(self):
        idx = 0
        # node feature csv file
        user_feature_matrix = pd.read_csv("D:/vscode/github/graph_network/data_clean/temp12.csv")

        X = user_feature_matrix.to_numpy()
        X = X[:, 1:]

        node_num = X.shape[0]

        # obtain k nearest neighbors in the histology image (use the euclidian distance)
        tree = KDTree(X)
        dist, ind = tree.query(X, k=self.k)

        # indices of k closest neighbors of each node, the dimension is [node number x k]
        print("knn shape = ", ind.shape)

        # construct graph
        edge_list = []
        for node_id in range(node_num):
            neighbors = ind[node_id]
            edge_list.extend([[node_id, i] for i in neighbors])
            # print(len([[node_id, i] for i in neighbors]))
            # print([[node_id, i] for i in neighbors])
        print(len(edge_list))
        edge_list_arr = np.array(edge_list)
        print("k = ", self.k, "edge_num = ", edge_list_arr.shape[0])

        data = pd.DataFrame(data=edge_list_arr, columns=['node_from', 'node_to'])
        data.to_csv(osp.join(self.processed_dir, self.filename+"_init_"+str(self.k) + ".csv"), index=False)
        # TODO save data
        # data = Data(X1=X1, X2=X2, X3=X3, X4=X4, edge_index=edge_list_tensor, num_nodes=self.k)
        #
        # torch.save(data, osp.join(self.processed_dir, self.filename+"_init_"+str(self.k)+".pt"))

    def len(self):
        return len(self.processed_file_names)

    def get(self, idx):
        data = pd.read_csv(osp.join(self.processed_dir, self.filename+"_init_"+str(self.k)+".csv"))
        # TODO read in data
        return data
