from ..app.config import Config
from ..app.memory import Memory
from .element import (
    ImageElement,
    RectElement,
    TextElement,
    WindowElement,
)


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


class MainPage(Page):
    def __init__(self):
        super().__init__("main_page")

        colors = Config().colors

        ImageElement(
            "logo",
            self.percent(50, 30),
            self.percent(25, 5),
            "assets/images/logo.png",
        ).add_to(self)

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

        return


class StudentListPage(Page):
    def __init__(self):
        super().__init__("student_list_page")

        colors = Config().colors

        ImageElement(
            "logo_small",
            self.percent(12.5, 17.5),
            self.percent(02.5, 02.5),
            "assets/images/logo_small.png"
        ).add_to(self)

        TextElement(
            "title",
            self.percent(17.5, 5),
            colors["background"],
            "School Clinic Management System",
            34
        ).add_to(self)

        RectElement(
            "menu_btn",
            self.percent(5, 5),
            self.percent(90, 5),
            colors["background"],
        ).add_to(self)

        RectElement(
            "search",
            self.percent(50, 5),
            self.percent(25, 12),
            colors["normal"]["white"]
        ).rounded(1, 0, colors["background"]) \
            .add_to(self)

        info_window = WindowElement(
            "info_window",
            self.percent(50, 70),
            self.percent(40, 25),
        )

        RectElement(
            "info_rect",
            info_window.percent(100, 100),
            info_window.percent(0, 0),
            colors["normal"]["white"]
        ).rounded(1, 0, colors["background"]) \
            .add_to(info_window)

        RectElement(
            "boys_title_rect",
            info_window.percent(46, 10),
            info_window.percent(2, 2),
            colors["normal"]["blue"]
        ).rounded(1, 0, colors["background"]) \
            .add_to(info_window)

        RectElement(
            "girls_title_rect",
            info_window.percent(46, 10),
            info_window.percent(52, 2),
            colors["normal"]["magenta"]
        ).rounded(1, 0, colors["background"]) \
            .add_to(info_window)

        RectElement(
            "boys_rect",
            info_window.percent(46, 80),
            info_window.percent(2, 15)
        ).rounded(1, 0, colors["background"]) \
            .add_to(info_window)

        RectElement(
            "girls_rect",
            info_window.percent(46, 80),
            info_window.percent(52, 15)
        ).rounded(1, 0, colors["background"]) \
            .add_to(info_window)

        info_window.flush()
        info_window.add_to(self)

        for i in range(0, 6):
            RectElement(
                "grade_" + str(i + 7) + "_rect",
                self.percent(30, 10),
                self.percent(5, 25 + (i * 12)),
                colors["normal"]["white"],
            ).rounded(1, 0, colors["normal"]["black"]) \
                .add_to(self)

        return
