import pygame

class Player:
    def __init__(self, x, y, image_right, image_left):
        self.image_right = image_right
        self.image_left = image_left
        self.image = image_right
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.y_velocity = 0

        self.is_flipping = False
        self.flip_angle = 0

    def move(self, keys, move_speed, screen_width):
        if keys[pygame.K_LEFT]:
            self.rect.x -= move_speed
            self.image = self.image_left
        if keys[pygame.K_RIGHT]:
            self.rect.x += move_speed
            self.image = self.image_right

        if self.rect.right < 0:
            self.rect.left = screen_width
        elif self.rect.left > screen_width:
            self.rect.right = 0

    def apply_gravity(self, gravity):
        self.y_velocity += gravity
        self.rect.y += self.y_velocity

        if self.y_velocity > 0:
            self.is_flipping = False
            self.flip_angle = 0

    def jump(self, strength, boost_multiplier=1.0, flip = False):
        self.y_velocity = strength * boost_multiplier
        if flip:
            self.is_flipping = True
            self.flip_angle = 0

    def draw(self, surface):
        if self.is_flipping:
            self.flip_angle -= 15  # Adjust this number to spin faster/slower
            rotated_image = pygame.transform.rotate(self.image, self.flip_angle)
            new_rect = rotated_image.get_rect(center=self.rect.center)
            surface.blit(rotated_image, new_rect)
        else:
            surface.blit(self.image, self.rect)