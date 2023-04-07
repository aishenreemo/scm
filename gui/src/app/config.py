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


class Config:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Config, cls).__new__(cls)

        return cls.instance

    def init(self, colors=CONFIG_COLORSCHEME):
        self.colors = colors

        return
