class AppSettings:
    def __init__(self):
        self._theme = "system"

    #нкапсуляция геттер темы
    @property
    def theme(self):
        return self._theme

    #икапсуляция сеттер темы
    @theme.setter
    def theme(self, value):
        if value in ["light", "dark", "system"]:
            self._theme = value