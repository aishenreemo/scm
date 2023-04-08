from ...app.memory import Memory
from ..element import ImageElement


class Page:
    def __init__(self, name):
        self.name = str(name)
        self.elements = []

        ImageElement(
            "background",
            self.percent(100, 100),
            self.percent(0, 0),
            "assets/images/background.png",
        ).add_to(self)

        return

    def percent(self, x, y):
        return Memory().percent_ws(x, y)
