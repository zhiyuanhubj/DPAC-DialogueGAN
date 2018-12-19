import torch
import torch.autograd as autograd
import torch.nn as nn
import pdb
import numpy as np
import sys


class Discriminator(nn.Module):

    def __init__(self, embedding_dim, hidden_dim, vocab_size, max_seq_len, dropout=0.2, device="cpu"):
        super(Discriminator, self).__init__()
        self.hidden_dim = hidden_dim
        self.embedding_dim = embedding_dim
        self.max_seq_len = max_seq_len
        self.vocab_size = vocab_size
        self.device = device

        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.gru = nn.GRU(embedding_dim, hidden_dim, num_layers=2, bidirectional=False)
        self.dropout = nn.Dropout(p=dropout)
        self.hidden2out = nn.Linear(hidden_dim, vocab_size)


    def init_hidden(self, batch_size):
        h = autograd.Variable(torch.zeros(2*1, batch_size, self.hidden_dim))
        return h.to(self.device)

    def forward(self, input, hidden):
        embedding = self.embeddings(input.to(self.device)) # batchsize x embedding dim
        embedding = embedding.permute(1, 0, 2)
        out, hidden = self.gru(embedding, hidden)
        out = out[-1,:,:] # Take the output for the last token
        out = torch.tanh(out)
        out = self.dropout(out)
        out = self.hidden2out(out)
        out = torch.softmax(out, dim=1)
        return out.squeeze()

    def batchClassify(self, input):
        """
        Classifies a batch of sequences.

        Inputs: inp
            - inp: batch_size x seq_len

        Returns: out
            - out: batch_size ([0,1] score)
        """

        h_response = self.init_hidden(input.size()[0])
        output = self.forward(input.long(), h_response)
        return output

    def batchBCELoss(self, inp, target):
        """
        Returns Binary Cross Entropy Loss for discriminator.

         Inputs: inp, target
            - inp: batch_size x seq_len
            - target: batch_size (binary 1/0)
        """

        loss_fn = nn.BCELoss()
        h = self.init_hidden(inp.size()[0])
        out = self.forward(inp, h)
        return loss_fn(out, target)

    def get_rewards(self, reply, ignore_index):
        batch_size, max_seq_len = reply.shape
        # criterion = nn.CrossEntropyLoss(reduction="none", ignore_index=ignore_index)
        rewards = torch.zeros(batch_size, max_seq_len-1)

        for t in range(max_seq_len-1): ## CANNOT PREDICT NEXT WORD FOR LAST ONE
            inp = reply[np.arange(batch_size), :t+1]
            target = reply[np.arange(batch_size), t+1]

            vocab_distr = self.batchClassify(inp.long())
            reward = vocab_distr.gather(1, target.type(torch.LongTensor).unsqueeze(1).to(self.device))

            mask = torch.zeros(batch_size)
            for i in range(batch_size):
                if target[i].item() != ignore_index:
                    mask[i] = 1.0
                else:
                    break

            # rewards[:, t] = -criterion(output, target.long().to(self.device))
            rewards[:, t] = torch.log(reward.squeeze() + 1e-12) * mask.to(self.device)
        return rewards

    def get_reward(self, history, word):
        """
        Calculate reward for a new word based on the history
        """
        output = self.batchClassify(history.long())
        reward = output.gather(1, word.type(torch.LongTensor).unsqueeze(1).to(self.device))
        reward = torch.log(reward.squeeze() + 1e-12) # prevent taking the log of zero
        return reward
