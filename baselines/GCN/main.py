from GCNNet import *
from utils import *
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('--hidden_channels', type=int, default=128, help="size of hidden channel for GCN")
# parser.add_argument('--out_channels', type=int, default=64, help="size of out channel for GCN")
# parser.add_argument('--n_layer', type=int, default=3, help="layer number for GCN")
# parser.add_argument('--dropout', type=float, default=0.3, help="dropout")
# parser.add_argument("--learning_rate", type=float, default=0.001, help="learining rate")
# parser.add_argument("--max_epochs", type=int, default=5000, help="max training number")
# parser.add_argument("--tol", type=float, default=1e-3, help="stop criterion for training")
# args = parser.parse_args()
# args.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

if __name__ == '__main__':
    # GPU OOM
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    device = torch.device('cpu')
    data = load_data('./data_clean/temp12.csv', './follow_edge_final.csv', './data_clean/label.csv', 0.01, 0.01)
    print(data)
    print(f'total user number{data.test_mask.sum()}')
    print(f'total user number with label=1: {data.y[data.test_mask].sum()}')
    model = GCN(data.num_node_features, 20, 2).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    model.train()
    for epoch in range(1):
        optimizer.zero_grad()
        out = model(data)
        loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
    model.eval()
    pred = model(data).argmax(dim=1)
    correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
    acc = int(correct) / int(data.test_mask.sum())
    print('Accuracy: {:.4f}'.format(acc))
