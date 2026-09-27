import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from test_dataset import MarioDataset
from model import MarioCNN

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from test_dataset import MarioDataset
from model import MarioCNN


dataset = MarioDataset("saved_actions/2026-09-2714_56_46save.json")

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True
)

model = MarioCNN()