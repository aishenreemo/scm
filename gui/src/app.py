###########
# IMPORTS #
###########
from pygame import transform as pyg_transform
from pygame import surface as pyg_surface
from pygame import display as pyg_display
from pygame import locals as pyg_locals
from pygame import image as pyg_image
from pygame import event as pyg_event
from pygame import font as pyg_font
from pygame import draw as pyg_draw
from pygame import rect as pyg_rect
from pygame import time as pyg_time
from pygame import key as pyg_key
from pygame.sprite import Sprite

from requests import get as req_get

from enum import Enum


#############
# CONSTANTS #
#############
APP_FPS = 60
APP_WINDOW_SIZE = (900, 650)
APP_KEYDOWN_DELAY = 500
APP_KEYDOWN_INTERVAL = 100

CONFIG_COLORSCHEME = {
    "background":  "#0B0F10",
    "foreground":  "#c5c8c9",
    "normal": {
        "black":   "#131718",
        "red":     "#df5b61",
        "green":   "#87c7a1",
        "yellow":  "#de8f78",
        "blue":    "#004AAD",
        "magenta": "#bc83e3",
        "cyan":    "#70b9cc",
        "white":   "#c4c4c4",
    },
    "bright": {
        "black":   "#151a1c",
        "red":     "#ee6a70",
        "green":   "#96d6b0",
        "yellow":  "#ffb29b",
        "blue":    "#7ba5dd",
        "magenta": "#cb92f2",
        "cyan":    "#7fc8db",
        "white":   "#cccccc",
    },
}


#######
# APP #
#######
class App:
    # singleton pattern
    # https://en.wikipedia.org/wiki/Singleton_pattern
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(App, cls).__new__(cls)

        return cls.instance

    # only run this method once cus this is a singleton
    # do `App()` to access the global instance
    # same applies for other singletons (Memory, Config, Display, etc)
    def init(self):
        self.memory = Memory()
        self.config = Config()
        self.display = Display()

        self.config.init()
        self.display.init()
        self.memory.init()
        self.display.change_page(PageType.LOGIN)

        self.running = True
        self.commands = []
        self.clock = pyg_time.Clock()

        # control how held keys are repeated
        pyg_key.set_repeat(APP_KEYDOWN_DELAY, APP_KEYDOWN_INTERVAL)

        return

    def listen(self):
        if not self.running:
            return

        # get events from queue
        for event in pyg_event.get():
            for command_type in range(0, CommandType.LAST.value):
                # check if the event can trigger
                # this type of command... if so,
                # then run it
                self.command(command_type, event)

        return

    def update(self):
        if not self.running:
            return

        # i don't need to explain
        # self-explanatory lines right?
        self.memory.update()

        for command in self.commands:
            command.run()

        self.commands.clear()

        return

    def render(self):
        if not self.running:
            return

        # draw stuff to screen
        self.display.screen.fill((0, 0, 0))
        self.display.flush()
        pyg_display.flip()

        return

    def tick(self):
        if not self.running:
            return

        self.clock.tick(APP_FPS)

        return

    def command(self, type, event):
        command_class = CommandType.get_class(type)

        if command_class is None:
            return

        options = command_class.options(event)

        # options is None if it's not triggerable
        if options is not None:
            # push an instance to command queue
            instance = command_class(options)
            self.commands.append(instance)

        return


##########
# MEMORY #
##########
class Memory:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Memory, cls).__new__(cls)

        return cls.instance

    def init(self):
        self.window_size = pyg_display.get_surface().get_size()
        self.database = {}
        self.student = None

        return

    def update(self):
        self.window_size = pyg_display.get_surface().get_size()

        return


##########
# CONFIG #
##########
class Config:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Config, cls).__new__(cls)

        return cls.instance

    def init(self, colors=CONFIG_COLORSCHEME):
        self.colors = colors
        self.debug = True

        return


###########
# DISPLAY #
###########
class Display:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Display, cls).__new__(cls)

        return cls.instance

    def init(self):
        self.screen = pyg_display.set_mode(APP_WINDOW_SIZE)
        self.page = None

        return

    def change_page(self, type):
        page_class = PageType.get_class(type)

        if page_class is not None:
            self.page = page_class()

        return

    def flush(self):
        for element in self.page.elements:
            if not element.visible:
                continue
            elif element.surface is None:
                continue
            elif element.type == ElementType.RECT:
                element.flush()

            self.screen.blit(element.surface, element.position)

        return


############
# COMMANDS #
############
class CommandType(Enum):
    QUIT = 0
    CHANGE_PAGE = 1
    SHOW_SECTION_LIST = 2
    SHOW_STUDENT_LIST = 3
    LAST = 4

    @staticmethod
    def get_class(type):
        if type == CommandType.QUIT.value:
            return QuitCommand
        elif type == CommandType.CHANGE_PAGE.value:
            return ChangePageCommand
        elif type == CommandType.SHOW_SECTION_LIST.value:
            return ShowSectionListCommand
        elif type == CommandType.SHOW_STUDENT_LIST.value:
            return ShowStudentListCommand
        else:
            return None


class Command:
    def __init__(self, type):
        self.type = type

        return

    def run(self):
        pass

    @staticmethod
    def options(event):
        pass


class QuitCommand(Command):
    def __init__(self, options):
        super().__init__(CommandType.QUIT)

        return

    def run(self):
        app = App()
        app.running = False

        return

    @staticmethod
    def options(event):
        # if os closed the client
        if pyg_locals.QUIT == event.type:
            return True

        # if user pressed Ctrl-Q
        if (
            (pyg_locals.KMOD_CTRL & pyg_key.get_mods()) and
            (pyg_locals.KEYDOWN == event.type) and
            (pyg_locals.K_q == event.key)
        ):
            return True

        # dont quit!
        return None


class ChangePageCommand(Command):
    def __init__(self, options):
        super().__init__(CommandType.CHANGE_PAGE)
        self.page_type = options

        return

    def run(self):
        app = App()
        app.display.change_page(self.page_type)

        return

    @staticmethod
    def options(event):
        app = App()

        # check if user clicked the mouse
        if pyg_locals.MOUSEBUTTONDOWN == event.type:
            # if the page is not LOGIN page
            if app.display.page.type != PageType.LOGIN:
                return

            window = app.display.page.element("login")
            button = window.element("button")

            rect = pyg_rect.Rect(
                button.position[0] + window.position[0],
                button.position[1] + window.position[1],
                button.size[0],
                button.size[1],
            )

            # if user clicked the login button
            if rect.collidepoint(event.pos):
                return PageType.STUDENT_LIST

        if not app.config.debug:
            return None

        # check if user pressed a key
        if event.type == pyg_locals.KEYDOWN:
            # if user is not pressing CTRL
            is_ctrl = pyg_locals.KMOD_CTRL & pyg_key.get_mods()

            # if user pressed CTRL-h
            if (pyg_locals.K_h == event.key) and is_ctrl:
                if app.display.page.type == PageType(0):
                    return PageType(PageType.LAST.value - 1)
                else:
                    return PageType(app.display.page.type.value - 1)

            # if user pressed CTRL-l
            if (pyg_locals.K_l == event.key) and is_ctrl:
                new_page = app.display.page.type.value + 1
                new_page %= PageType.LAST.value

                return PageType(new_page)

        return None


class ShowSectionListCommand(Command):
    def __init__(self, options):
        super().__init__(CommandType.SHOW_SECTION_LIST)
        self.grade_level = options

        return

    def run(self):
        display = Display()
        memory = Memory()
        config = Config()

        student_list = display.page.element("student_list")
        section_list = display.page.element("section_list")
        student_list.visible = False
        section_list.visible = True

        main_rect = section_list.element("rect")
        main_rect.elements.clear()
        main_rect.draw(0, config.colors["foreground"])
        main_rect.draw(1, config.colors["background"])

        memory_key = f"sections_{self.grade_level}"
        if memory_key not in memory.database:
            api_url = f"http://localhost:3000/sections/{self.grade_level}"
            memory.database[memory_key] = req_get(api_url).json()

        for i, section in enumerate(memory.database[memory_key]):
            main_rect.elements.append(TextElement(
                f"{section.lower}_item",
                main_rect.percent(6, 5 + i * 6),
                f"{self.grade_level} {section}",
                20,
                config.colors["background"],
            ))

        return

    @staticmethod
    def options(event):
        app = App()

        if pyg_locals.MOUSEBUTTONDOWN != event.type:
            return None

        if app.display.page.type != PageType.STUDENT_LIST:
            return None

        for element in app.display.page.elements:
            if not element.name.startswith("grade_"):
                continue

            if not element.name.endswith("_rect"):
                continue

            rect = pyg_rect.Rect(
                element.position[0],
                element.position[1],
                element.size[0],
                element.size[1],
            )

            if rect.collidepoint(event.pos):
                return int(element.name.split("_")[1])

        return None


class ShowStudentListCommand(Command):
    def __init__(self, options):
        super().__init__(CommandType.SHOW_STUDENT_LIST)
        self.grade_level = options[0]
        self.section = options[1]

        return

    def run(self):
        display = Display()
        memory = Memory()
        config = Config()

        student_list = display.page.element("student_list")
        section_list = display.page.element("section_list")
        student_list.visible = True
        section_list.visible = False

        boys = student_list.element("boys")
        boys.elements.clear()
        boys.draw(0, config.colors["foreground"])
        boys.draw(1, config.colors["background"])

        girls = student_list.element("girls")
        girls.elements.clear()
        girls.draw(0, config.colors["foreground"])
        girls.draw(1, config.colors["background"])

        memory_key = f"students_{self.grade_level}_{self.section.lower()}"
        if memory_key not in memory.database:
            api_url = f"http://localhost:3000/students/{self.grade_level}/{self.section}"
            memory.database[memory_key] = req_get(api_url).json()

        boys_count = 0
        girls_count = 0
        for student in memory.database[memory_key]:
            name = student["name"]

            if student["gender"] == 0:
                boys.elements.append(TextElement(
                    name["first"].lower() + "_" + name["last"].lower() + "_item",
                    boys.percent(6, 5 + boys_count * 6),
                    name["last"] + " " + name["first"] + " " + name["middle"],
                    13,
                    config.colors["background"],
                ))
                boys_count += 1
            else:
                girls.elements.append(TextElement(
                    name["first"].lower() + "_" + name["last"].lower() + "_item",
                    girls.percent(6, 5 + girls_count * 6),
                    name["last"] + " " + name["first"] + " " + name["middle"],
                    13,
                    config.colors["background"],
                ))
                girls_count += 1

        return

    @staticmethod
    def options(event):
        app = App()

        if pyg_locals.MOUSEBUTTONDOWN != event.type:
            return None

        if app.display.page.type != PageType.STUDENT_LIST:
            return None

        section_list = app.display.page.element("section_list")

        if not section_list.visible:
            return None

        main_rect = section_list.element("rect")

        for element in main_rect.elements:
            rect = pyg_rect.Rect(
                element.position[0] + section_list.position[0] + main_rect.position[0],
                element.position[1] + section_list.position[1] + main_rect.position[1],
                element.size[0],
                element.size[1],
            )

            if not rect.collidepoint(event.pos):
                continue

            return [
                int(element.text.split(" ")[0]),
                str(element.text.split(" ")[1]),
            ]


#########
# PAGES #
#########
class PageType(Enum):
    LOGIN = 0
    STUDENT_LIST = 1
    STUDENT_INFO = 2
    LAST = 3

    @staticmethod
    def get_class(type):
        if type == PageType.LOGIN:
            return LoginPage
        elif type == PageType.STUDENT_LIST:
            return StudentListPage
        elif type == PageType.STUDENT_INFO:
            return StudentInfoPage
        else:
            return None


class Page:
    def __init__(self, type):
        self.type = type
        self.elements = []

        self.elements.append(ImageElement(
            "background",
            self.percent(100, 100),
            self.percent(0, 0),
            "assets/images/background.png",
        ))

        return

    def percent(self, x, y):
        memory = Memory()
        return (
            memory.window_size[0] * (x / 100),
            memory.window_size[1] * (y / 100),
        )

    def element(self, name):
        for element in self.elements:
            if element.name == name:
                return element

        return None

    def last(self):
        if len(self.elements) == 0:
            return None

        return self.elements[-1]


class LoginPage(Page):
    def __init__(self):
        super().__init__(PageType.LOGIN)
        colors = Config().colors

        self.elements.append(ImageElement(
            "logo",
            self.percent(50, 30),
            self.percent(25, 5),
            "assets/images/logo.png",
        ))

        self.login_init(colors)

        return

    def login_init(self, colors):
        login = RectElement(
            "login",
            self.percent(30, 50),
            self.percent(35, 40),
        )

        login.draw(0, colors["normal"]["blue"], 20)
        login.draw(1, colors["background"], 20)

        login.elements.append(ImageElement(
            "logo",
            login.percent(50, 40),
            login.percent(25, 5),
            "assets/images/logo_small.png",
        ))

        login.elements.append(RectElement(
            "username",
            login.percent(90, 8),
            login.percent(5, 50),
        ))
        login.last().draw(0, colors["normal"]["white"], 5)
        login.last().draw(1, colors["background"], 5)

        login.elements.append(RectElement(
            "password",
            login.percent(90, 8),
            login.percent(5, 60),
        ))
        login.last().draw(0, colors["normal"]["white"], 5)
        login.last().draw(1, colors["background"], 5)

        login.elements.append(RectElement(
            "button",
            login.percent(60, 8),
            login.percent(20, 70),
        ))
        login.last().draw(0, colors["bright"]["blue"], 5)
        login.last().draw(1, colors["background"], 5)
        login.last().elements.append(TextElement(
            "text",
            login.last().percent(35, 20),
            "LOGIN",
            16,
            colors["background"],
        ))

        self.elements.append(login)

        return


class StudentListPage(Page):
    def __init__(self):
        super().__init__(PageType.STUDENT_LIST)
        colors = Config().colors

        self.elements.append(ImageElement(
            "logo",
            self.percent(12.5, 17.5),
            self.percent(02.5, 02.5),
            "assets/images/logo_small.png"
        ))

        self.elements.append(TextElement(
            "title",
            self.percent(17.5, 5),
            "School Clinic Management System",
            34,
            colors["background"],
        ))

        self.elements.append(ImageElement(
            "menu",
            self.percent(5, 6),
            self.percent(90, 5),
            "assets/images/menu.png",
        ))

        self.elements.append(RectElement(
            "search",
            self.percent(50, 5),
            self.percent(25, 12),
            colors["normal"]["white"]
        ))
        self.last().draw(1, colors["background"])

        self.student_list_init(colors)
        self.section_list_init(colors)

        for i in range(0, 6):
            self.elements.append(RectElement(
                "grade_" + str(i + 7) + "_rect",
                self.percent(30, 10),
                self.percent(5, 25 + (i * 12)),
                colors["normal"]["white"],
            ))
            self.last().draw(1, colors["background"])
            self.last().elements.append(TextElement(
                "grade_" + str(i + 7) + "_text",
                self.last().percent(25, 30),
                "GRADE " + str(i + 7),
                26,
                colors["background"],
            ))

        return

    def student_list_init(self, colors):
        window = RectElement(
            "student_list",
            self.percent(50, 70),
            self.percent(40, 25),
            colors["foreground"],
            visible=False,
        )

        window.draw(1, colors["background"])

        window.elements.append(RectElement(
            "boys_title",
            window.percent(46, 10),
            window.percent(2, 2),
            colors["normal"]["blue"],
        ))
        window.last().draw(1, colors["background"])
        window.last().elements.append(TextElement(
            "text",
            window.last().percent(30, 20),
            "BOYS",
            24,
            colors["background"],
        ))

        window.elements.append(RectElement(
            "girls_title",
            window.percent(46, 10),
            window.percent(52, 2),
            colors["normal"]["magenta"],
        ))
        window.last().draw(1, colors["background"])
        window.last().elements.append(TextElement(
            "text",
            window.last().percent(30, 20),
            "GIRLS",
            24,
            colors["background"],
        ))

        window.elements.append(RectElement(
            "boys",
            window.percent(46, 80),
            window.percent(2, 15),
        ))
        window.last().draw(1, colors["background"])

        window.elements.append(RectElement(
            "girls",
            window.percent(46, 80),
            window.percent(52, 15),
        ))
        window.last().draw(1, colors["background"])

        self.elements.append(window)
        return

    def section_list_init(self, colors):
        window = RectElement(
            "section_list",
            self.percent(50, 70),
            self.percent(40, 25),
            colors["foreground"],
            visible=False,
        )

        window.draw(1, colors["background"])

        window.elements.append(RectElement(
            "rect",
            window.percent(95, 95),
            window.percent(2.5, 2.5),
        ))
        window.last().draw(1, colors["background"])

        self.elements.append(window)

        return


class StudentInfoPage(Page):
    def __init__(self):
        super().__init__(PageType.STUDENT_INFO)

        return


############
# ELEMENTS #
############
class ElementType(Enum):
    RECT = 0
    TEXT = 1
    IMAGE = 2


class Element(Sprite):
    def __init__(self, name, size, position, type):
        super().__init__()
        self.name = name
        self.type = type
        self.size = size
        self.position = position
        self.visible = True
        self.surface = None

        return


class RectElement(Element):
    def __init__(self, name, size, position, color=None, visible=True):
        super().__init__(name, size, position, ElementType.RECT)
        self.visible = visible
        self.elements = []

        self.surface = pyg_surface.Surface(size).convert_alpha()
        self.color = color or [0, 0, 0, 0]

        self.draw()

        return

    def draw(self, width=0, color=None, border_radius=0, border_custom_radius=(-1, -1, -1, -1)):
        pyg_draw.rect(
            self.surface,
            color or self.color,
            self.surface.get_rect(),
            width,
            border_radius,
            border_custom_radius[0],
            border_custom_radius[1],
            border_custom_radius[2],
            border_custom_radius[3],
        )

        return

    def percent(self, x, y):
        return (
            self.size[0] * (x / 100),
            self.size[1] * (y / 100),
        )

    def element(self, name):
        for element in self.elements:
            if element.name == name:
                return element

        return None

    def flush(self):
        if self.surface is None:
            return

        for element in self.elements:
            if not element.visible:
                continue
            elif element.surface is None:
                continue
            if element.type == ElementType.RECT:
                element.flush()

            self.surface.blit(element.surface, element.position)

        return

    def last(self):
        if len(self.elements) == 0:
            return None

        return self.elements[-1]


class TextElement(Element):
    def __init__(self, name, position, text="Hello World!", points=12, color=(0, 0, 0)):
        super().__init__(name, (0, 0), position, ElementType.TEXT)
        self.family = pyg_font.get_default_font()
        self.text = text
        self.points = points

        self.color = color
        self.font = pyg_font.Font(self.family, self.points)
        self.surface = self.font.render(self.text, False, self.color)
        self.size = (self.surface.get_width(), self.surface.get_height())

        return


class ImageElement(Element):
    def __init__(self, name, size, position, path):
        super().__init__(name, size, position, ElementType.IMAGE)

        self.path = path
        self.image = pyg_image.load(path)
        self.surface = pyg_transform.scale(self.image, self.size)

        return


#######
# EOF #
#######
