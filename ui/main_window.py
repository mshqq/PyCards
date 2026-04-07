# Основное окно
import ui.constants as const

import customtkinter as ctk


def main_menu(app) -> None:
    for widget in app.winfo_children():
        widget.destroy()

    for i in range(8):
        app.grid_rowconfigure(i, weight=0)
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    app.configure(fg_color=const.COLOR_BG)

    main_Label = ctk.CTkLabel(app, text="PyCards", font=("Inter", 32, "bold"),
        text_color=const.TEXT_PRIMARY)
    main_Label.grid(row=0, column=0, sticky="nsew")

    buttons_Frame = ctk.CTkFrame(app, fg_color=const.COLOR_BG)
    buttons_Frame.grid(row=1, column=0, sticky="N")

    learning_Button = ctk.CTkButton(
        buttons_Frame,
        fg_color=const.BUTTON_PRIMARY_BG,
        text="Обучение",
        font=("Inter", 14, "bold"),
        command=lambda: open_learning(app),
        corner_radius=15,
        height=38,
        width=158,
    
        text_color=const.TEXT_PRIMARY,
        hover_color=const.BUTTON_PRIMARY_HOVER)
    learning_Button.grid(row=0, column=0, pady=(0, 15))

    editor_Button = ctk.CTkButton(
        buttons_Frame,
        fg_color=const.BUTTON_SECONDARY_BG,
        text="Редактор",
        font=("Inter", 14, "bold"),
        command=lambda: open_editor(app),
        corner_radius=15,
        height=38,
        width=158,
    
        text_color=const.TEXT_PRIMARY,
        hover_color=const.BUTTON_SECONDARY_HOVER)
    editor_Button.grid(row=1, column=0)

    info_label = ctk.CTkLabel(
        app,
        text="v0.1 by Mshqq",
        font=("Bahnschrift", 15, "bold"),
        text_color=const.TEXT_SECONDARY,
    )
    info_label.grid(row=2, column=0, pady=20)


def open_learning(app):
    from ui import review_window

    review_window.select_Window(app)


def open_editor(app):
    from ui import editor_window

    editor_window.editor_decks(app)
