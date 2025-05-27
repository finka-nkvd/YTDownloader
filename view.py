import customtkinter as ctk
from PIL import Image
import qrcode


class MainView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_main_window()

    def _setup_main_window(self):
        self.title("Video Downloader")
        self.geometry("600x400")

        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        #поле ввода
        self.url_entry = ctk.CTkEntry(
            input_frame,
            width=400,
            placeholder_text="Введите ссылку..."
        )
        self.url_entry.pack(side="left", padx=(0, 5))

        #статус
        self.status_label = ctk.CTkLabel(self, text="", height=50, wraplength=400)
        self.status_label.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)

        #кнопка вставить
        paste_img = ctk.CTkImage(Image.open("assets/paste.png"), size=(20, 20))
        self.paste_btn = ctk.CTkButton(
            input_frame,
            image=paste_img,
            text="",
            width=30,
            command=self.controller.paste_from_clipboard
        )
        self.paste_btn.pack(side="left", padx=(0, 5))

        #кнопка загрузить
        download_img = ctk.CTkImage(Image.open("assets/download.png"), size=(20, 20))
        self.download_btn = ctk.CTkButton(
            input_frame,
            image=download_img,
            text="",
            width=30,
            fg_color="green",
            hover_color="#2AAA8A",
            command=self.controller.download_handler
        )
        self.download_btn.pack(side="left")

        #меню (Strategy pattern для обработки разных действий)
        self.menu_btn = ctk.CTkButton(
            self,
            text="Информация",
            command=self.controller.show_about
        )
        self.menu_btn.place(relx=0.95, rely=0.05, anchor=ctk.NE)

    def update_status(self, message, color):
        self.status_label.configure(text=message, text_color=color)


class AboutWindow(ctk.CTkToplevel):
    #окно о проекте (Composite pattern для группировки компонентов)
    def __init__(self, controller, total_downloads):
        super().__init__()
        self.controller = controller
        self._setup_window(total_downloads)

    def _setup_window(self, total_downloads):
        self.title("Информация")
        self.geometry("300x450")

        #генерация QR-кода
        qr = qrcode.make("https://github.com/finka-nkvd/YTDownloader")
        qr.save("assets/github_qr.png")

        #интерфейс
        self.qr_image = ctk.CTkImage(Image.open("assets/github_qr.png"), size=(200, 200))
        self.qr_label = ctk.CTkLabel(self, image=self.qr_image, text="")
        self.qr_label.pack(pady=10)

        self.link_label = ctk.CTkLabel(
            self,
            text="https://github.com/finka-nkvd/YTDownloader",
            cursor="hand2"
        )
        self.link_label.pack(pady=10)
        self.link_label.bind("<Button-1>", lambda e: self.controller.copy_to_clipboard()) #e - event, нужно для избежания type error если принимается другое событие

        self.stats_label = ctk.CTkLabel(
            self,
            text=f"Всего загрузок: {total_downloads}",
            font=("Arial", 14)
        )
        self.stats_label.pack(pady=10)

        self.theme_switch = ctk.CTkSwitch(
            self,
            text="Темная тема",
            command=self.controller.toggle_theme
        )
        self.theme_switch.pack(pady=10)