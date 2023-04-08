from pygame.surface import Surface
from .element import (
    ElementType,
    Element,
)


class WindowElement(Element):
    def __init__(
        self,
        name,
        size=(1, 1),
        position=(0, 0),
        visible=True,
    ):
        super().__init__(name, ElementType.WINDOW, size, position, visible)
        self.elements = []
        self.surface = Surface(self.size).convert_alpha()
        self.surface.fill([0, 0, 0, 0])

        return

    def flush(self):
        for element in self.elements:
            if not element.visible:
                continue

            self.surface.blit(element.surface, element.position)

        return

    def percent(self, x, y):
        return (
            self.size[0] * (x / 100),
            self.size[1] * (y / 100),
        )

    def get_element(self, element_name):
        for element in self.elements:
            if element.name == element_name:
                return element

        return None
