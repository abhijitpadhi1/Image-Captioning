import torch
import torch.nn as nn
from model.attention import Attention

class DecoderWithAttention(nn.Module):
    def __init__(self, feature_dim, embed_size, hidden_size, vocab_size):
        super().__init__()

        self.attention = Attention(feature_dim, hidden_size)
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTMCell(embed_size + feature_dim, hidden_size)

        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, features, captions):
        B, seq_len = captions.shape

        embeddings = self.embedding(captions)

        h = torch.zeros(B, self.lstm.hidden_size).to(features.device)
        c = torch.zeros(B, self.lstm.hidden_size).to(features.device)

        outputs = []
        alphas = []

        for t in range(seq_len):
            context, alpha = self.attention(features, h)

            lstm_input = torch.cat((embeddings[:, t, :], context), dim=1)

            h, c = self.lstm(lstm_input, (h, c))

            out = self.fc(self.dropout(h))

            outputs.append(out.unsqueeze(1))
            alphas.append(alpha.unsqueeze(1))

        outputs = torch.cat(outputs, dim=1)
        alphas = torch.cat(alphas, dim=1)

        return outputs, alphas