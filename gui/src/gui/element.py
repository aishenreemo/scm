from pygame.sprite import Sprite
from pygame import Surface
import pygame

from enum import Enum


class ElementType(Enum):
    RECT = 0
    IMAGE = 1


class Element(Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type

        return


class RectElement(Element):
    def __init__(
        self,
        size=(1, 1),
        position=(0, 0),
        color=None,
    ):
        super().__init__(ElementType.RECT)

        try:
            if size[0] <= 0 or size[1] <= 0:
                raise ValueError("invalid size argument")
        except ValueError as err:
            print("RectElement.__init__(size):", err)
            exit(1)

        self.color = color or [0, 0, 0, 0]
        self.size = size
        self.position = position
        self.surface = Surface(size).convert_alpha()
        self.rect = self.surface.get_rect()

        self.fill()

        return

    def fill(self, color=None):
        self.surface.fill(color or self.color)

        return self

    def rounded(
        self,
        width=0,
        border_radius=0,
        border_custom_radius=(-1, -1, -1, -1),
        color=None,
    ):
        pygame.draw.rect(
            self.surface,
            color or self.color,
            self.rect,
            width,
            border_radius,
            border_custom_radius[0],
            border_custom_radius[1],
            border_custom_radius[2],
            border_custom_radius[3],
        )

        return self


class ImageElement(Element):
    def __init__(self, size=(1, 1), position=(0, 0), path=""):
        super().__init__(ElementType.IMAGE)

        try:
            if size[0] <= 0 or size[1] <= 0:
                raise ValueError("invalid size argument")
        except ValueError as err:
            print("RectElement.__init__(size):", err)
            exit(1)

        self.size = size
        self.position = position
        self.path = path
        self.image = pygame.image.load(path)
        self.surface = pygame.transform.scale(self.image, self.size)

        return
