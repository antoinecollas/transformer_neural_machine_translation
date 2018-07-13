import numpy as np
import math
import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from layers import MultiHeadAttention, PositionWiseFeedForward, get_mask

# torch.manual_seed(1)

class Encoder(nn.Module):
    def __init__(self, n_layers=6, nb_heads=8, d_model=512, n_neurons = 2048, dropout=0.1):
        super(Encoder, self).__init__()
        self.n_layers = n_layers
        self.MultiHeadAttention = [MultiHeadAttention(nb_heads, d_model, dropout) for _ in range(self.n_layers)]
        self.PositionWiseFeedForward = [PositionWiseFeedForward(d_model, n_neurons, dropout) for _ in range(self.n_layers)]

    def forward(self, X, mask=None):
        '''
        Arg:
            tensor(nb_texts, nb_tokens, d_model(=size of one token))
        Output:
            tensor(nb_texts, nb_tokens, d_model(=size of one token))
        '''
        output = X
        for i in range(self.n_layers):
            output = self.MultiHeadAttention[i].forward(output,output,output,mask)
            output = self.PositionWiseFeedForward[i].forward(output)
        return output

