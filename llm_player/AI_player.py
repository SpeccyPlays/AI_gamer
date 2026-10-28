import keyboard
import time
import os
from ollama import chat
import pydirectinput
import json
from ai_window_capture import WindowCapture, get_window_title_dict
from prompts import get_chuckie_egg_prompt, get_chuckie_key_mapping, get_smb_prompt, get_SMB_key_mapping, get_pacman_key_mapping, get_pacman_prompt

#Mario cheat code SXIOPO for infinte lives
#Change below depending on window title
window_titles = get_window_title_dict()
print(get_window_title_dict())
def print_menu(titles):
    for idx, title in window_titles.items():
        print(idx, "-", title)
    print("Select a window to use or type q to exit")
print_menu(window_titles)
valid_choice = False
title = ""

while not valid_choice:
    choice = input("Select a window: ")

    if choice.lower() == "q":
        break
    elif window_titles[int(choice)]:
        title = window_titles[int(choice)]
        valid_choice = True
    else:
        print("Incorrect option")
        print_menu(window_titles)
if not valid_choice:
    raise SystemExit
wincap = WindowCapture(title)
    
key_mappings = get_pacman_key_mapping()

previous_plan = ""
held_key = None
jump_release_time = None
action = None
enemy_pos = None
current_time = time.time()
previous_screenshot = wincap.get_screenshot()
current_screenshot = None

screenshots = []
screenshots.append(previous_screenshot)

while True:
    
    if keyboard.is_pressed("esc"):
        for key in key_mappings.values():
            pydirectinput.keyUp(key)
        print("Stopping...")

        for idx, item in enumerate(screenshots):
            with open (os.path.join("llm_player", f"{idx}.png"), "wb") as file:
                file.write(item)

        break
    if len(screenshots) >= 3:
        screenshots.pop(0)
    if (time.time() - current_time > 0.1):
        current_time = time.time() 
        current_screenshot = wincap.get_screenshot()
        screenshots.append(current_screenshot)
        response = chat(
            model="qwen3.5:0.8b",
            messages=[
                {
                    "role": "user",
                    "content": get_pacman_prompt(previous_plan, action, enemy_pos),
                    "images": screenshots,
                }
            ],
            think=False,
            format={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": list(key_mappings)
                    },
                    "plan" : {
                        "type": "string",
                    },
                    "player_loc" : {
                        "type": "string",
                    },
                    "enemy_pos" : {
                        "type": "string"
                    }
                },
                "required": ["action", "plan", "player_loc", "enemy_pos"]
            }

        )
        print("Ollama call took", time.time() - current_time)
        content = response.message.content
        previous_screenshot = current_screenshot
        if (content is None):
            continue
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            print("Invalid JSON:", repr(content))
            continue

        action = data["action"]
        plan = data["plan"]
        player_loc = data["player_loc"]
        enemy_pos = data["enemy_pos"]
        previous_plan = plan
        print("The plan is", plan) 
        print("The action is", action)
        key = key_mappings[action]
        if action == "JUMP":
            pydirectinput.keyDown(key_mappings["JUMP"])
            jump_release_time = time.time() + 0.5
        elif key != held_key:
            if held_key is not None:
                pydirectinput.keyUp(held_key)
            pydirectinput.press(key)
            held_key = key
