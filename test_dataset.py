"""
test_dataset.py

PURPOSE:
Loads our recorded Mario gameplay data and prepares it for PyTorch.

WHAT IT DOES:
1. Loads the JSON file containing screenshots and actions.
2. Converts action names into numbers:
       NONE  = 0
       LEFT  = 1
       RIGHT = 2
       JUMP  = 3
3. Loads each screenshot.
4. Resizes screenshots to 128x128.
5. Converts images into PyTorch tensors.
6. Changes image format from:
       [height, width, channels]
   to:
       [channels, height, width]
7. Changes pixel values from 0-255 to 0-1.
8. Returns:
       image + action

DataLoader then groups these examples into batches of 32.
"""

import json
from PIL import Image
import torch
from torch.utils.data import Dataset
import numpy as np
from torchvision import transforms
from torch.utils.data import DataLoader



class MarioDataset(Dataset):
    def __init__(self, json_file):
        with open(json_file, "r") as f:
            self.data = json.load(f)

        self.action_to_id = {
            "NONE": 0,
            "LEFT": 1,
            "RIGHT": 2,
            "JUMP": 3
        }
        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
        ])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        item = self.data[index]

        image = Image.open(item["screenshot"]).convert("RGB")
        image = self.transform(image)
        #Changes from height width channels to channels height width and changes pixel to be between 0-1 for ease of training
        image = torch.tensor(np.array(image), dtype=torch.float32).permute(2, 0, 1) / 255.0

        action = self.action_to_id[item["action"]]

        return image, action

