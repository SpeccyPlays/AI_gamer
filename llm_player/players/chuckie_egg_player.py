from base_player import BasePlayer

class Chuckie_egg_player:
    def get_prompt(self, previous_plan, action, enemy_pos):
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

    def get_key_mapping(self):
        return {
            "LEFT" : "9", 
            "RIGHT": "0", 
            "UP": "2", 
            "DOWN" : "W", 
            "JUMP" : "M", 
        }