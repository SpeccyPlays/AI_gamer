import io
import torch
import keyboard
import time
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

action_to_key = {
    "LEFT": "o",
    "RIGHT": "p",
    "JUMP": "m"
}

capture = WindowCapture(
    "Super Mario Bros. + Duck Hunt (U) [!] [NES] - BizHawk"
)

for i in range(3):
    print(f"Starting in {i+1}")
    time.sleep(1.0)

print("Playing")
while True:

    if keyboard.is_pressed("esc"):
        print("Stopping...")
        break

    screenshot = capture.get_screenshot()

    image = Image.open(io.BytesIO(screenshot)).convert("RGB")
    image = transform(image)
    image = torch.tensor(
        np.array(image),
        dtype=torch.float32
    ).permute(2, 0, 1) / 255.0

    image = image.unsqueeze(0)

    with torch.no_grad():
        predictions = model(image)

    probabilities = torch.softmax(predictions, dim=1)[0]

    predicted_id = predictions.argmax(dim=1).item()
    predicted_action = id_to_action[predicted_id]

    predicted_id = predictions.argmax(dim=1).item()
    predicted_action = id_to_action[predicted_id]

    if predicted_action in action_to_key:
        keyboard.press(action_to_key[predicted_action])

    print("\033[2J\033[H", end="")

    for i, probability in enumerate(probabilities):
        print(f"{id_to_action[i]}: {probability:.2%}")

    time.sleep(0.2)