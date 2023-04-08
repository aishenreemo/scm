from .page.student_list_page import StudentListPage
from .page.main_page import MainPage


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
