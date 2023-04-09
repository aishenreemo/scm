from pygame import locals as pyg_locals
from pygame import rect as pyg_rect

from ...ui.elements import ElementType, TextElement
from ..memory import Memory
from ..config import Config
from .command import (
    CommandType,
    Command,
)


class ShowStudentListCommand(Command):
    def __init__(self, opts):
        super().__init__(CommandType.SHOW_STUDENT_LIST_COMMAND)
        self.grade_level = opts[0]
        self.section = opts[1]

    def run(self, app):
        memory = Memory()
        config = Config()
        window = app.gui.pages[1]
        section_window = window.get_element("section_list_window")
        student_window = window.get_element("student_list_window")
        student_window.visible = True
        section_window.visible = False

        elements = []

        for element in student_window.elements:
            if not element.name.endswith("_rect") and not element.name.endswith("_text"):
                continue

            elements.append(element)

        boys_count = 0
        girls_count = 0
        for student in memory.students:
            if student["section"] != self.section:
                continue

            if student["grade_level"] != self.grade_level - 7:
                continue

            name = student["name"]
            if student["gender"] == 0:
                elements.append(TextElement(
                    name["first"].lower() + "_" + student["name"]["last"].lower() + "_item",
                    student_window.percent(6, 20 + boys_count * 4),
                    config.colors["background"],
                    name["last"] + " " + name["first"] + " " + name["middle"],
                    12,
                ))
                boys_count += 1
            else:
                elements.append(TextElement(
                    name["first"].lower() + "_" + student["name"]["last"].lower() + "_item",
                    student_window.percent(56, 20 + girls_count * 4),
                    config.colors["background"],
                    name["last"] + " " + name["first"] + " " + name["middle"],
                    12,
                ))
                girls_count += 1

        student_window.elements = elements
        student_window.flush()

        return

    def opts(app, event):
        if pyg_locals.MOUSEBUTTONDOWN != event.type:
            return None

        if app.gui.pointer != 1:
            return None

        window = app.gui.pages[app.gui.pointer]
        section_window = window.get_element("section_list_window")

        if not section_window.visible:
            return None

        for element in section_window.elements:
            if (element.type != ElementType.TEXT):
                continue

            rect = pyg_rect.Rect(
                element.position[0] + section_window.position[0],
                element.position[1] + section_window.position[1],
                element.size[0],
                element.size[1],
            )

            if not rect.collidepoint(event.pos):
                continue

            return [
                int(element.text.split(" ")[0]),
                str(element.text.split(" ")[1]),
            ]

        return None
