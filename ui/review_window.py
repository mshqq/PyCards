# Окно просмотра
# Основное окно
import customtkinter as ctk
import ui.constants as const


def show(app) -> None:
    for widget in app.winfo_children():
        widget.destroy()

    main_frame = ctk.CTkFrame(master=app, fg_color=const.BG_FRAME)
    main_frame.grid(row=0, column=0, sticky="nsew")

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure((0, 4), weight=1)

    title_label = ctk.CTkLabel(
        main_frame,
        text="Обучение",
        font=("Bahnschrift", 38, "bold"),
        text_color=const.TEXT_PRIMARY,
    )
    title_label.grid(row=0, column=0, padx=20, pady=10)

    btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    btn_frame.grid(row=3, column=0, pady=(0, 10))

    button_learning = ctk.CTkButton(
        master=btn_frame,
        text="Обучение",
        font=("Segoe UI", 14),
        fg_color=const.ACCENT,
        hover_color=const.ACCENT_HOVER,
        text_color=const.BG_DARK,
        corner_radius=10,
        height=const.BTN_HEIGHT,
        width=const.BTN_WIDTH,
        command=lambda: open_learning(app),
    )
    button_learning.grid(row=0, column=0, padx=8)

    button_editor = ctk.CTkButton(
        master=btn_frame,
        text="Редактор",
        font=("Segoe UI", 14),
        fg_color=const.ACCENT,
        hover_color=const.ACCENT_HOVER,
        text_color=const.BG_DARK,
        corner_radius=10,
        height=const.BTN_HEIGHT,
        width=const.BTN_WIDTH,
        command=lambda: open_editor(app),
    )
    button_editor.grid(row=2, column=0, pady=10)

    info_label = ctk.CTkLabel(
        main_frame,
        text="v0.1 by Mshqq",
        font=("Bahnschrift", 15, "bold"),
        text_color=const.TEXT_MUTED,
    )
    info_label.grid(row=4, column=0, pady=20)


def open_learning(app):
    from ui import review_window

    review_window.show(app)
    print("Кнопка 'Обучение' нажата")


def open_editor(app):
    from ui import editor_window

    editor_window.show(app)
    print("Кнопка 'Редактор' нажата")
