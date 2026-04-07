import customtkinter
import ui.constants as const


def alert(app, suffix=None, on_close=None):
    def close():
        alert_window.destroy()
        if on_close:
            on_close()

    alert_window = customtkinter.CTkToplevel(app)
    alert_window.title("Ошибка!")
    alert_window.geometry("300x150")
    alert_window.resizable(False, False)
    alert_window.configure(fg_color=const.COLOR_BG)
    alert_window.rowconfigure((0, 2), weight=1)
    alert_window.rowconfigure(1, weight=0)
    alert_window.columnconfigure((0, 1, 2), weight=1)

    msg = f"Ошибка: {suffix}" if suffix else ""

    label = customtkinter.CTkLabel(
        alert_window,
        text=msg,
        font=("Inter", 16, "bold"),
        text_color=const.TEXT_PRIMARY,
    )
    label.grid(row=0, column=1, sticky="EW")
    close_btn = customtkinter.CTkButton(
        alert_window,
        text="Закрыть окно",
        command=close,
        font=("Inter", 14),
        fg_color=const.BUTTON_PRIMARY_BG,
        text_color=const.TEXT_PRIMARY,
        hover_color=const.BUTTON_PRIMARY_HOVER,
    )
    close_btn.grid(row=1, column=1)
    alert_window.after(100, alert_window.lift)


def confirm(object, type, app, on_yes=None, on_no=None):
    def yes():
        confirm_window.destroy()
        if on_yes:
            on_yes()

    def no():
        confirm_window.destroy()
        if on_no:
            on_no()

    confirm_window = customtkinter.CTkToplevel(app)
    confirm_window.title("Подтверждение")
    confirm_window.geometry("600x150")
    confirm_window.configure(fg_color=const.COLOR_BG)
    confirm_window.resizable(False, False)
    confirm_window.rowconfigure((0, 2), weight=1)
    confirm_window.rowconfigure(1, weight=0)
    confirm_window.columnconfigure((0, 1, 2), weight=1)

    if type == "deck":
        name = object["name"]
        if len(name) > 60:
            name = name[:60] + "..."
        text = f'Вы уверены, что хотите удалить колоду\n"{name}"'
    elif type == "card":
        question = object["question"]
        if len(question) > 60:
            question = question[:60] + "..."
        text = f'Вы уверены, что хотите удалить карточку\n"{question}"'

    label = customtkinter.CTkLabel(
        confirm_window,
        text=text,
        font=("Inter", 16, "bold"),
        text_color=const.TEXT_PRIMARY,
    )
    label.grid(row=0, column=0, columnspan=3, sticky="EW")

    buttons = customtkinter.CTkFrame(confirm_window, fg_color=const.COLOR_BG)
    buttons.grid(row=1, column=0, sticky="EW", columnspan=3)
    buttons.rowconfigure(0, weight=1)
    buttons.columnconfigure((0, 2), weight=1)
    buttons.columnconfigure(1, weight=0)

    yes_btn = customtkinter.CTkButton(
        buttons,
        text="Да",
        command=yes,
        font=("Rubik", 14),
        fg_color=const.BUTTON_SECONDARY_BG,
        text_color=const.TEXT_PRIMARY,
        hover_color=const.BUTTON_SECONDARY_HOVER,
    )
    yes_btn.grid(row=0, column=0, sticky="E", padx=20)

    no_btn = customtkinter.CTkButton(
        buttons,
        text="Нет",
        command=no,
        font=("Rubik", 14),
        fg_color=const.BUTTON_SECONDARY_BG,
        text_color=const.TEXT_PRIMARY,
        hover_color=const.BUTTON_SECONDARY_HOVER,
    )
    no_btn.grid(row=0, column=1, sticky="W", padx=20)

    confirm_window.after(100, confirm_window.lift)


if __name__ == "__main__":
    app = customtkinter.CTk()
    app.geometry("400x150")
    s = ""
    button = customtkinter.CTkButton(
        app, text="my button", command=lambda name="", app=app: confirm(name, app)
    )
    button.pack(padx=20, pady=20)

    app.mainloop()
