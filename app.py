import customtkinter as ctk

from configurations import InterfaceConfig
from interfaces.interface import Interface


def initialize_application():
    """Initialize the application with default settings."""
    ctk.set_appearance_mode(InterfaceConfig.THEME)
    ctk.set_default_color_theme(InterfaceConfig.THEME_COLOR)
    app = Interface()
    app.mainloop()


if __name__ == "__main__":
    initialize_application()
