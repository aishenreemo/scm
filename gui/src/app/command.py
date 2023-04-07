import pygame
from enum import Enum


class CommandType(Enum):
    QUIT = 0
    CHANGE_PAGE = 1


class Command:
    def __init__(self, app, event, type=CommandType.QUIT):
        self.type = type

    def run(self, app):
        pass

    @staticmethod
    def check(app, event):
        pass

    @staticmethod
    def ops(app, event):
        return (None)


class QuitCommand(Command):
    def __init__(self, app, event):
        super().__init__(app, event, CommandType.QUIT)

    def run(self, app):
        app.running = False

    def check(app, event):
        mods = pygame.key.get_mods()

        return (pygame.QUIT == event.type) or (
            (pygame.KEYDOWN == event.type) and
            (pygame.K_q == event.key) and
            (pygame.KMOD_CTRL & mods)
        )


class ChangePageCommand(Command):
    def __init__(self, app, event):
        super().__init__(app, event, CommandType.CHANGE_PAGE)
        opts = ChangePageCommand.opts(app, event)
        self.pointer = opts[0]

    def run(self, app):
        app.gui.pointer = self.pointer

    def check(app, event):
        mods = pygame.key.get_mods()
        return (
            (pygame.KEYDOWN == event.type) and
            (pygame.K_h == event.key) and
            (pygame.KMOD_CTRL & mods)
        ) or (
            (pygame.KEYDOWN == event.type) and
            (pygame.K_l == event.key) and
            (pygame.KMOD_CTRL & mods)
        )

    def opts(app, event):
        mods = pygame.key.get_mods()

        if (
            (pygame.KEYDOWN != event.type) or
            (not (pygame.KMOD_CTRL & mods))
        ):
            return (None)

        if pygame.K_h == event.key:

            if (app.gui.pointer == 0):
                return (len(app.gui.pages) - 1, None)
            else:
                return (app.gui.pointer - 1, None)

        elif pygame.K_l == event.key:

            new_ptr = app.gui.pointer + 1
            new_ptr %= len(app.gui.pages)

            return (new_ptr, None)
