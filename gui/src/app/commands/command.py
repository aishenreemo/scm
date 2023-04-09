from enum import Enum


class CommandType(Enum):
    QUIT = 0
    CHANGE_PAGE = 1
    SHOW_SECTION_LIST_COMMAND = 2
    SHOW_STUDENT_LIST_COMMAND = 3


class Command:
    def __init__(self, type=CommandType.QUIT):
        self.type = type

    def run(self, app):
        pass

    @staticmethod
    def opts(app, event):
        return None
