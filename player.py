import keyboard
from ollama import chat
import json
import pydirectinput
from windowcapture import WindowCapture

wincap = WindowCapture('Fuse')

while True:
    if keyboard.is_pressed("esc"):
        print("Stopping...")
        break

    response = chat(
        model="qwen3.5:2b",
        messages=[
            {
                "role": "user",
                "content": """
    Look at this Chuckie Egg game screenshot.
    Chuckie Egg is a platforming games where you need to collect the eggs by moving the player over them before the time runs out while avoiding being touched by the hens as this kills the player.
    Choose the next action. You may only choose:
    LEFT, RIGHT, UP, DOWN, FIRE, NONE
    Return ONLY the action. Do not explain your answer.
    """,
                "images": [wincap.get_screenshot()],
            }
        ],
        think=False,
        format={
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["LEFT", "RIGHT", "UP", "DOWN", "FIRE", "NONE"]
                }
            },
            "required": ["action"]
        }

    )
    print("Ollama responded")

    print(response.message.content)