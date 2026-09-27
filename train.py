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
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split

from test_dataset import MarioDataset
from model import MarioCNN


# Load our recorded Mario gameplay
dataset = MarioDataset("saved_actions/2026-09-2714_56_46save.json")


train_size = int(0.8 * len(dataset))
validation_size = len(dataset) - train_size

train_dataset, validation_dataset = random_split(
    dataset,
    [train_size, validation_size]
)

# Split the dataset into batches
train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)

# Create the CNN
model = MarioCNN()

# Loss function - add weight for jumping
loss_function = nn.CrossEntropyLoss(weight=torch.tensor([1.0, 1.0, 1.0, 6.0]))

# Optimizer
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

epochs = 10

for epoch in range(epochs):

    total_loss = 0

    for images, actions in train_loader:

        predictions = model(images)

        loss = loss_function(predictions, actions)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    average_loss = total_loss / len(train_loader)

    print(f"Epoch {epoch + 1}/{epochs}, Loss: {average_loss:.4f}")

model.eval()

validation_loss = 0
correct = 0
total = 0

confusion_matrix = torch.zeros(4, 4, dtype=torch.int64)

# Split the dataset into batches
validation_loader = DataLoader(
    validation_dataset,
    batch_size=32,
    shuffle=False
)

with torch.no_grad():

    for images, actions in validation_loader:

        predictions = model(images)

        loss = loss_function(predictions, actions)

        validation_loss += loss.item()

        predicted_actions = predictions.argmax(dim=1)

        correct += (predicted_actions == actions).sum().item()
        total += actions.size(0)

        for actual, predicted in zip(actions, predicted_actions):
            confusion_matrix[actual, predicted] += 1

validation_loss /= len(validation_loader)

print(f"Validation Loss: {validation_loss:.4f}")

accuracy = correct / total

print(f"Validation Accuracy: {accuracy:.2%}")

print("\nConfusion Matrix:")
print(confusion_matrix)

print("\nRows = Actual")
print("Columns = Predicted")
print("Order = NONE, LEFT, RIGHT, JUMP")

torch.save(model.state_dict(), "mario_model.pth")