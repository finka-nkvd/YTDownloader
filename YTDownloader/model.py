import customtkinter as ctk


class AppSettings:
    """Хранение настроек приложения (тема)"""

    def __init__(self):
        self._theme = "system"

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        if value in ["light", "dark", "system"]:
            self._theme = value