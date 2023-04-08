from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from pygame.font import init as pyg_font_init
from pygame import init as pyg_init

from .app import App


def main():
    app = App()

    pyg_init()
    pyg_font_init()

    app.init()

    while app.running:
        app.listen()
        app.render()
        app.update()
        app.tick()


if __name__ == "__main__":
    main()
