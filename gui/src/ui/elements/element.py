from pygame.sprite import Sprite
from enum import Enum


class ElementType(Enum):
    RECT = 0
    IMAGE = 1
    TEXT = 2
    WINDOW = 3


class Element(Sprite):
    def __init__(self, name, type, size, position, visible=True):
        super().__init__()

        self.name = name
        self.type = type
        self.size = size
        self.visible = visible
        self.position = position

        try:
            if size[0] <= 0 or size[1] <= 0:
                raise ValueError("invalid size argument")
        except ValueError as err:
            print("RectElement.__init__(size):", err)
            exit(1)

        return

    def add_to(self, window):
        window.elements.append(self)

        return
