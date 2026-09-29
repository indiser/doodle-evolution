from config import *
from assets import exploding_platform_sound

class Platform:
    def __init__(self, x, y, image, breakable=False, broken_frames=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.breakable = breakable
        self.broken_frames = broken_frames or []
        self.broken = False
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 5
        self.finished = False

    def scroll(self, amount):
        self.rect.y -= amount

    def break_platform(self):
        if self.breakable and not self.broken:
            self.broken = True

    def update(self):
        if self.broken and self.broken_frames:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.frame_index += 1
                if self.frame_index >= len(self.broken_frames):
                    self.finished = True

    def draw(self, surface):
        if self.broken and self.broken_frames:
            if self.frame_index < len(self.broken_frames):
                surface.blit(self.broken_frames[self.frame_index], self.rect)
        else:
            surface.blit(self.image, self.rect)


class ExplodingPlatform(Platform):
    def __init__(self, x, y, frames):
        # Initialize with the first frame (yellow)
        super().__init__(x, y, frames[0], breakable=False)
        self.frames = frames
        self.timer = 0
        self.explode_time = 120  # 2 seconds at 60 FPS
        self.warning_time = 80   # Turns red after ~1.3 seconds
        self.vanish_time = 135   # Lingers for 15 frames (0.25s) to show the explosion
        self.exploded = False
        self.is_explosive = True 

    def update(self):
        self.timer += 1
        
        # Phase 3: Purge from memory
        if self.timer > self.vanish_time:
            self.finished = True 

        # Phase 2: Detonate
        elif self.timer > self.explode_time and not self.exploded:
            self.exploded = True
            self.image = self.frames[2] # Draw the explosion frame
            self.broken = True # Instantly disables collisions in main.py
            
            exploding_platform_sound.play()
            
        # Phase 1: Warning
        elif self.timer > self.warning_time and not self.exploded:
            self.image = self.frames[1] # Draw the red warning frame


    def draw(self, surface):
        # Always draw the current image until the vanish_time deletes it
        surface.blit(self.image, self.rect)

class MovingPlatform(Platform):
    def __init__(self, x, y, image, axis, current_score):
        super().__init__(x, y, image)
        self.axis = axis
        # Speed scales up by 1 for every 3000 points
        self.speed = 2 + (int(current_score) // 3000) 
        self.direction = 1
        self.start_y = y
        self.range = 75 # Pixels it can travel up/down before reversing

    def update(self):
        if self.axis == 'horizontal':
            self.rect.x += self.speed * self.direction
            if self.rect.right >= WIDTH or self.rect.left <= 0:
                self.direction *= -1

        elif self.axis == 'vertical':
            self.rect.y += self.speed * self.direction
            # Reverse direction if it moves too far from its original spawn Y
            if abs(self.rect.y - self.start_y) > self.range:
                self.direction *= -1
                
    def scroll(self, amount):
        super().scroll(amount)
        # Shift the start_y so vertical platforms don't fly off screen when the camera moves
        self.start_y -= amount