from base_player import BasePlayer

class pacman_player:
    def get_prompt(self, previous_plan, action, enemy_pos):
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

    def get_key_mapping(self):
        return {
            "LEFT" : "o", 
            "RIGHT": "p", 
            "UP" : "q", 
            "DOWN" : "a"
        }