from ..app.config import Config
from ..app.memory import Memory
from .element import (
    ImageElement,
    RectElement,
    TextElement,
)


class Page:
    def __init__(self, name):
        self.name = str(name)
        self.elements = []

        return

    def add_image(self, size=(1, 1), position=(0, 0), path=""):
        mem = Memory()

        self.elements.append(ImageElement(
            mem.window_size_percentage(size[0], size[1]),
            mem.window_size_percentage(position[0], position[1]),
            path
        ))

        return

    def add_rect(self, size=(1, 1), position=(0, 0), color=(0, 0, 0)):
        mem = Memory()

        self.elements.append(RectElement(
            size=mem.window_size_percentage(size[0], size[1]),
            position=mem.window_size_percentage(position[0], position[1]),
            color=color,
        ))

        return

    def add_rounded_rect(
        self,
        size=(1, 1),
        position=(0, 0),
        color=(0, 0, 0),
        width=0,
        border_radius=0,
        border_custom_radius=(-1, -1, -1, -1)
    ):
        mem = Memory()

        self.elements.append(RectElement(
            size=mem.window_size_percentage(size[0], size[1]),
            position=mem.window_size_percentage(position[0], position[1]),
        ).rounded(width, border_radius, border_custom_radius, color))

        return

    def add_text(
        self,
        position=(0, 0),
        color=(0, 0, 0),
        text="Hello World",
        pt=12
    ):
        mem = Memory()

        self.elements.append(TextElement(
            position=mem.window_size_percentage(position[0], position[1]),
            color=color,
            text=text,
            pt=pt
        ))

        return


class MainPage(Page):
    def __init__(self):
        super().__init__("main")

        colors = Config().colors

        self.add_image(
            size=(1, 1),
            position=(0, 0),
            path="assets/images/background.png"
        )

        # add logo
        self.add_image(
            size=(0.5, 0.3),
            position=(0.25, 0.05),
            path="assets/images/logo.png"
        )

        # add blue rect
        self.add_rounded_rect(
            size=(0.3, 0.5),
            position=(0.35, 0.4),
            color=colors["normal"]["blue"],
            width=0,
            border_radius=5
        )

        # add logo small
        self.add_image(
            (0.175, 0.225),
            (0.4125, 0.415),
            "assets/images/logo_small.png"
        )

        # add input rects and login button
        for info in [
            ((0.25, 0.05), (0.375, 0.655), colors["normal"]["white"]),
            ((0.25, 0.05), (0.375, 0.715), colors["normal"]["white"]),
            ((0.15, 0.05), (0.425, 0.780), colors["bright"]["blue"])
        ]:
            self.add_rounded_rect(
                size=info[0],
                position=info[1],
                color=info[2],
                width=0,
                border_radius=2
            )

        return


class StudentListPage(Page):
    def __init__(self):
        super().__init__("student_list")

        self.add_image(
            size=(1, 1),
            position=(0, 0),
            path="assets/images/background.png"
        )

        return
