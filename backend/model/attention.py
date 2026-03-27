import torch
import torch.nn as nn

class Attention(nn.Module):
    def __init__(self, feature_dim, hidden_dim):
        super().__init__()

        self.attn = nn.Linear(feature_dim + hidden_dim, hidden_dim)
        self.v = nn.Linear(hidden_dim, 1)

    def forward(self, features, hidden):
        B, num_regions, feature_dim = features.shape

        hidden = hidden.unsqueeze(1).repeat(1, num_regions, 1)

        energy = torch.tanh(self.attn(torch.cat((features, hidden), dim=2)))
        attention = self.v(energy).squeeze(2)

        alpha = torch.softmax(attention, dim=1)
        context = (features * alpha.unsqueeze(2)).sum(dim=1)

        return context, alpha