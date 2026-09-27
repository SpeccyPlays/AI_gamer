import io
import torch
from PIL import Image
from torchvision import transforms

from model import MarioCNN
from windowcapture import WindowCapture

import numpy as np

model = MarioCNN()
model.load_state_dict(torch.load("mario_model.pth"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((128, 128)),
])

id_to_action = {
    0: "NONE",
    1: "LEFT",
    2: "RIGHT",
    3: "JUMP"
}

capture = WindowCapture(
    "Super Mario Bros. + Duck Hunt (U) [!] [NES] - BizHawk"
)

png_bytes = capture.get_screenshot()

image = Image.open(io.BytesIO(png_bytes)).convert("RGB")

image = transform(image)

image = torch.tensor(
    np.array(image),
    dtype=torch.float32
).permute(2, 0, 1) / 255.0

image = image.unsqueeze(0)

with torch.no_grad():
    predictions = model(image)

predicted_id = predictions.argmax(dim=1).item()

print("Prediction:", id_to_action[predicted_id])