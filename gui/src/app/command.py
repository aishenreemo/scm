import pygame
from enum import Enum


class CommandType(Enum):
    QUIT = 0
    CHANGE_PAGE = 1


class Command:
    def __init__(self, type=CommandType.QUIT):
        self.type = type

    def run(self, app):
        pass

    @staticmethod
    def opts(app, event):
        return None


class QuitCommand(Command):
    def __init__(self, opts):
        super().__init__(CommandType.QUIT)

    def run(self, app):
        app.running = False

    def opts(app, event):
        mods = pygame.key.get_mods()

        if (pygame.QUIT == event.type) or (
            (pygame.KEYDOWN == event.type) and
            (pygame.K_q == event.key) and
            (pygame.KMOD_CTRL & mods)
        ):
            return True

        return None


class ChangePageCommand(Command):
    def __init__(self, opts):
        super().__init__(CommandType.CHANGE_PAGE)
        self.pointer = opts

    def run(self, app):
        app.gui.pointer = self.pointer

    def opts(app, event):
        mods = pygame.key.get_mods()

        if pygame.KEYDOWN == event.type:
            if pygame.KMOD_CTRL & mods:
                if pygame.K_h == event.key:
                    if (app.gui.pointer == 0):
                        return len(app.gui.pages) - 1
                    else:
                        return app.gui.pointer - 1

                elif pygame.K_l == event.key:
                    new_ptr = app.gui.pointer + 1
                    new_ptr %= len(app.gui.pages)

                    return new_ptr

        elif pygame.MOUSEBUTTONDOWN == event.type:
            return None
