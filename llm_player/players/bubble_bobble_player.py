from base_player import BasePlayer

class BubbleBobble():

    def get_prompt(self, previous_plan, action, enemy_pos):
        return '''
            You are controlling the player in Bubble Bobble.
            The player is a green dinosaur that starts at the bottom of the screen.
            The player character has eyes which point in the direction is is facing.
            The aim of the game is to capure the enemies in a bubble then jump on them to kill them.
            They will then drop an object you can collect and a new level will start.
            You can jump on the platforms and any gaps in the platform will let you fall down.
            You can move left and right when falling.
            The bubble you fire is a green circle.
            When an enemy is captured in a bubble, the bubble will have them in the middle and be more green.
            You can and should run in to the enemy when they are in a bubble.
            The bubbles you fire have limited range.

            IMPORTANT:
            -If the enemy is not in a bubble then they can kill you if they touch the player character. Avoid this.
            -You HAVE to be facing the enemy to FIRE in their direction.
            -You can jump to avoid an enemy to the left or right of you.
            -There is around 1 second lag between actions so take action to avoid or capture enemies sooner.
            -Try to anticpate enemy movement.
            -When the enemy is captured in a bubble they will move to the top center of the screen. Jump up there to collect them.

            Actions:
            - RIGHT: move right.
            - LEFT: move left.
            - JUMP: jump.
            - FIRE: fires a bubble to capture an enemy
                    
            Previous plan: {previous_plan}
            Previous action: {action}
            Previous enemy positions: {enemy_pos}
                    
            Return JSON with exactly these two fields:
            action: one of LEFT, RIGHT, JUMP, FIRE
            plan: an extremely concise description of your immediate goal
            player_loc: extremely concise position of player
            enemy_pos: describe enemy positions relative to player
                    
            Do not output anything else.
        '''

    def get_key_mapping(self):
        return {
            "LEFT" : "o",
            "RIGHT" : "p",
            "FIRE" : "n",
            "JUMP" : "m"
        }