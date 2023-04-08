from ...app.config import Config
from ..element import (
    ImageElement,
    TextElement,
    RectElement,
    WindowElement,
)

from . import Page


class StudentInfoPage(Page):
    def __init__(self):
        super().__init__("student_info_page")

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

        RectElement(
            "data_btn_rect",
            self.percent(13, 8),
            self.percent(4, 22),
        ).draw(0, colors["foreground"], 20) \
            .draw(1, colors["background"], 20) \
            .add_to(self)

        TextElement(
            "data_btn_text",
            self.percent(5, 25),
            colors["background"],
            "SHOW DATA",
            16
        ).add_to(self)

        RectElement(
            "record_btn_rect",
            self.percent(21, 8),
            self.percent(18, 22),
        ).draw(0, colors["foreground"], 20) \
            .draw(1, colors["background"], 20) \
            .add_to(self)

        TextElement(
            "record_btn_text",
            self.percent(19, 25),
            colors["background"],
            "ADD/UPDATE RECORD",
            15
        ).add_to(self)

        RectElement(
            "print_btn_rect",
            self.percent(8, 8),
            self.percent(40, 22),
        ).draw(0, colors["foreground"], 20) \
            .draw(1, colors["background"], 20) \
            .add_to(self)

        TextElement(
            "print_btn_text",
            self.percent(41, 25),
            colors["background"],
            "PRINT",
            16
        ).add_to(self)

        RectElement(
            "delete_btn_rect",
            self.percent(9, 8),
            self.percent(49, 22),
        ).draw(0, colors["foreground"], 20) \
            .draw(1, colors["background"], 20) \
            .add_to(self)

        TextElement(
            "delete_btn_text",
            self.percent(50, 25),
            colors["background"],
            "DELETE",
            16
        ).add_to(self)

        RectElement(
            "back_btn_rect",
            self.percent(7, 8),
            self.percent(59, 22),
        ).draw(0, colors["foreground"], 20) \
            .draw(1, colors["background"], 20) \
            .add_to(self)

        TextElement(
            "back_btn_text",
            self.percent(60, 25),
            colors["background"],
            "BACK",
            16
        ).add_to(self)

        self.data_init()
        self.record_init()
        self.print_init()
        self.delete_init()
        self.back_init()

        return

    def data_init(self):
        colors = Config().colors

        data_window = WindowElement(
            "data_window",
            self.percent(90, 60),
            self.percent(5, 35),
        )

        RectElement(
            "data_rect",
            data_window.percent(100, 100),
            data_window.percent(0, 0),
            colors["foreground"],
        ).draw(1, colors["background"]) \
            .add_to(data_window)

        data_window.flush()
        data_window.add_to(self)

        return

    def record_init(self):
        colors = Config().colors

        record_window = WindowElement(
            "record_window",
            self.percent(90, 60),
            self.percent(5, 35),
            visible=False
        )

        RectElement(
            "record_rect",
            record_window.percent(100, 100),
            record_window.percent(0, 0),
            colors["foreground"],
        ).draw(1, colors["background"]) \
            .add_to(record_window)

        record_window.flush()
        record_window.add_to(self)

        return

    def print_init(self):
        colors = Config().colors

        print_window = WindowElement(
            "print_window",
            self.percent(90, 60),
            self.percent(5, 35),
            visible=False
        )

        RectElement(
            "print_rect",
            print_window.percent(100, 100),
            print_window.percent(0, 0),
            colors["foreground"],
        ).draw(1, colors["background"]) \
            .add_to(print_window)

        print_window.flush()
        print_window.add_to(self)

        return

    def delete_init(self):
        colors = Config().colors

        delete_window = WindowElement(
            "delete_window",
            self.percent(90, 60),
            self.percent(5, 35),
            visible=False
        )

        RectElement(
            "delete_rect",
            delete_window.percent(100, 100),
            delete_window.percent(0, 0),
            colors["foreground"],
        ).draw(1, colors["background"]) \
            .add_to(delete_window)

        delete_window.flush()
        delete_window.add_to(self)

        return

    def back_init(self):
        colors = Config().colors

        back_window = WindowElement(
            "back_window",
            self.percent(90, 60),
            self.percent(5, 35),
            visible=False
        )

        RectElement(
            "back_rect",
            back_window.percent(100, 100),
            back_window.percent(0, 0),
            colors["foreground"],
        ).draw(1, colors["background"]) \
            .add_to(back_window)

        back_window.flush()
        back_window.add_to(self)

        return
