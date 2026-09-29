import pygame
import math

class Monster:
    def __init__(self, platform, y_offset, frames):
        self.frames = frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        
        # Anchor to the parent platform
        self.platform = platform
        self.y_offset = y_offset
        
        # Animation and timing
        self.frame_index = 0
        self.animation_speed = 0.15
        self.time = 0
        self.hover_speed = 0.05
        
        # Dynamic boundaries: Calculate exact max sway so it never hangs off the edge
        self.hover_range = (self.platform.rect.width - self.rect.width) // 2
        if self.hover_range < 0:
            self.hover_range = 0 # Prevents erratic math if the monster is wider than the platform
        
    def update(self):
        # 1. Animation Cycle
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
        # 2. Dynamic Anchoring (Follows the platform even if it moves horizontally)
        self.time += self.hover_speed
        self.rect.centerx = self.platform.rect.centerx + math.sin(self.time) * self.hover_range
        
        # Lock the monster's vertical position to the platform's current position
        self.rect.bottom = self.platform.rect.top - self.y_offset
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)