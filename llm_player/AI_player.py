import keyboard
import time
from ollama import chat
import pydirectinput
import json
from windowcapture import WindowCapture
from llm_player.prompts import get_chuckie_egg_prompt, get_chuckie_key_mapping, get_smb_prompt, get_SMB_key_mapping

#Mario cheat code SXIOPO for infinte lives
#Change below depending on window title
wincap = WindowCapture('Super Mario Bros. + Duck Hunt (U) [!] [NES] - BizHawk')

with open("ollama_test.png", "wb") as f:
    f.write(wincap.get_screenshot())
    
key_mappings = get_SMB_key_mapping()

previous_plan = ""
held_key = None
jump_release_time = None
action = None
enemy_pos = None
current_time = time.time()
previous_screenshot = wincap.get_screenshot()
while True:
    
    if keyboard.is_pressed("esc"):
        for key in key_mappings.values():
            pydirectinput.keyUp(key)
        print("Stopping...")
        break
    if (time.time() - current_time > 0.1):
        current_time = time.time() 
        current_screenshot = wincap.get_screenshot()
        response = chat(
            model="qwen3.5:0.8b",
            messages=[
                {
                    "role": "user",
                    "content": get_smb_prompt(previous_plan, action, enemy_pos),
                    "images": [previous_screenshot, current_screenshot],
                }
            ],
            think=False,
            format={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["LEFT", "RIGHT", "JUMP"]
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
        print("The plan is", plan, " The action is", action, "The player location is", player_loc, "Enemy positions", enemy_pos);
        key = key_mappings[action]
        if action == "JUMP":
            pydirectinput.keyDown(key_mappings["JUMP"])
            jump_release_time = time.time() + 0.5
        elif key != held_key:
            if held_key is not None:
                pydirectinput.keyUp(held_key)
            pydirectinput.keyDown(key)
            held_key = key
