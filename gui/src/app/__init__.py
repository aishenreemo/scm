import pygame

from .config import Config
from .memory import Memory
from .command import (
    QuitCommand,
    ChangePageCommand,
)

from ..gui import Display

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
        self.screen = pygame.display.set_mode(APP_WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.delta = 0

        self.mem = Memory()
        self.cfg = Config()
        self.gui = Display()

        self.mem.update()
        self.cfg.init()
        self.gui.init()

        pygame.key.set_repeat(APP_KEYDOWN_DELAY, APP_KEYDOWN_INTERVAL)

        return

    def command(self, command_class, event):
        if command_class.check(self, event):
            instance = command_class(self, event)
            self.cmd_queue.append(instance)

        return

    def listen(self):
        if not self.running:
            return

        for event in pygame.event.get():
            self.command(QuitCommand, event)
            self.command(ChangePageCommand, event)

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

        try:
            screen = self.gui.pages[self.gui.pointer]

            for element in screen.elements:
                self.screen.blit(element.surface, element.position)

            pygame.display.flip()

        except IndexError as err:
            print("screen_ptr:", err)
            exit(1)

        return

    def tick(self):
        if not self.running:
            return

        self.delta = self.clock.tick(APP_FPS)

        return
