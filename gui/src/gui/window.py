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

    def add_image(
        self,
        name="sample_element",
        size=(1, 1),
        position=(0, 0),
        path=""
    ):
        mem = Memory()

        self.elements.append(ImageElement(
            name,
            mem.window_size_percentage(size[0], size[1]),
            mem.window_size_percentage(position[0], position[1]),
            path
        ))

        return

    def add_rect(
         self,
         name="sample_element",
         size=(1, 1),
         position=(0, 0),
         color=(0, 0, 0)
    ):
        mem = Memory()

        self.elements.append(RectElement(
            name,
            size=mem.window_size_percentage(size[0], size[1]),
            position=mem.window_size_percentage(position[0], position[1]),
            color=color,
        ))

        return

    def add_rounded_rect(
        self,
        name="sample_element",
        size=(1, 1),
        position=(0, 0),
        color=(0, 0, 0),
        width=0,
        border_radius=0,
        border_custom_radius=(-1, -1, -1, -1)
    ):
        mem = Memory()

        self.elements.append(RectElement(
            name,
            size=mem.window_size_percentage(size[0], size[1]),
            position=mem.window_size_percentage(position[0], position[1]),
        ).rounded(width, border_radius, border_custom_radius, color))

        return

    def add_text(
        self,
        name="sample_element",
        position=(0, 0),
        color=(0, 0, 0),
        text="Hello World",
        pt=12
    ):
        mem = Memory()

        self.elements.append(TextElement(
            name,
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
            name="background",
            size=(1, 1),
            position=(0, 0),
            path="assets/images/background.png"
        )

        # add logo
        self.add_image(
            name="logo",
            size=(0.5, 0.3),
            position=(0.25, 0.05),
            path="assets/images/logo.png"
        )

        # add blue rect
        self.add_rounded_rect(
            name="login_rect",
            size=(0.3, 0.5),
            position=(0.35, 0.4),
            color=colors["normal"]["blue"],
            width=0,
            border_radius=5
        )

        # add logo small
        self.add_image(
            "logo_small",
            (0.175, 0.225),
            (0.4125, 0.415),
            "assets/images/logo_small.png"
        )

        # add input rects and login button
        for info in [
            (
                "username",
                (0.25, 0.05),
                (0.375, 0.655),
                colors["normal"]["white"]
            ),
            (
                "password",
                (0.25, 0.05),
                (0.375, 0.715),
                colors["normal"]["white"]
            ),
            (
                "login",
                (0.15, 0.05),
                (0.425, 0.780),
                colors["bright"]["blue"]
            )
        ]:
            self.add_rounded_rect(
                name=info[0],
                size=info[1],
                position=info[2],
                color=info[3],
                width=0,
                border_radius=2
            )

        return


class StudentListPage(Page):
    def __init__(self):
        super().__init__("student_list")
        colors = Config().colors

        self.add_image(
            name="background",
            size=(1, 1),
            position=(0, 0),
            path="assets/images/background.png"
        )

        self.add_image(
            "logo_small",
            (0.125, 0.175),
            (0.025, 0.025),
            "assets/images/logo_small.png"
        )

        self.add_text(
            name="title",
            position=(0.175, 0.05),
            color=colors["background"],
            text="School Clinic Management System",
            pt=34
        )

        self.add_rect(
            name="menu",
            size=(0.05, 0.05),
            position=(0.9, 0.05),
            color=colors["background"],
        )

        self.add_rect(
            name="search",
            size=(0.5, 0.05),
            position=(0.25, 0.12),
            color=colors["bright"]["white"],
        )

        self.add_rect(
            name="student_list_rect",
            size=(0.5, 0.7),
            position=(0.4, 0.25),
            color=colors["bright"]["white"],
        )

        return
