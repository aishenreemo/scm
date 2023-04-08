from pygame.surface import Surface
import pygame

from .element import ElementType, Element


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

        self.draw()

        return

    def draw(
        self,
        width=0,
        color=None,
        border_radius=0,
        border_custom_radius=(-1, -1, -1, -1),
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
