from pygame.transform import scale
from pygame.image import load

from .element import ElementType, Element


class ImageElement(Element):
    def __init__(self, name, size=(1, 1), position=(0, 0), path=""):
        super().__init__(name, ElementType.IMAGE, size, position)

        self.path = path
        self.image = load(path)
        self.surface = scale(self.image, self.size)

        return
