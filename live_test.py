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
model.load_state_dict(torch.load("mario_mega_model.pth"))
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

jump_release_time = None

capture = WindowCapture(
    "Super Mario Bros. + Duck Hunt (U) [!] [NES] - BizHawk"
)

for i in range(3):
    print(f"Starting in {i+1}")
    time.sleep(1.0)

current_key = None

print("Playing")

while True:

    if keyboard.is_pressed("esc"):
        print("Stopping...")
        break
    if (jump_release_time is not None and time.time() - jump_release_time > 1.0):
        keyboard.release(action_to_key["JUMP"])
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

    new_key = action_to_key.get(predicted_action)

    if predicted_action == "JUMP":
        jump_release_time = time.time()
        keyboard.press(action_to_key["JUMP"])

    elif new_key != current_key:

        if current_key is not None:
            keyboard.release(current_key)

        if new_key is not None:
            keyboard.press(new_key)

        current_key = new_key

    print("\033[2J\033[H", end="")

    for i, probability in enumerate(probabilities):
        print(f"{id_to_action[i]}: {probability:.2%}")

    time.sleep(0.2)

for key in action_to_key.values():
    keyboard.release(key)