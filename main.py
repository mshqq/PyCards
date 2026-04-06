# Основное приложение
from db import init_db
import customtkinter as ctk
from ui import main_window


def main() -> None:
    init_db()
    print("БД инициализирована.")

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.title("PyCards")
    app.geometry("800x600")
    app.resizable(False, False)

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    main_window.main_menu(app)
    app.mainloop()


if __name__ == "__main__":
    print("PyCards запускается...")
    main()
