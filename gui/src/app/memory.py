import pygame


class Memory:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Memory, cls).__new__(cls)

        return cls.instance

    def update(self):
        self.window_size = pygame.display.get_surface().get_size()

        return

    def window_size_percentage(self, size_x, size_y):
        return (
            self.window_size[0] * size_x,
            self.window_size[1] * size_y
        )
