from pygame.font import (
    get_default_font,
    Font,
)

from .element import (
    ElementType,
    Element,
)


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

        self.family = get_default_font()
        self.text = text
        self.pt = pt

        self.color = color
        self.font = Font(self.family, self.pt)
        self.surface = self.font.render(self.text, True, self.color)
        self.size = self.surface.get_size()

        return
