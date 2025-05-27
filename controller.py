import pyperclip
from model import AppSettings
from view import MainView, AboutWindow
import customtkinter as ctk
import pytube
import json
import os
import time


class MainController:
    #контроллер как переходник между model и view (Mediator pattern)"""
    def __init__(self):
        self.model = AppSettings()
        self.view = MainView(self)
        self.about_window = None

        #инициализация темы
        ctk.set_appearance_mode(self.model.theme)

    def download_handler(self):
        url = self.view.url_entry.get()
        if not url:
            self.view.update_status("Введите URL видео", "red")
            return

        try:
            start_time = time.time()
            self.view.update_status("Подключение к YouTube...", "blue")

            yt = pytube.YouTube(url)
            self.view.update_status(f"Найдено видео: {yt.title}", "blue")

            stream = yt.streams.get_highest_resolution()
            self.view.update_status("Начинаем загрузку...", "blue")

            stream.download()

            download_time = round(time.time() - start_time, 2)
            stats = DownloadStats()
            stats.increment_downloads()
            self.view.update_status(
                f"Загрузка завершена! Время: {download_time} сек",
                "green"
            )

        except Exception as e:
            self.view.update_status(f"Ошибка: {str(e)}", "red")

    def paste_from_clipboard(self):
        """Вставка URL из буфера обмена"""
        try:
            clipboard_content = pyperclip.paste()
            if clipboard_content:
                self.view.url_entry.delete(0, 'end')
                self.view.url_entry.insert(0, clipboard_content)
        except Exception as e:
            self.view.update_status(f"Ошибка вставки: {str(e)}", "red")

    def show_about(self):
        if not self.about_window or not self.about_window.winfo_exists():
            self.about_window = AboutWindow(self)

    def copy_to_clipboard(self):
        #копирование ссылки (SRP - отдельный метод для одной операции)
        pyperclip.copy("https://github.com/finka-nkvd/YTDownloader")

    def toggle_theme(self):
        #смена темы (Инкапсуляция - работа через свойства модели)
        self.model.theme = "dark" if self.model.theme == "light" else "light"
        ctk.set_appearance_mode(self.model.theme)


class DownloadStats:
    def __init__(self):
        self.stats_file = "download_stats.json"
        self.stats = self._load_stats()

    def _load_stats(self):
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        return {"total_downloads": 0}

    def increment_downloads(self):
        self.stats["total_downloads"] += 1
        self._save_stats()

    def _save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f)

    @property
    def total_downloads(self):
        return self.stats["total_downloads"]