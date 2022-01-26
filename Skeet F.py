"""
File: skeet.py
Original Author: Br. Burton
Designed to be completed by others
This program implements an awesome version of skeet.

Written by Nathan Taylor
CS241 Prove 07
"""
import arcade
import math
import random
from abc import abstractmethod
from abc import ABC


# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 15

class Point:
    # This will initiate the point to be a float.
    def __init__ (self):
        self.x = 0.0
        self.y = 0.0
        
class Velocity:
    # This will initiate the velocity to be a float.
    
    def __init(self):
        self.dx = 0.0
        self.dy = 0.0
        
class FlyingObject(ABC):
    
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0.0
        self.alive = True
        
        
    
    def advance(self):
        #This will advance the flying object
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
    @abstractmethod    
    def draw(self): #abstract function
        pass
    
    def is_off_screen(self):
        # Determines if anything is off screen and sets the self.alive = False.
        if (self.center.x > SCREEN_WIDTH):
            return True
        elif (self.center.y > SCREEN_HEIGHT or self.center.y < 0):
             return True
        else:
            return False

class Target(FlyingObject, ABC):
    
    def __init__(self):
        super().__init__()
        
        # This decides where the targets will come from.
        
        self.center.y = float(random.randint((SCREEN_HEIGHT // 2), 500))
        
        # This will set the velocity of the targets.
        self.velocity.dx = random.randint(1,5)
        self.velocity.dy = random.randint(-2,5)
        
        self.radius = TARGET_RADIUS
        
        self.alive = True
    
    @abstractmethod
    def draw(self): # absract function
        pass
    
    @abstractmethod
    def hit(self): # abstract function
        pass
    
class Standard_target(Target):
    
    def __init__(self):
        super().__init__()
        
    
    def draw(self):
        # if the target is alive, it will draw the target.
        arcade.draw_circle_filled(self.center.x, self.center.y, TARGET_RADIUS, TARGET_COLOR)
    
    def hit(self):
        # If this target is hit, it will be considered dead and return one point to the score. 
        self.alive = False
        return 1
    
class Strong_target(Target):
    
    def __init__(self):
        super().__init__()
        self.velocity.dx = random.randint(1,3)
        self.velocity.dy = random.randint(-2,3)
        self.lives = 3
    
    def draw(self):
        #This draws just the outline of a circle with the number of lives it has left inscribed in the circle. 
        arcade.draw_circle_outline(self.center.x,self.center.y, TARGET_RADIUS, TARGET_COLOR)
        text_x = self.center.x - (TARGET_RADIUS / 2)
        text_y = self.center.y - (TARGET_RADIUS / 2)
        arcade.draw_text(repr(self.lives), text_x, text_y, TARGET_COLOR, font_size=20)
    
    def hit(self):
        # When the target is hit it drops the number lives of lives down by one and gives one point.
        if (self.lives > 1):
            self.lives -= 1
            return 1
         
         # When the target gets hit the third time it is considered dead and gives 3 points.
        else:
            self.alive = False
            return 3
            
    
class Safe_target(Target):
    
    def __init__(self):
        super().__init__()
        self.radius = TARGET_SAFE_RADIUS
    
    def draw(self):
        #The safe target it a solid square.
        arcade.draw_rectangle_filled(self.center.x, self.center.y, TARGET_SAFE_RADIUS, TARGET_SAFE_RADIUS, TARGET_SAFE_COLOR) 
    
    def hit(self):
        #This target should not be hit, so when it is hit it takes away ten points. 
        self.alive = False
        return -10
    
class Bullet(FlyingObject):
    
    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS
        
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, BULLET_RADIUS, BULLET_COLOR)
    
    def fire(self, angle):
        #This sets the bullet to come out of the center of the rifle.
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED
    

class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0

        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, self.angle)


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.rifle = Rifle()
        self.score = 0

        self.bullets = []
        
        self.targets = []

        # TODO: Create a list for your targets (similar to the above bullets)


        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()

        # TODO: iterate through your targets and draw them...
        for target in self.targets:
            target.draw()


        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        if random.randint(1, 50) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()

        # TODO: Iterate through your targets and tell them to advance
        for target in self.targets:
            target.advance()

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """

        # TODO: Decide what type of target to create and append it to the list
        target_num = random.randint(0,2)
        
        if (target_num == 0):
            target = Strong_target()
            self.targets.append(target)
        
        elif (target_num == 1):
            target = Safe_target()
            self.targets.append(target)
        
        else:
            target = Standard_target()
            self.targets.append(target)

        """
        target_options = [Strong_target(), Safe_target(), Standard_target()]
        target = random.choice(target_options)
        self.targets.append(target)
        """
    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen():
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)
        
    def check_keys(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)
        
        if arcade.key.SPACE  in self.held_keys:
            bullet = Bullet()
            bullet.fire()
            bullets.append(new_bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()