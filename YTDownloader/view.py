import customtkinter as ctk
from PIL import Image
import qrcode


class MainView(ctk.CTk):
    """Основное окно приложения (View)"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_main_window()

    def _setup_main_window(self):
        self.title("Video Downloader")
        self.geometry("600x400")

        # Поле ввода (Builder pattern мог бы использоваться для сложных объектов)
        self.url_entry = ctk.CTkEntry(self, width=400, placeholder_text="Введите ссылку...")
        self.url_entry.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Кнопка загрузки
        download_img = ctk.CTkImage(Image.open("assets/download.png"), size=(20, 20))
        self.download_btn = ctk.CTkButton(
            self,
            image=download_img,
            text="",
            width=30,
            fg_color="green",
            hover_color="#2AAA8A",
            command=self.controller.download_handler
        )
        self.download_btn.place(relx=0.7, rely=0.5, anchor=ctk.CENTER)

        # Меню (Strategy pattern для обработки разных действий)
        self.menu_btn = ctk.CTkButton(
            self,
            text="О проекте",
            command=self.controller.show_about
        )
        self.menu_btn.place(relx=0.95, rely=0.05, anchor=ctk.NE)


class AboutWindow(ctk.CTkToplevel):
    """Окно 'О проекте' (Composite pattern для группировки компонентов)"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_window()

    def _setup_window(self):
        self.title("О проекте")
        self.geometry("300x400")

        # Генерация QR-кода
        qr = qrcode.make("https://github.com/finka-nkvd/YTDownloader")
        qr.save("assets/github_qr.png")

        # Элементы интерфейса
        self.qr_image = ctk.CTkImage(Image.open("assets/github_qr.png"), size=(200, 200))
        self.qr_label = ctk.CTkLabel(self, image=self.qr_image, text="")
        self.qr_label.pack(pady=10)

        self.link_label = ctk.CTkLabel(
            self,
            text="https://github.com/finka-nkvd/YTDownloader",
            cursor="hand2"
        )
        self.link_label.pack(pady=10)
        self.link_label.bind("<Button-1>", lambda e: self.controller.copy_to_clipboard())

        self.theme_switch = ctk.CTkSwitch(
            self,
            text="Темная тема",
            command=self.controller.toggle_theme
        )
        self.theme_switch.pack(pady=10)