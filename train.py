"""
train.py

PURPOSE:
Trains Mario's neural network using our recorded gameplay.

TRAINING PROCESS:

1. Load the MarioDataset.
2. DataLoader groups screenshots into batches.
3. Send each batch of screenshots into MarioCNN.
4. CNN predicts an action for each screenshot.
5. Compare the predictions against the human-recorded actions.
6. Calculate how wrong the predictions are (loss).
7. Adjust the CNN's weights to reduce the loss.
8. Repeat this process many times.

The goal is for the CNN to learn:

    Screenshot of Mario
            ↓
    What would I have done?
            ↓
    NONE / LEFT / RIGHT / JUMP

Once trained, the model can take a new screenshot
and predict which action Mario should perform.
"""

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