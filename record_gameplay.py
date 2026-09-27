import keyboard
import time
import json
from windowcapture import WindowCapture

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

while True:

    if keyboard.is_pressed("esc"):
        print("Stopping...")
        break

    jump_pressed = keyboard.is_pressed("m")

    # Capture immediately when JUMP is newly pressed
    if jump_pressed and not jump_was_pressed:

        timestamp = time.strftime("%Y-%m-%d%H_%M_%S")
        file_name = f"screenshots/{timestamp}screenshoot{frame_count}.png"

        try:
            with open(file_name, "wb") as f:
                f.write(wincap.get_screenshot())

            action_list.append({
                "id": frame_count,
                "screenshot": file_name,
                "action": "JUMP"
            })

            frame_count += 1

        except:
            print("Error saving file", file_name)

    jump_was_pressed = jump_pressed

    # Normal 0.1 second recording
    if time.time() - current_time > 0.1:

        current_time = time.time()

        timestamp = time.strftime("%Y-%m-%d%H_%M_%S")
        file_name = f"screenshots/{timestamp}screenshoot{frame_count}.png"

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

save_timestamp = time.strftime("%Y-%m-%d%H_%M_%S")
save_file_name = f"saved_actions/{save_timestamp}save.json"
with open(save_file_name , "w") as f:
    json.dump(action_list, f, indent=4)