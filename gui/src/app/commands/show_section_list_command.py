from pygame import locals as pyg_locals
from pygame import rect as pyg_rect

from ...ui.elements import TextElement
from ..memory import Memory
from ..config import Config
from .command import (
    CommandType,
    Command,
)


class ShowSectionListCommand(Command):
    def __init__(self, opts):
        super().__init__(CommandType.SHOW_SECTION_LIST_COMMAND)
        self.grade_level = opts

    def run(self, app):
        memory = Memory()
        config = Config()
        window = app.gui.pages[1]
        student_window = window.get_element("student_list_window")
        section_window = window.get_element("section_list_window")
        student_window.visible = False
        section_window.visible = True

        memory.update_lazy()

        elements = []
        sections = []

        for element in section_window.elements:
            if not element.name.endswith("_rect"):
                continue

            elements.append(element)

        i = 0
        for student in memory.students:
            section = student["section"]
            if section in sections:
                continue

            if self.grade_level != (student["grade_level"] + 7):
                continue

            sections.append(section)
            elements.append(TextElement(
                section.lower() + "_item",
                section_window.percent(6, 5 + i * 5),
                config.colors["background"],
                str(self.grade_level) + " " + section,
                16,
            ))

            i += 1

        section_window.elements = elements
        section_window.flush()

        return

    def opts(app, event):
        if pyg_locals.MOUSEBUTTONDOWN == event.type:
            if app.gui.pointer == 1:
                window = app.gui.pages[app.gui.pointer]

                elements = list(filter(ShowSectionListCommand.is_grade_level_element, window.elements))
                rects = list(map(ShowSectionListCommand.element_to_rect, elements))

                for i in range(0, len(elements)):
                    if rects[i].collidepoint(event.pos):
                        return int(elements[i].name.split("_")[1])

    @staticmethod
    def is_grade_level_element(element):
        return element.name.startswith("grade") and element.name.endswith("rect")

    @staticmethod
    def element_to_rect(x):
        return pyg_rect.Rect(x.position[0], x.position[1], x.size[0], x.size[1])
