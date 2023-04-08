from pygame import locals as pyg_locals
from pygame import key as pyg_key

from .command import (
    CommandType,
    Command,
)


class QuitCommand(Command):
    def __init__(self, opts):
        super().__init__(CommandType.QUIT)

    def run(self, app):
        app.running = False

    def opts(app, event):
        mods = pyg_key.get_mods()

        if (pyg_locals.QUIT == event.type) or (
            (pyg_locals.KEYDOWN == event.type) and
            (pyg_locals.K_q == event.key) and
            (pyg_locals.KMOD_CTRL & mods)
        ):
            return True

        return None
