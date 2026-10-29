from base_player import BasePlayer

class SuperMario(BasePlayer):

    def get_prompt(self, previous_plan, action, enemy_pos):
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
                            
                            Clouds, bushes, and hills are NOT Goombas or obstacles. You DO NOT need to avoid them.
        
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

    def get_key_mapping(self):
        return {
            "LEFT" : "o", 
            "RIGHT": "p", 
            "JUMP" : "m", 
        }