from ...app.config import Config
from ..element import (
    ImageElement,
    RectElement,
    WindowElement,
)

from . import Page


class MainPage(Page):
    def __init__(self):
        super().__init__("main_page")

        ImageElement(
            "logo",
            self.percent(50, 30),
            self.percent(25, 5),
            "assets/images/logo.png",
        ).add_to(self)

        self.login_init()

        return

    def login_init(self):
        colors = Config().colors

        login_window = WindowElement(
            "login_window",
            self.percent(30, 50),
            self.percent(35, 40),
        )

        RectElement(
            "login_rect",
            login_window.percent(100, 100),
            login_window.percent(0, 0),
        ).rounded(0, 20, colors["normal"]["blue"]) \
            .rounded(1, 20, colors["background"]) \
            .add_to(login_window)

        ImageElement(
            "logo_small",
            login_window.percent(50, 40),
            login_window.percent(25, 5),
            "assets/images/logo_small.png",
        ).add_to(login_window)

        RectElement(
            "username",
            login_window.percent(90, 8),
            login_window.percent(5, 50),
        ).rounded(0, 5, colors["normal"]["white"]) \
            .rounded(1, 5, colors["background"]) \
            .add_to(login_window)

        RectElement(
            "password",
            login_window.percent(90, 8),
            login_window.percent(5, 60),
        ).rounded(0, 5, colors["normal"]["white"]) \
            .rounded(1, 5, colors["background"]) \
            .add_to(login_window)

        RectElement(
            "login_btn",
            login_window.percent(60, 8),
            login_window.percent(20, 70),
        ).rounded(0, 5, colors["bright"]["blue"]) \
            .rounded(1, 5, colors["background"]) \
            .add_to(login_window)

        login_window.flush()
        login_window.add_to(self)
