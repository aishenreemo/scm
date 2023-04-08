from ...app.config import Config
from ..element import (
    ImageElement,
    TextElement,
    RectElement,
    WindowElement,
)

from . import Page


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

        ImageElement(
            "menu_btn",
            self.percent(5, 6),
            self.percent(90, 5),
            "assets/images/menu.png",
        ).add_to(self)

        RectElement(
            "search",
            self.percent(50, 5),
            self.percent(25, 12),
            colors["normal"]["white"]
        ).draw(1, colors["background"]) \
            .add_to(self)

        self.student_list_init()
        self.section_list_init()

        for i in range(0, 6):
            RectElement(
                "grade_" + str(i + 7) + "_rect",
                self.percent(30, 10),
                self.percent(5, 25 + (i * 12)),
                colors["normal"]["white"],
            ).draw(1, colors["normal"]["black"]) \
                .add_to(self)

            TextElement(
                "grade_" + str(i + 7) + "_text",
                self.percent(13, 28 + (i * 12)),
                colors["background"],
                "GRADE " + str(i + 7),
                26,
            ).add_to(self)

        return

    def student_list_init(self):
        colors = Config().colors
        info_window = WindowElement(
            "student_list_window",
            self.percent(50, 70),
            self.percent(40, 25),
            visible=False
        )

        RectElement(
            "info_rect",
            info_window.percent(100, 100),
            info_window.percent(0, 0),
            colors["normal"]["white"]
        ).draw(1, colors["background"]) \
            .add_to(info_window)

        RectElement(
            "boys_title_rect",
            info_window.percent(46, 10),
            info_window.percent(2, 2),
            colors["normal"]["blue"]
        ).draw(1, colors["background"]) \
            .add_to(info_window)

        RectElement(
            "girls_title_rect",
            info_window.percent(46, 10),
            info_window.percent(52, 2),
            colors["normal"]["magenta"]
        ).draw(1, colors["background"]) \
            .add_to(info_window)

        RectElement(
            "boys_rect",
            info_window.percent(46, 80),
            info_window.percent(2, 15)
        ).draw(1, colors["background"]) \
            .add_to(info_window)

        RectElement(
            "girls_rect",
            info_window.percent(46, 80),
            info_window.percent(52, 15)
        ).draw(1, colors["background"]) \
            .add_to(info_window)

        info_window.flush()
        info_window.add_to(self)

        return

    def section_list_init(self):
        colors = Config().colors
        info_window = WindowElement(
            "section_list_window",
            self.percent(50, 70),
            self.percent(40, 25),
        )

        RectElement(
            "info_rect",
            info_window.percent(100, 100),
            info_window.percent(0, 0),
            colors["normal"]["white"]
        ).draw(1, colors["background"]) \
            .add_to(info_window)

        RectElement(
            "section_rect",
            info_window.percent(95, 95),
            info_window.percent(2.5, 2.5),
        ).draw(1, colors["background"]) \
            .add_to(info_window)

        info_window.flush()
        info_window.add_to(self)

        return
