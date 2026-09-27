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

