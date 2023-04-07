from .page import (
    MainPage,
    StudentListPage,
)


class Display:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Display, cls).__new__(cls)

        return cls.instance

    def init(self):
        self.pages = []
        self.pointer = 0

        self.pages.append(MainPage())
        self.pages.append(StudentListPage())

        return

    def update(self):

        return
