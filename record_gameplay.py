import keyboard
import time
import json
from windowcapture import WindowCapture
import os
import sys

os.makedirs("training_data", exist_ok=True)

print("Enter a session name:")
session_name = input()

duplicate_name = os.path.isdir(f"training_data/{session_name}")

if duplicate_name :
    while duplicate_name:
        print("Duplicate session name. Enter a new one or type QUIT to abort:")
        session_name = input()
        if session_name == "QUIT":
            sys.exit("User quit session")
        duplicate_name = os.path.isdir(f"training_data/{session_name}")

os.makedirs(f"training_data/{session_name}")
#Mario cheat code SXIOPO for infinte lives
#Change below depending on window title
wincap = WindowCapture('Super Mario Bros. + Duck Hunt (U) [!] [NES] - BizHawk')

current_time = time.time()

frame_count = 0
action_list = []
jump_was_pressed = False

key_mappings = {
                "o" : "LEFT",
                "p" : "RIGHT", 
                "m" : "JUMP", 
            }
for i in range(3):
    print(f"Starting in {i+1}")
    time.sleep(1.0)

print("Starting recording")

while True:

    if keyboard.is_pressed("esc"):
        print("Stopping...")
        break

    jump_pressed = keyboard.is_pressed("m")

    # Capture immediately when JUMP is newly pressed
    if jump_pressed and not jump_was_pressed:

        file_name = f"training_data/{session_name}/frame_{frame_count:06d}.png"

        try:
            with open(file_name, "wb") as f:
                f.write(wincap.get_screenshot())

            action_list.append({
                "id": frame_count,
                "screenshot": f"frame_{frame_count:06d}.png",
                "action": "JUMP"
            })

            frame_count += 1

        except:
            print("Error saving file", file_name)

    jump_was_pressed = jump_pressed

    # Normal 0.1 second recording
    if time.time() - current_time > 0.1:

        current_time = time.time()

        file_name = f"training_data/{session_name}/frame_{frame_count:06d}.png"

        try:
            with open(file_name, "wb") as f:
                f.write(wincap.get_screenshot())
        except:
            print("Error saving file", file_name)

        action = "NONE"

        for key, mapped_action in key_mappings.items():
            if keyboard.is_pressed(key):
                action = mapped_action
                break

        action_list.append({
            "id": frame_count,
            "screenshot": file_name,
            "action": action
        })

        frame_count += 1

save_file_name = f"training_data/{session_name}/actions.json"
with open(save_file_name , "w") as f:
    json.dump(action_list, f, indent=4)