class Feeder:
    def __init__(self, x, y, image_down, image_up):
        self.image_down = image_down
        self.image_up = image_up
        self.rect = self.image_down.get_rect(midbottom=(x, y))
        self.sprung = False

    def trigger(self):
        self.sprung = True

    def scroll(self, amount):
        self.rect.y -= amount

    def draw(self, surface):
        if self.sprung:
            surface.blit(self.image_up, self.rect)
        else:
            surface.blit(self.image_down, self.rect)
