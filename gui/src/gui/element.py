from pygame.sprite import Sprite
from pygame import Surface
import pygame

from enum import Enum


class ElementType(Enum):
    RECT = 0
    IMAGE = 1
    TEXT = 2


class Element(Sprite):
    def __init__(self, name, type, size, position):
        super().__init__()
        self.name = name
        self.type = type
        self.size = size
        self.position = position

        try:
            if size[0] <= 0 or size[1] <= 0:
                raise ValueError("invalid size argument")
        except ValueError as err:
            print("RectElement.__init__(size):", err)
            exit(1)

        return


class RectElement(Element):
    def __init__(
        self,
        name,
        size=(1, 1),
        position=(0, 0),
        color=None,
    ):
        super().__init__(name, ElementType.RECT, size, position)

        self.color = color or [0, 0, 0, 0]
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
    def __init__(self, name, size=(1, 1), position=(0, 0), path=""):
        super().__init__(name, ElementType.IMAGE, size, position)

        self.path = path
        self.image = pygame.image.load(path)
        self.surface = pygame.transform.scale(self.image, self.size)

        return


class TextElement(Element):
    def __init__(
        self,
        name,
        position=(0, 0),
        color=(0, 0, 0),
        text="Hello World",
        pt=12,
    ):
        super().__init__(name, ElementType.TEXT, (1, 1), position)

        self.family = pygame.font.get_default_font()
        self.text = text
        self.pt = pt

        self.color = color
        self.font = pygame.font.Font(self.family, self.pt)
        self.surface = self.font.render(self.text, True, self.color)
        self.size = self.surface.get_size()

        return
