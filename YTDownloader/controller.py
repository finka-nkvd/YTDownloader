import pyperclip
from model import AppSettings
from view import MainView, AboutWindow
import customtkinter as ctk


class MainController:
    """Основной контроллер (Mediator pattern)"""

    def __init__(self):
        self.model = AppSettings()
        self.view = MainView(self)
        self.about_window = None

        # Инициализация темы
        ctk.set_appearance_mode(self.model.theme)

    def download_handler(self):
        """Обработчик загрузки (Command pattern)"""
        url = self.view.url_entry.get()
        print(f"Processing URL: {url}")  # Заглушка для реальной логики

    def show_about(self):
        """Открытие окна 'О проекте'"""
        if not self.about_window or not self.about_window.winfo_exists():
            self.about_window = AboutWindow(self)

    def copy_to_clipboard(self):
        """Копирование ссылки (SRP - отдельный метод для одной операции)"""
        pyperclip.copy("https://github.com/finka-nkvd/YTDownloader")

    def toggle_theme(self):
        """Смена темы (Инкапсуляция - работа через свойства модели)"""
        self.model.theme = "dark" if self.model.theme == "light" else "light"
        ctk.set_appearance_mode(self.model.theme)