import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv


class GCN(torch.nn.Module):
    def __init__(self, features, hidden, classes) -> None:
        super().__init__()
        self.gcn1 = GCNConv(features, hidden, add_self_loops = False)
        self.gcn2 = GCNConv(hidden, classes, add_self_loops = False)
    
    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.gcn1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.gcn2(x, edge_index)

        return F.log_softmax(x, dim=1)
