"""
model.py

PURPOSE:
Defines Mario's neural network (CNN).

INPUT:
A 128x128 RGB screenshot.

Input shape:
    [3, 128, 128]

The CNN processes the screenshot through:
    - Convolutional layers
    - ReLU activation
    - Max pooling
    - Linear layers

OUTPUT:
4 numbers representing the model's prediction for each action:

    0 = NONE
    1 = LEFT
    2 = RIGHT
    3 = JUMP

The model starts with random weights.
Training will adjust those weights so the predictions
become better at matching our recorded gameplay.
"""

import torch.nn as nn

class MarioCNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Flatten(),

            nn.Linear(64 * 16 * 16, 128),
            nn.ReLU(),

            nn.Linear(128, 4)
        )

    def forward(self, x):
        return self.network(x)
