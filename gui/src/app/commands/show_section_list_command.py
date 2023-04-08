from pygame import locals as pyg_locals
from pygame import rect as pyg_rect

from .command import (
    CommandType,
    Command,
)


class ShowSectionListCommand(Command):
    def __init__(self, opts):
        super().__init__(CommandType.CHANGE_PAGE)
        self.grade_level = opts

    def run(self, app):
        window = app.gui.pages[1]
        student_window = window.get_element("student_list_window")
        section_window = window.get_element("section_list_window")
        student_window.visible = False
        section_window.visible = True

    def opts(app, event):
        if pyg_locals.MOUSEBUTTONDOWN == event.type:
            if app.gui.pointer == 1:
                window = app.gui.pages[app.gui.pointer]

                elements = list(filter(ShowSectionListCommand.is_grade_level_element, window.elements))
                rects = list(map(ShowSectionListCommand.element_to_rect, elements))

                for i in range(0, len(elements)):
                    if rects[i].collidepoint(event.pos):
                        return elements[i].name.split("_")[1]

    @staticmethod
    def is_grade_level_element(element):
        return element.name.startswith("grade") and element.name.endswith("rect")

    @staticmethod
    def element_to_rect(x):
        return pyg_rect.Rect(x.position[0], x.position[1], x.size[0], x.size[1])
