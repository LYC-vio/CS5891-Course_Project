import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import random


class GraphAttentionLayer(nn.Module):
	"""
	Simple GAT layer
	"""

	def __init__(self, in_features, out_features, dropout, alpha, concat=True):
		super(GraphAttentionLayer, self).__init__()
		self.dropout = dropout
		self.in_features = in_features
		self.out_features = out_features
		self.alpha = alpha
		self.concat = concat

		# edge wise attention trainable parameter
		self.a1 = nn.Parameter(torch.tensor(random.uniform(0, 1)))
		self.a2 = nn.Parameter(torch.tensor(random.uniform(0, 1)))
		self.a3 = nn.Parameter(torch.tensor(random.uniform(0, 1)))

		self.W = nn.Parameter(torch.empty(size=(in_features, out_features)))
		nn.init.xavier_uniform_(self.W.data, gain=1.414)
		self.a = nn.Parameter(torch.empty(size=(2 * out_features, 1)))
		nn.init.xavier_uniform_(self.a.data, gain=1.414)

		self.leakyrelu = nn.LeakyReLU(self.alpha)

	def forward(self, h, adj):
		Wh = torch.mm(h, self.W)  # h.shape: (N, in_features), Wh.shape: (N, out_features)
		e = self._prepare_attentional_mechanism_input(Wh)

		zero_vec = -9e15 * torch.ones_like(e)
		#
		attention1 = torch.where(adj[:, :, 0] > 0, e, zero_vec)
		attention1 = F.softmax(attention1, dim=1)
		attention1 = F.dropout(attention1, self.dropout, training=self.training)

		attention2 = torch.where(adj[:, :, 1] > 0, e, zero_vec)
		attention2 = F.softmax(attention2, dim=1)
		attention2 = F.dropout(attention2, self.dropout, training=self.training)

		attention3 = torch.where(adj[:, :, 2] > 0, e, zero_vec)
		attention3 = F.softmax(attention3, dim=1)
		attention3 = F.dropout(attention3, self.dropout, training=self.training)

		# attention = F.softmax(attention, dim=1)
		# attention = F.dropout(attention, self.dropout, training=self.training)

		"""
		alpha * attention1 + beta * attention2 + gamma * attention3
		"""
		attention = self.a1 * attention1 + self.a2 * attention2 + self.a3 * attention3

		h_prime = torch.matmul(attention, Wh)

		if self.concat:
			return F.elu(h_prime)
		else:
			return h_prime

	def _prepare_attentional_mechanism_input(self, Wh):
		# Wh.shape (N, out_feature)
		# self.a.shape (2 * out_feature, 1)
		# Wh1&2.shape (N, 1)
		# e.shape (N, N)
		Wh1 = torch.matmul(Wh, self.a[:self.out_features, :])
		Wh2 = torch.matmul(Wh, self.a[self.out_features:, :])
		# broadcast add
		e = Wh1 + Wh2.T
		return self.leakyrelu(e)

	def __repr__(self):
		return self.__class__.__name__ + ' (' + str(self.in_features) + ' -> ' + str(self.out_features) + ')'


class SpecialSpmmFunction(torch.autograd.Function):
	"""Special function for only sparse region backpropataion layer."""

	@staticmethod
	def forward(ctx, indices, values, shape, b):
		assert indices.requires_grad == False
		a = torch.sparse_coo_tensor(indices, values, shape)
		ctx.save_for_backward(a, b)
		ctx.N = shape[0]
		return torch.matmul(a, b)

	@staticmethod
	def backward(ctx, grad_output):
		a, b = ctx.saved_tensors
		grad_values = grad_b = None
		if ctx.needs_input_grad[1]:
			grad_a_dense = grad_output.matmul(b.t())
			edge_idx = a._indices()[0, :] * ctx.N + a._indices()[1, :]
			grad_values = grad_a_dense.view(-1)[edge_idx]
		if ctx.needs_input_grad[3]:
			grad_b = a.t().matmul(grad_output)
		return None, grad_values, None, grad_b


class SpecialSpmm(nn.Module):
	def forward(self, indices, values, shape, b):
		return SpecialSpmmFunction.apply(indices, values, shape, b)


class SpGraphAttentionLayer(nn.Module):
	"""
	Sparse version GAT layer, similar to https://arxiv.org/abs/1710.10903
	"""

	def __init__(self, in_features, out_features, dropout, alpha, concat=True):
		super(SpGraphAttentionLayer, self).__init__()
		self.in_features = in_features
		self.out_features = out_features
		self.alpha = alpha
		self.concat = concat

		self.W = nn.Parameter(torch.zeros(size=(in_features, out_features)))
		nn.init.xavier_normal_(self.W.data, gain=1.414)

		self.a = nn.Parameter(torch.zeros(size=(1, 2 * out_features)))
		nn.init.xavier_normal_(self.a.data, gain=1.414)

		self.dropout = nn.Dropout(dropout)
		self.leakyrelu = nn.LeakyReLU(self.alpha)
		self.special_spmm = SpecialSpmm()

	def forward(self, input, adj):
		dv = 'cuda' if input.is_cuda else 'cpu'

		N = input.size()[0]
		edge = adj.nonzero().t()

		h = torch.mm(input, self.W)
		# h: N x out
		assert not torch.isnan(h).any()

		# Self-attention on the nodes - Shared attention mechanism
		edge_h = torch.cat((h[edge[0, :], :], h[edge[1, :], :]), dim=1).t()
		# edge: 2*D x E

		edge_e = torch.exp(-self.leakyrelu(self.a.mm(edge_h).squeeze()))
		assert not torch.isnan(edge_e).any()
		# edge_e: E

		e_rowsum = self.special_spmm(edge, edge_e, torch.Size([N, N]), torch.ones(size=(N, 1), device=dv))
		# e_rowsum: N x 1

		edge_e = self.dropout(edge_e)
		# edge_e: E

		h_prime = self.special_spmm(edge, edge_e, torch.Size([N, N]), h)
		assert not torch.isnan(h_prime).any()
		# h_prime: N x out

		h_prime = h_prime.div(e_rowsum)
		# h_prime: N x out
		assert not torch.isnan(h_prime).any()

		if self.concat:
			# if this layer is not last layer,
			return F.elu(h_prime)
		else:
			# if this layer is last layer,
			return h_prime

	def __repr__(self):
		return self.__class__.__name__ + ' (' + str(self.in_features) + ' -> ' + str(self.out_features) + ')'