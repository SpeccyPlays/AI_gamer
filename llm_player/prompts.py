def get_chuckie_egg_prompt(previous_plan):
    return f"""
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
                    - Platforms are always coloured and never black.

                    Priority:
                    1. Collect all eggs on screen.
                    2. Reach ladders/platforms needed to collect eggs.
                    3. Avoid birds only when they pose an immediate collision risk.
                    4. Do not remain stationary unless there is genuinely no useful action.

                    Ladder rules:
                    - Empty space above the player is NOT a ladder.
                    - Platforms and gaps are NOT ladders.
                    - If you cannot clearly see a ladder alighned with the player, do not choose UP or DOWN.
                    - When trying to use a ladder, first move LEFT or RIGHT until the player is horizontally aligned exactly with the ladder.
                    - If you do not move up a ladder when pressing up, move LEFT or RIGHT a small amount and try again.

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
                    Goomba_pos: an extremely concise description of where you think any birds are on screen

                    Do not output anything else.
                    """
def get_chuckie_key_mapping():
    return {
                "LEFT" : "9", 
                "RIGHT": "0", 
                "UP": "2", 
                "DOWN" : "W", 
                "JUMP" : "M", 
            }

def get_smb_prompt(previous_plan, action, enemy_pos):
    return f"""
                    The player is Mario, wearing a red hat and red overalls.

                        SCREEN INTERPRETATION:
                        The bottom portion of the screen is usually the ground and terrain.
                        Mario's position should be interpreted relative to the terrain, not
                        just relative to the image.
                        Objects that are farther to the RIGHT are generally objects Mario
                        will encounter next.
                        An Goomba on the same platform and to the RIGHT of Mario is usually
                        a threat.
                        An Goomba above Mario or on a different platform is not necessarily
                        an immediate threat.
                        Do not treat decorative background elements as obstacles.

                    Goal: complete the level by moving right.

                    You will receive a series of screen frames, from oldest to newest.

                    Compare the frames carefully.

                    First determine:
                    - Mario's current position.
                    - Whether Mario is moving left, right, or jumping.
                    - Any enemies visible near Mario.
                    - Each Goomba's position relative to Mario.
                    - Whether an Goomba is directly in Mario's path.

                    Then choose the action.

                    IMPORTANT:
                    -Goombas are enemies
                    -If a Goomba is to the RIGHT of Mario, on the same ground/platform, and Mario is moving toward it, the Goomba is directly in Mario's path.
                    -If a Goomba is directly in Mario's path, choose JUMP.
                    -There is control latency so When you see a Goomba, choose JUMP
                    -Mario can avoid enemies by jumping on a question mark block or brick block above the Goomba
                    -Goombas can be killed by jumping on top of them or landing on top of them from a higher level
                    -Goombas can move from right to left, or left to right so may move towards Mario
                    
                    Clouds, bushes, and hills are NOT Goombas or obstacles

                    Green pipes are obstacles and MUST be jumped over. They are NOT Goombas
                    Question mark blocks and brick blocks are obstacles but can be moved under or jumped on.
                    Question mark blocks and brick blocks are NOT Goombas

                    When falling, you CANNOT jump

                    CONTROL LATENCY:
                    -There is about a 1.5 second delay between you choosing an action and the action being performed
                    -Take this in to account when planning next action

                    Mario also has momentum so does not instantly change direction
                    Mario jumps in an arc in the direction he is travelling

                    Otherwise:
                    - If the path ahead is clear, choose RIGHT.
                    - If there is a gap or obstacle ahead, choose JUMP.
                    - Choose LEFT only to avoid immediate danger. Otherwise, you should be moving RIGHT as much as possible
                    - If Mario is no longer moving right he may be stuck behind something. choose JUMP

                    Actions:
                    - RIGHT: move right.
                    - LEFT: move left.
                    - JUMP: jump.

                    Previous plan: {previous_plan}
                    Previous action: {action}
                    Previous enemy (Goomba) positions: {enemy_pos}

                    Return JSON with exactly these two fields:
                    action: one of LEFT, RIGHT, JUMP
                    plan: an extremely concise description of your immediate goal
                    player_loc: extremely concise position of Mario
                    enemy_pos: describe Goomba position relative to Mario

                    Do not output anything else.
                    """
def get_SMB_key_mapping():
    return {
                "LEFT" : "o", 
                "RIGHT": "p", 
                "JUMP" : "m", 
            }

def get_pacman_prompt(previous_plan, action, enemy_pos):
    return f"""


                    Goal: 
                    Complete the level by navigating through the maze collecting small yellow pills and avoiding enemies.
                    The level is complete when all pills collected
                    There are larger pills called power pills which can also be collected.

                    Enemies: 
                    Enemies are ghosts which chase Pacman around the maze. They should be avoided but should not hamper pill collection.

                    You will receive a series of images to help decide your actions.
                    The images will be in order of oldest to newest

                    Image INTERPRETATION:

                    The left 3 quarters of the screen shows the maze.
                    Pacman is the yellow circle within the maze.
                    Enemies are shaped liked ghosts and spawn from the center of the maze.
                    The maze is blue walls and pacman cannot pass through them.
                    The right side third of the screen is a HUD and can be ignored.

                    Compare the images carefully.

                    First determine:
                    - Pacman's current position.
                    - Whether Pacman is moving left, right, up, or down.
                    - Any enemies visible near pacmans.
                    - Each enemies's position relative to enemies.

                    Then choose the action.

                    IMPORTANT:
                    - If pacman does not appear to move between images then he is blocked by a maze wall. 
                    - If blocked choose a different direction and note in your plan that Pacman is blocked by a wall.


                    CONTROL LATENCY:
                    - There is about a 1.5 second delay between you choosing an action and the action being performed
                    - Take this in to account when planning next action

                    Actions:
                    - RIGHT: move right.
                    - LEFT: move left.
                    - UP: move up.
                    - DOWN: move down.

                    Previous plan: {previous_plan}
                    Previous action: {action}
                    Previous enemy positions: {enemy_pos}

                    Return JSON with exactly these two fields:
                    action: one of LEFT, RIGHT, UP, DOWN
                    plan: an extremely concise description of your immediate goal
                    player_loc: extremely concise position of Pacman
                    enemy_pos: describe enemy positions relative to Pacman

                    Do not output anything else.
                    """
def get_pacman_key_mapping():
    return {
                "LEFT" : "o", 
                "RIGHT": "p", 
                "UP" : "q", 
                "DOWN" : "a"
            }