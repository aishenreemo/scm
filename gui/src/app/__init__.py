from pygame import display as pyg_display
from pygame import event as pyg_event
from pygame import time as pyg_time
from pygame import key as pyg_key

from .config import Config
from .memory import Memory
from .commands import (
    ShowSectionListCommand,
    ShowStudentListCommand,
    ChangePageCommand,
    QuitCommand,
)

from ..ui import Display

APP_FPS = 60
APP_WINDOW_SIZE = (900, 650)
APP_KEYDOWN_DELAY = 500
APP_KEYDOWN_INTERVAL = 100


class App:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(App, cls).__new__(cls)

        return cls.instance

    def init(self):
        self.running = True
        self.cmd_queue = []
        self.screen = pyg_display.set_mode(APP_WINDOW_SIZE)
        self.clock = pyg_time.Clock()
        self.delta = 0

        self.mem = Memory()
        self.cfg = Config()
        self.gui = Display()

        self.mem.update()
        self.mem.update_lazy()
        self.cfg.init()
        self.gui.init()

        pyg_key.set_repeat(APP_KEYDOWN_DELAY, APP_KEYDOWN_INTERVAL)

        return

    def command(self, command_class, event):
        opts = command_class.opts(self, event)
        if not (opts is None):
            instance = command_class(opts)
            self.cmd_queue.append(instance)

        return

    def listen(self):
        if not self.running:
            return

        for event in pyg_event.get():
            self.command(QuitCommand, event)
            self.command(ChangePageCommand, event)
            self.command(ShowSectionListCommand, event)
            self.command(ShowStudentListCommand, event)

        return

    def update(self):
        if not self.running:
            return

        self.mem.update()
        self.gui.update()

        for command in self.cmd_queue:
            command.run(self)

        self.cmd_queue.clear()

        return

    def render(self):
        if not self.running:
            return

        if self.gui.pointer >= len(self.gui.pages):
            print("warn: gui pointer overflow")
            return

        screen = self.gui.pages[self.gui.pointer]

        for element in screen.elements:
            if not element.visible:
                continue

            self.screen.blit(element.surface, element.position)

        pyg_display.flip()

        return

    def tick(self):
        if not self.running:
            return

        self.delta = self.clock.tick(APP_FPS)

        return
