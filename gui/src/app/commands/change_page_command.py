from pygame import locals as pyg_locals
from pygame import rect as pyg_rect
from pygame import key as pyg_key

from .command import (
    CommandType,
    Command,
)


class ChangePageCommand(Command):
    def __init__(self, opts):
        super().__init__(CommandType.CHANGE_PAGE)
        self.pointer = opts

    def run(self, app):
        app.gui.pointer = self.pointer

    def opts(app, event):
        mods = pyg_key.get_mods()

        if pyg_locals.KEYDOWN == event.type:
            if pyg_locals.KMOD_CTRL & mods:
                if pyg_locals.K_h == event.key:
                    if (app.gui.pointer == 0):
                        return len(app.gui.pages) - 1
                    else:
                        return app.gui.pointer - 1

                elif pyg_locals.K_l == event.key:
                    new_ptr = app.gui.pointer + 1
                    new_ptr %= len(app.gui.pages)

                    return new_ptr

        elif pyg_locals.MOUSEBUTTONDOWN == event.type:
            if app.gui.pointer == 0:
                window = app.gui.pages[app.gui.pointer]
                login_window = window.get_element("login_window")
                login_rect = login_window.get_element("login_btn")

                rect = pyg_rect.Rect(
                    login_rect.position[0] + login_window.position[0],
                    login_rect.position[1] + login_window.position[1],
                    login_rect.size[0],
                    login_rect.size[1],
                )

                if rect.collidepoint(event.pos):
                    return 1
