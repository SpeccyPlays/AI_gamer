import keyboard
import time
from ollama import chat
import pydirectinput
import json
from windowcapture import WindowCapture

wincap = WindowCapture('Fuse')

key_mappings = {
    "LEFT" : "9", 
    "RIGHT": "0", 
    "UP": "2", 
    "DOWN" : "W", 
    "JUMP" : "M", 
}

previous_plan = ""
held_key = None
current_time = time.time()
while True:
    
    if keyboard.is_pressed("esc"):
        if held_key is not None:
            pydirectinput.keyUp(held_key)
            print("Stopping...")
            break

    if (time.time() - current_time > 0.5  ):
        current_time = time.time() 
        response = chat(
            model="ministral-3:3b",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    You are controlling the player in Chuckie Egg.

                    Look at the screenshot and choose the single best action to make progress toward collecting eggs.
                    The player is the small yellow character.
                    First identify the player's exact position in the screenshot.
                    Base your action on the player's current position, not on the position of eggs or birds.
                    Rules:
                    - LEFT and RIGHT move horizontally.
                    - UP and DOWN use ladders when the player is aligned with one.
                    - JUMP jumps over obstacles.
                    - Avoid blue birds, but do not let them prevent progress.
                    - Collect eggs even if this requires passing near a bird.
                    - Prioritize collecting eggs and reaching the next platform.
                    - Only avoid a bird if the player is directly in its path.

                    Priority:
                    1. Collect eggs.
                    2. Reach ladders/platforms needed to collect eggs.
                    3. Avoid birds only when they pose an immediate collision risk.
                    4. Do not remain stationary unless there is genuinely no useful action.

                    Ladder rules:
                    - Only choose UP or DOWN if you can clearly see a ladder directly connected to the player's current position.
                    - Empty space above the player is NOT a ladder.
                    - Platforms and gaps are NOT ladders.
                    - If you cannot clearly see a ladder, do not choose UP or DOWN.
                    - When trying to use a ladder, first move LEFT or RIGHT until the player is horizontally aligned with the ladder.

                    Previous plan: {previous_plan}

                    Choose exactly ONE action:
                    LEFT
                    RIGHT
                    UP
                    DOWN
                    JUMP
                    NONE

                    Return JSON with exactly these two fields:
                    action: one of LEFT, RIGHT, UP, DOWN, JUMP, NONE
                    plan: an extremely concise description of your immediate goal
                    player_loc: an extremely concise description of where you think the player is on screen

                    Do not output anything else.
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
                        "enum": ["LEFT", "RIGHT", "UP", "DOWN", "JUMP", "NONE"]
                    },
                    "plan" : {
                        "type": "string",
                    },
                    "player_loc" : {
                        "type": "string",
                    }
                },
                "required": ["action", "plan", "player_loc"]
            }

        )
        content = response.message.content
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
        previous_plan = plan
        print("The plan is ", plan);
        print("The action is ", action)
        print("The player location is", player_loc)
        if (action == "NONE" or action not in key_mappings):
            if action == "NONE" or action not in key_mappings:
                if held_key is not None:
                    pydirectinput.keyUp(held_key)
                    held_key = None
                continue
            continue
        key = key_mappings[action]
        if key != held_key:
            if held_key is not None:
                pydirectinput.keyUp(held_key)
            pydirectinput.keyDown(key)
            held_key = key
        print("Key is", key)
