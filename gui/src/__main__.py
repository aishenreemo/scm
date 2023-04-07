import pygame
from .app import App


def main():
    app = App()

    pygame.init()
    pygame.font.init()

    app.init()

    while app.running:
        app.listen()
        app.render()
        app.update()
        app.tick()


if __name__ == "__main__":
    main()
