# Окно редактора
# Основное окно
from ui import main_window
import customtkinter as ctk

from ui.utils import alert
from PIL import Image

import ui.constants as const
# import constants as const

import sys
import chardet
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from importer import load_deck, save_deck

from deck_model import (
    _get_decks_with_counts,
    _delete_deck,
    _rename_deck,
    _create_deck,
    _get_deck_by_id,
    _get_all_decks,
)
from card_model import _get_cards_by_deck, _delete_card, _update_card, _create_card

IMG_ARROW = ctk.CTkImage(Image.open("icons/arrow.png"), size=(16, 12))
IMG_DELETE = ctk.CTkImage(Image.open("icons/Delete_png.png"), size=(20, 20))
IMG_SETTINGS = ctk.CTkImage(Image.open("icons/settings-2.png"), size=(20, 20))


# Редактор колод
def editor_decks(app, reload=None) -> None:
    def back():
        main_window.main_menu(app)

    app.configure(fg_color=const.COLOR_BG)
    app.title("PyCards - Редактор колод")

    if reload:
        for widget in app.winfo_children():
            widget.destroy()

    for i in range(8):
        app.grid_rowconfigure(i, weight=0)
    app.grid_columnconfigure(0, weight=1)

    # header_frame
    header_frame = ctk.CTkFrame(
        master=app, height=38, width=740, fg_color=const.COLOR_BG
    )
    header_frame.grid(row=0, column=0, pady=15, sticky="EW", padx=20)
    header_frame.rowconfigure(0, weight=1)
    header_frame.columnconfigure((0, 1, 2), weight=1)
    header_frame.columnconfigure(0, weight=0)

    # Кнопка "Назад"
    back_button = ctk.CTkButton(
        master=header_frame,
        image=IMG_ARROW,
        text="",
        width=30,
        height=30,
        fg_color="transparent",
        hover_color="#27272A",
        command=lambda: back(),
        font=("Inter", 18, "bold"),
    )
    back_button.grid(row=0, column=0, sticky="W", padx=10)

    # Заголовок "Колоды"
    decks_label = ctk.CTkLabel(
        master=header_frame, text="Колоды", font=("Inter", 24, "bold")
    )
    decks_label.grid(row=0, column=1, sticky="W")

    # Кнопка "Создать"
    create_button = ctk.CTkButton(
        master=header_frame,
        text="+ Создать",
        fg_color="#155DFC",
        hover_color="#1447E6",
        font=("Inter", 16, "bold"),
        corner_radius=15,
        height=38,
        width=92,
        command=lambda app=app: create_deck(app),
    )
    create_button.grid(row=0, column=2, sticky="E", padx=10)

    # Фрейм под колоды
    decks_frame = ctk.CTkScrollableFrame(
        master=app,
        width=760,
        height=500,
        fg_color=const.COLOR_BG,
        scrollbar_button_color="#303037",
    )
    decks_frame.grid(row=1, column=0, padx=20, sticky="EW")

    decks_list = _get_decks_with_counts()
    for index, deck in enumerate(decks_list):
        # Фрейм под колоду
        deck_frame = ctk.CTkFrame(
            master=decks_frame,
            fg_color="#242427",
            height=90,
            width=730,
            border_width=2,
            border_color="#303037",
            corner_radius=15,
        )
        deck_frame.grid(
            row=1 + index, column=0, columnspan=8, sticky="EW", padx=5, pady=5
        )
        deck_frame.grid_columnconfigure(2, weight=1)
        deck_frame.grid_rowconfigure(0, weight=1)
        deck_frame.grid_propagate(False)

        # Название колоды
        name_label = ctk.CTkLabel(
            master=deck_frame, text=deck["name"], font=("Inter", 16, "bold")
        )
        name_label.grid(row=0, column=0, padx=(15, 10))

        # Количество карточек в колоде
        quantity_label = ctk.CTkLabel(
            master=deck_frame,
            text=deck["card_count"],
            font=("Inter", 12),
            text_color=const.TEXT_SECONDARY,
        )
        quantity_label.grid(row=0, column=1, sticky="W")

        # Фрейм под кнопки
        buttons_frame = ctk.CTkFrame(master=deck_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=2, sticky="E", padx=5)
        buttons_frame.rowconfigure(0, weight=1)
        buttons_frame.columnconfigure(2, weight=1)

        # Кнопка "Открыть"
        open_button = ctk.CTkButton(
            master=buttons_frame,
            font=("Inter", 14),
            text="Открыть",
            height=37,
            width=86,
            corner_radius=15,
            text_color=const.WHITE,
            fg_color=const.BUTTON_SECONDARY_BG,
            hover_color="#51515C",
            command=lambda deck=deck, app=app: editor_cards(app, deck),
        )
        open_button.grid(row=0, column=1)

        # Кнопка "Настройки"
        settings_button = ctk.CTkButton(
            master=buttons_frame,
            font=("Inter", 14),
            text="Настройки",
            height=37,
            width=98,
            corner_radius=15,
            text_color=const.WHITE,
            fg_color=const.BUTTON_SECONDARY_BG,
            hover_color="#51515C",
            command=lambda d=deck: settings_deck(d, app),
        )
        settings_button.grid(row=0, column=2, padx=5)

        # Кнопка "Удалить"
        delete_button = ctk.CTkButton(
            master=buttons_frame,
            font=("Inter", 14),
            text="Удалить",
            height=37,
            width=85,
            corner_radius=15,
            fg_color=const.BUTTON_DELETE_BG,
            text_color=const.BUTTON_DELETE_TEXT,
            hover_color="#51282C",
            command=lambda id=deck: delete_deck(id, app),
        )
        delete_button.grid(row=0, column=3)


# Модальное окно создания колоды
def create_deck(app):
    def cancel():
        createDeck_TopUp.destroy()
        createDeck_TopUp.update()

    def create():
        name = input_Entry.get()
        if name == "":
            alert(createDeck_TopUp, "Пустой ввод.")
            return

        result = _create_deck(name)

        if result is None:
            alert(createDeck_TopUp, "Имя занято.")
            return

        createDeck_TopUp.destroy()
        createDeck_TopUp.update()
        editor_decks(app, reload=True)

    # Модальное окно создания колоды
    createDeck_TopUp = ctk.CTkToplevel(app)
    createDeck_TopUp.title("Создать колоду")
    createDeck_TopUp.geometry("490x250")
    createDeck_TopUp.configure(fg_color=const.COLOR_BG, corner_radius=15)
    createDeck_TopUp.resizable(False, False)
    createDeck_TopUp.rowconfigure((0, 1, 2), weight=0)
    createDeck_TopUp.columnconfigure(0, weight=1)

    # Шапка
    header_Frame = ctk.CTkFrame(createDeck_TopUp, fg_color=const.COLOR_BG, height=64)
    header_Frame.grid(row=0, column=0, padx=15, pady=10, sticky="EW")
    header_Frame.rowconfigure(0, weight=0)
    header_Frame.columnconfigure(0, weight=1)
    header_Frame.columnconfigure(1, weight=0)

    header_Label = ctk.CTkLabel(
        header_Frame, text="Создать колоду", font=("Inter", 16, "bold")
    )
    header_Label.grid(row=0, column=0, sticky="W")

    header_Button = ctk.CTkButton(
        header_Frame,
        text="X",
        height=20,
        width=20,
        font=("Inter", 16, "bold"),
        fg_color="transparent",
        command=lambda: cancel(),
    )
    header_Button.grid(row=0, column=1, sticky="E")

    # Поле ввода
    input_Frame = ctk.CTkFrame(createDeck_TopUp, fg_color=const.COLOR_BG)
    input_Frame.grid(row=1, column=0, padx=15, pady=(25, 0))

    input_Label = ctk.CTkLabel(input_Frame, text="Название колоды", font=("Inter", 14))
    input_Label.grid(row=0, column=0, sticky="W", pady=5)

    input_Entry = ctk.CTkEntry(
        input_Frame,
        placeholder_text="Например: Английские слова",
        placeholder_text_color=const.TEXT_SECONDARY,
        width=454,
        height=50,
        corner_radius=15,
        fg_color=const.ENTRY_BG,
        border_color=const.FRAME_BORDER,
    )
    input_Entry.grid(row=1, column=0, sticky="W")

    # Кнопки
    buttons_Frame = ctk.CTkFrame(createDeck_TopUp, fg_color=const.COLOR_BG)
    buttons_Frame.grid(row=2, column=0, sticky="E", padx=15, pady=31)

    cancel_Button = ctk.CTkButton(
        buttons_Frame,
        text="Отмена",
        font=("Inter", 14),
        height=39,
        width=86,
        corner_radius=15,
        fg_color=const.BUTTON_SECONDARY_BG,
        text_color=const.BUTTON_SECONDARY_TEXT,
        command=lambda: cancel(),
    )
    cancel_Button.grid(row=0, column=0, padx=10)

    create_Button = ctk.CTkButton(
        buttons_Frame,
        text="Создать",
        font=("Inter", 14, "bold"),
        height=39,
        width=84,
        corner_radius=15,
        fg_color=const.BUTTON_PRIMARY_BG,
        text_color=const.BUTTON_PRIMARY_TEXT,
        command=lambda: create(),
    )
    create_Button.grid(row=0, column=1)

    createDeck_TopUp.after(100, createDeck_TopUp.lift)


# Модальное окно подтверждения удаления колоды
def delete_deck(deck, app):
    def cancel():
        confirmation_TopUp.destroy()
        confirmation_TopUp.update()

    def delete():
        _delete_deck(deck["id"])

        confirmation_TopUp.destroy()
        confirmation_TopUp.update()

        editor_decks(app, True)

    # Модальное окно подтверждения удаления колоды
    confirmation_TopUp = ctk.CTkToplevel(app)
    confirmation_TopUp.title("Удалить колоду")
    confirmation_TopUp.geometry("490x250")
    confirmation_TopUp.configure(fg_color=const.COLOR_BG)
    confirmation_TopUp.resizable(False, False)
    confirmation_TopUp.rowconfigure((0, 1, 2), weight=0)
    confirmation_TopUp.columnconfigure(0, weight=1)

    # Шапка
    header_Frame = ctk.CTkFrame(confirmation_TopUp, fg_color=const.COLOR_BG, height=64)
    header_Frame.grid(row=0, column=0, padx=15, pady=10, sticky="EW")
    header_Frame.rowconfigure(0, weight=0)
    header_Frame.columnconfigure(0, weight=1)
    header_Frame.columnconfigure(1, weight=0)

    header_Label = ctk.CTkLabel(
        header_Frame, text="Удалить колоду", font=("Inter", 16, "bold")
    )
    header_Label.grid(row=0, column=0, sticky="W")

    header_Button = ctk.CTkButton(
        header_Frame,
        text="X",
        height=20,
        width=20,
        font=("Inter", 16, "bold"),
        fg_color="transparent",
        command=lambda: cancel(),
    )
    header_Button.grid(row=0, column=1, sticky="E")

    # Формируем сообщение
    text = f'Удалить колоду "{deck["name"]}" и все её карточки?\nЭто действие нельзя отменить.'

    # Описание окна
    confirmation_Label = ctk.CTkLabel(
        confirmation_TopUp,
        text=text,
        font=("Inter", 14),
        wraplength=450,
        anchor="w",
        justify="left",
    )
    confirmation_Label.grid(row=1, column=0, padx=15, pady=(36, 0), sticky="EW")

    # Кнопки
    buttons_Frame = ctk.CTkFrame(confirmation_TopUp, fg_color=const.COLOR_BG)
    buttons_Frame.grid(row=2, column=0, sticky="E", padx=15, pady=60)

    cancel_Button = ctk.CTkButton(
        buttons_Frame,
        text="Отмена",
        font=("Inter", 14),
        height=38,
        width=86,
        corner_radius=15,
        fg_color=const.BUTTON_SECONDARY_BG,
        text_color=const.BUTTON_SECONDARY_TEXT,
        command=lambda: cancel(),
    )
    cancel_Button.grid(row=0, column=0, padx=10)

    delete_Button = ctk.CTkButton(
        buttons_Frame,
        text="Удалить",
        font=("Inter", 14, "bold"),
        height=38,
        width=80,
        corner_radius=15,
        fg_color=const.BUTTON_CONFIRM_BG,
        text_color=const.BUTTON_CONFIRM_TEXT,
        command=lambda: delete(),
    )
    delete_Button.grid(row=0, column=1)

    confirmation_TopUp.after(100, confirmation_TopUp.lift)


# Модальное окно с настройками колоды
def settings_deck(deck, app):
    def cancel():
        deckSettings_TopUp.destroy()
        deckSettings_TopUp.update()

    def update():
        id = deck["id"]

        new_name = input_Entry.get()
        if new_name == "":
            alert(deckSettings_TopUp, "Пустой ввод.")
            return

        result = _rename_deck(id, new_name)

        if result is False:
            alert(deckSettings_TopUp, "Имя занято.")
            return

        deckSettings_TopUp.destroy()
        deckSettings_TopUp.update()
        editor_decks(app, reload=True)

    # Модальное окно с настройками колоды
    deckSettings_TopUp = ctk.CTkToplevel(app)
    deckSettings_TopUp.title("Настройки колоды")
    deckSettings_TopUp.geometry("490x250")
    deckSettings_TopUp.configure(fg_color=const.COLOR_BG, corner_radius=15)
    deckSettings_TopUp.resizable(False, False)
    deckSettings_TopUp.rowconfigure((0, 1, 2), weight=0)
    deckSettings_TopUp.columnconfigure(0, weight=1)

    # Шапка
    header_Frame = ctk.CTkFrame(deckSettings_TopUp, fg_color=const.COLOR_BG, height=64)
    header_Frame.grid(row=0, column=0, padx=15, pady=10, sticky="EW")
    header_Frame.rowconfigure(0, weight=0)
    header_Frame.columnconfigure(0, weight=1)
    header_Frame.columnconfigure(1, weight=0)

    header_Label = ctk.CTkLabel(
        header_Frame, text="Настройки колоды", font=("Inter", 16, "bold")
    )
    header_Label.grid(row=0, column=0, sticky="W")

    header_Button = ctk.CTkButton(
        header_Frame,
        text="X",
        height=20,
        width=20,
        font=("Inter", 16, "bold"),
        fg_color="transparent",
        command=lambda: cancel(),
    )
    header_Button.grid(row=0, column=1, sticky="E")

    # Поле ввода
    input_Frame = ctk.CTkFrame(deckSettings_TopUp, fg_color=const.COLOR_BG)
    input_Frame.grid(row=1, column=0, padx=15, pady=(25, 0))

    input_Label = ctk.CTkLabel(input_Frame, text="Новое название", font=("Inter", 14))
    input_Label.grid(row=0, column=0, sticky="W", pady=5)

    name = deck["name"]
    input_Entry = ctk.CTkEntry(
        input_Frame,
        placeholder_text=name,
        placeholder_text_color=const.TEXT_SECONDARY,
        width=454,
        height=50,
        corner_radius=15,
        fg_color=const.ENTRY_BG,
        border_color=const.FRAME_BORDER,
    )
    input_Entry.grid(row=1, column=0, sticky="W")

    # Кнопки
    buttons_Frame = ctk.CTkFrame(deckSettings_TopUp, fg_color=const.COLOR_BG)
    buttons_Frame.grid(row=2, column=0, sticky="E", padx=15, pady=31)

    cancel_Button = ctk.CTkButton(
        buttons_Frame,
        text="Отмена",
        font=("Inter", 14),
        height=39,
        width=86,
        corner_radius=15,
        fg_color=const.BUTTON_SECONDARY_BG,
        text_color=const.BUTTON_SECONDARY_TEXT,
        command=lambda: cancel(),
    )
    cancel_Button.grid(row=0, column=0, padx=10)

    save_Button = ctk.CTkButton(
        buttons_Frame,
        text="Сохранить",
        font=("Inter", 14, "bold"),
        height=39,
        width=84,
        corner_radius=15,
        fg_color=const.BUTTON_PRIMARY_BG,
        text_color=const.BUTTON_PRIMARY_TEXT,
        command=lambda: update(),
    )
    save_Button.grid(row=0, column=1)

    deckSettings_TopUp.after(100, deckSettings_TopUp.lift)


def editor_cards(app, deck, reload=None) -> None:
    current_deck = deck
    current_deck_id = current_deck["id"]
    current_deck_name = current_deck["name"]

    app.configure(fg_color=const.COLOR_BG)
    app.title(f"PyCards - Редактор карточек - {current_deck_name}")

    if reload:
        for widget in app.winfo_children():
            widget.destroy()

    for i in range(8):
        app.grid_rowconfigure(i, weight=0)
    app.grid_columnconfigure(0, weight=1)

    # Шапка
    header_frame = ctk.CTkFrame(
        master=app, height=38, width=740, fg_color=const.COLOR_BG
    )
    header_frame.grid(row=0, column=0, pady=15, sticky="EW", padx=20)
    header_frame.rowconfigure(0, weight=1)
    header_frame.columnconfigure((0, 1, 2), weight=1)
    header_frame.columnconfigure(0, weight=0)

    back_button = ctk.CTkButton(
        master=header_frame,
        image=IMG_ARROW,
        text="",
        width=30,
        height=30,
        fg_color="transparent",
        hover_color="#27272A",
        font=("Inter", 18, "bold"),
        command=lambda: editor_decks(app),
    )
    back_button.grid(row=0, column=0, sticky="W", padx=10)

    # Заголовок "Карточки колоды {name}"
    cards_label = ctk.CTkLabel(
        master=header_frame,
        text="Карточки",
        font=("Inter", 24, "bold"),
    )
    cards_label.grid(row=0, column=1, sticky="W")

    # Фрейм под кнопки
    buttons_Frame = ctk.CTkFrame(header_frame, fg_color=const.COLOR_BG)
    buttons_Frame.grid(row=0, column=2, sticky="E")

    # Кнопка "Импорт"
    import_Button = ctk.CTkButton(
        master=buttons_Frame,
        text="Импорт",
        fg_color=const.BUTTON_SECONDARY_BG,
        hover_color="#1447E6",
        font=("Inter", 16, "bold"),
        corner_radius=15,
        height=38,
        width=92,
        command=lambda d=deck, app=app: import_cards(d, app),
    )
    import_Button.grid(row=0, column=0)

    # Кнопка "Экспорт"
    export_Button = ctk.CTkButton(
        master=buttons_Frame,
        text="Экспорт",
        fg_color=const.BUTTON_SECONDARY_BG,
        hover_color="#1447E6",
        font=("Inter", 16, "bold"),
        corner_radius=15,
        height=38,
        width=92,
        command=lambda d=deck, app=app: export_cards(d, app),
    )
    export_Button.grid(row=0, column=1, padx=10)

    # Кнопка "Создать"
    create_Button = ctk.CTkButton(
        master=buttons_Frame,
        text="+ Создать",
        fg_color="#155DFC",
        hover_color="#1447E6",
        font=("Inter", 16, "bold"),
        corner_radius=15,
        height=38,
        width=92,
        command=lambda d=deck, app=app: create_card(d, app),
    )
    create_Button.grid(row=0, column=2)

    # Фрейм под карточки
    cards_frame = ctk.CTkScrollableFrame(
        master=app,
        width=760,
        height=500,
        fg_color=const.COLOR_BG,
        scrollbar_button_color="#303037",
    )
    cards_frame.grid(row=1, column=0, padx=20, sticky="EW")

    cards_list = _get_cards_by_deck(current_deck_id)
    for index, card in enumerate(cards_list):
        # Фрейм под карточку
        card_frame = ctk.CTkFrame(
            master=cards_frame,
            fg_color="#242427",
            height=90,
            width=730,
            border_width=2,
            border_color="#303037",
            corner_radius=15,
        )
        card_frame.grid(
            row=1 + index, column=0, columnspan=8, sticky="EW", padx=5, pady=5
        )
        card_frame.grid_columnconfigure(2, weight=1)
        card_frame.grid_rowconfigure(0, weight=1)
        card_frame.grid_propagate(False)

        # Сокращение слишком длинных вопросов и ответов
        question = card["question"]
        if len(question) > 70:
            question = question[:70] + "..."
        answer = card["answer"]
        if len(answer) > 80:
            answer = answer[:80] + "..."

        # Фрейм под данные карточки
        cardData_Frame = ctk.CTkFrame(master=card_frame, fg_color="#242427")
        cardData_Frame.grid(row=0, column=0, sticky="W", padx=(15, 0))
        cardData_Frame.grid_columnconfigure(0, weight=1)
        cardData_Frame.grid_rowconfigure((0, 1), weight=1)

        # Вопрос
        question_Label = ctk.CTkLabel(
            master=cardData_Frame,
            text=question,
            font=("Inter", 16, "bold"),
            text_color=const.WHITE,
        )
        question_Label.grid(row=0, column=0, sticky="W")

        # Ответ
        answer_Label = ctk.CTkLabel(
            master=cardData_Frame,
            text=answer,
            font=("Inter", 13),
            text_color=const.TEXT_SECONDARY,
        )
        answer_Label.grid(row=1, column=0, sticky="W")

        buttons_Frame = ctk.CTkFrame(master=card_frame, fg_color="transparent")
        buttons_Frame.grid(row=0, column=2, sticky="E", padx=(0, 5))

        buttons_Frame.rowconfigure(0, weight=1)
        buttons_Frame.columnconfigure(2, weight=1)

        settings_Button = ctk.CTkButton(
            master=buttons_Frame,
            font=("Inter", 13),
            text="",
            image=IMG_SETTINGS,
            height=35,
            width=20,
            corner_radius=10,
            fg_color="#3F3F46",
            hover_color="#51515C",
            command=lambda c=card, d=deck: settings_card(c, d, app),
        )
        settings_Button.grid(row=0, column=2, padx=(0, 5))
        delete_Button = ctk.CTkButton(
            master=buttons_Frame,
            font=("Inter", 13, "bold"),
            text="",
            image=IMG_DELETE,
            height=35,
            width=20,
            corner_radius=10,
            fg_color="#392529",
            text_color="#FF6467",
            hover_color="#51282C",
            command=lambda id=card: delete_card(id, deck, app),
        )
        delete_Button.grid(row=0, column=3, padx=(0, 5))


def import_cards(deck, app):
    def cancel():
        import_TopUp.destroy()
        import_TopUp.update()

    def import_from_csv():
        path = path_Entry.get()
        encoding = encoding_Entry.get()

        if not path and not encoding:
            alert(import_TopUp, "\nВы ничего не ввели!")
            return
        elif not path:
            alert(import_TopUp, "Вы не путь к файлу!")
            return

        import_TopUp.destroy()
        import_TopUp.update()

        load_deck(path, encoding, deck["name"])

        editor_cards(app, deck, True)

    import_TopUp = ctk.CTkToplevel(app)
    import_TopUp.title("Импорт карточек")
    import_TopUp.geometry("490x340")
    import_TopUp.resizable(False, False)
    import_TopUp.configure(fg_color=const.COLOR_BG, corner_radius=15)
    import_TopUp.rowconfigure((0, 1, 2, 3), weight=0)
    import_TopUp.columnconfigure(0, weight=1)

    # Шапка
    header_Frame = ctk.CTkFrame(import_TopUp, fg_color=const.COLOR_BG, height=64)
    header_Frame.grid(row=0, column=0, padx=15, pady=10, sticky="EW")
    header_Frame.rowconfigure(0, weight=0)
    header_Frame.columnconfigure(0, weight=1)
    header_Frame.columnconfigure(1, weight=0)

    header_Label = ctk.CTkLabel(
        header_Frame, text="Импорт карточек", font=("Inter", 16, "bold")
    )
    header_Label.grid(row=0, column=0, sticky="W")

    header_Button = ctk.CTkButton(
        header_Frame,
        text="X",
        height=20,
        width=20,
        font=("Inter", 16, "bold"),
        fg_color="transparent",
        command=lambda: cancel(),
    )
    header_Button.grid(row=0, column=1, sticky="E")

    path_Frame = ctk.CTkFrame(import_TopUp, fg_color=const.COLOR_BG)
    path_Frame.rowconfigure((0, 1), weight=1)
    path_Frame.columnconfigure(0, weight=1)
    path_Frame.grid(row=1, column=0, padx=15, pady=10, sticky="EW")

    path_Label = ctk.CTkLabel(
        path_Frame, text="Путь к файлу", font=("Inter", 16, "bold")
    )
    path_Label.grid(row=0, column=0, sticky="W")

    path_Selector = ctk.CTkFrame(path_Frame, fg_color=const.COLOR_BG)
    path_Selector.grid(row=1, column=0, pady=(7, 0))

    path_Entry = ctk.CTkEntry(
        path_Selector,
        placeholder_text=r"C:\Users\User\cards.csv",
        fg_color=const.ENTRY_BG,
        border_width=2,
        height=50,
        border_color=const.FRAME_BORDER,
        width=346,
        font=("Inter", 14),
        corner_radius=15,
    )
    path_Entry.grid(row=0, column=0, sticky="W", padx=(0, 20))

    def check_file_encoding(file_path):
        with open(file_path, "rb") as f:
            raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            encoding = result["encoding"]
            return encoding

    def insert_filepath():
        file_path = ctk.filedialog.askopenfilename()
        import_TopUp.after(100, import_TopUp.lift)
        file_encoding = check_file_encoding(file_path)
        path_Entry.delete(0, ctk.END)
        path_Entry.insert(0, file_path)
        encoding_Entry.delete(0, ctk.END)
        encoding_Entry.insert(0, file_encoding)

    path_Button = ctk.CTkButton(
        path_Selector,
        text="Обзор",
        fg_color=const.BUTTON_SECONDARY_BG,
        corner_radius=15,
        height=50,
        width=93,
        command=lambda: insert_filepath(),
    )
    path_Button.grid(row=0, column=1, sticky="E")

    encoding_Frame = ctk.CTkFrame(import_TopUp, fg_color=const.COLOR_BG)
    encoding_Frame.grid(row=2, column=0, padx=15, pady=10, sticky="EW")
    encoding_Frame.rowconfigure((0, 1), weight=1)
    encoding_Frame.columnconfigure(0, weight=1)

    encoding_Label = ctk.CTkLabel(
        encoding_Frame, text="Кодировка", font=("Inter", 16, "bold")
    )
    encoding_Label.grid(row=0, column=0, sticky="W")

    encoding_Entry = ctk.CTkEntry(
        encoding_Frame,
        placeholder_text="UTF-8",
        fg_color=const.ENTRY_BG,
        border_width=2,
        height=50,
        border_color=const.FRAME_BORDER,
        font=("Inter", 14),
        corner_radius=15,
    )
    encoding_Entry.grid(row=1, column=0, sticky="EW", pady=(7, 0))

    # Кнопки
    buttons_Frame = ctk.CTkFrame(import_TopUp, fg_color=const.COLOR_BG)
    buttons_Frame.grid(row=3, column=0, sticky="E", padx=15, pady=20)

    cancel_Button = ctk.CTkButton(
        buttons_Frame,
        text="Отмена",
        font=("Inter", 14),
        height=39,
        width=86,
        corner_radius=15,
        fg_color=const.BUTTON_SECONDARY_BG,
        text_color=const.BUTTON_SECONDARY_TEXT,
        command=lambda: cancel(),
    )
    cancel_Button.grid(row=0, column=0, padx=10)

    create_Button = ctk.CTkButton(
        buttons_Frame,
        text="Импортировать",
        font=("Inter", 14, "bold"),
        height=39,
        width=84,
        corner_radius=15,
        fg_color=const.BUTTON_PRIMARY_BG,
        text_color=const.BUTTON_PRIMARY_TEXT,
        command=lambda: import_from_csv(),
    )
    create_Button.grid(row=0, column=1)

    import_TopUp.after(100, import_TopUp.lift)


def export_cards(deck, app):
    def cancel():
        export_TopUp.destroy()
        export_TopUp.update()

    def import_from_csv():
        name = fileName_Entry.get()
        path = path_Entry.get()

        save_deck(deck["id"], name, path)

        export_TopUp.destroy()
        export_TopUp.update()

        editor_cards(app, deck, True)

    export_TopUp = ctk.CTkToplevel(app)
    export_TopUp.title("Экспорт карточек")
    export_TopUp.geometry("490x340")
    export_TopUp.resizable(False, False)
    export_TopUp.configure(fg_color=const.COLOR_BG, corner_radius=15)
    export_TopUp.rowconfigure((0, 1, 2, 3), weight=0)
    export_TopUp.columnconfigure(0, weight=1)

    # Шапка
    header_Frame = ctk.CTkFrame(export_TopUp, fg_color=const.COLOR_BG, height=64)
    header_Frame.grid(row=0, column=0, padx=15, pady=10, sticky="EW")
    header_Frame.rowconfigure(0, weight=0)
    header_Frame.columnconfigure(0, weight=1)
    header_Frame.columnconfigure(1, weight=0)

    header_Label = ctk.CTkLabel(
        header_Frame, text="Экспорт в CSV", font=("Inter", 16, "bold")
    )
    header_Label.grid(row=0, column=0, sticky="W")

    header_Button = ctk.CTkButton(
        header_Frame,
        text="X",
        height=20,
        width=20,
        font=("Inter", 16, "bold"),
        fg_color="transparent",
        command=lambda: cancel(),
    )
    header_Button.grid(row=0, column=1, sticky="E")

    fileName_Frame = ctk.CTkFrame(export_TopUp, fg_color=const.COLOR_BG)
    fileName_Frame.grid(row=1, column=0, padx=15, pady=10, sticky="EW")
    fileName_Frame.rowconfigure((0, 1), weight=1)
    fileName_Frame.columnconfigure(0, weight=1)

    fileName_Label = ctk.CTkLabel(
        fileName_Frame, text="Название файла", font=("Inter", 16, "bold")
    )
    fileName_Label.grid(row=0, column=0, sticky="W")

    fileName_Entry = ctk.CTkEntry(
        fileName_Frame,
        placeholder_text="Математика - интегралы",
        fg_color=const.ENTRY_BG,
        border_width=2,
        height=50,
        border_color=const.FRAME_BORDER,
        font=("Inter", 14),
        corner_radius=15,
    )
    fileName_Entry.grid(row=1, column=0, sticky="EW", pady=(7, 0))

    path_Frame = ctk.CTkFrame(export_TopUp, fg_color=const.COLOR_BG)
    path_Frame.rowconfigure((0, 1), weight=1)
    path_Frame.columnconfigure(0, weight=1)
    path_Frame.grid(row=2, column=0, padx=15, pady=10, sticky="EW")

    path_Label = ctk.CTkLabel(
        path_Frame, text="Путь для сохранения", font=("Inter", 16, "bold")
    )
    path_Label.grid(row=0, column=0, sticky="W")

    path_Selector = ctk.CTkFrame(path_Frame, fg_color=const.COLOR_BG)
    path_Selector.grid(row=1, column=0, pady=(0, 7))

    path_Entry = ctk.CTkEntry(
        path_Selector,
        placeholder_text=r"C:\Users\User\Documents",
        fg_color=const.ENTRY_BG,
        border_width=2,
        border_color=const.FRAME_BORDER,
        height=50,
        width=346,
        font=("Inter", 14),
        corner_radius=15,
    )
    path_Entry.grid(row=0, column=0, sticky="W", padx=(0, 20))

    def choose_filepath():
        path = ctk.filedialog.askdirectory()
        export_TopUp.after(100, export_TopUp.lift)
        path_Entry.delete(0, ctk.END)
        path_Entry.insert(0, path)

    path_Button = ctk.CTkButton(
        path_Selector,
        text="Обзор",
        fg_color=const.BUTTON_SECONDARY_BG,
        corner_radius=15,
        height=50,
        width=93,
        command=lambda: choose_filepath(),
    )
    path_Button.grid(row=0, column=1, sticky="E")

    # Кнопки
    buttons_Frame = ctk.CTkFrame(export_TopUp, fg_color=const.COLOR_BG)
    buttons_Frame.grid(row=3, column=0, sticky="E", padx=15, pady=20)

    cancel_Button = ctk.CTkButton(
        buttons_Frame,
        text="Отмена",
        font=("Inter", 14),
        height=39,
        width=86,
        corner_radius=15,
        fg_color=const.BUTTON_SECONDARY_BG,
        text_color=const.BUTTON_SECONDARY_TEXT,
        command=lambda: cancel(),
    )
    cancel_Button.grid(row=0, column=0, padx=10)

    create_Button = ctk.CTkButton(
        buttons_Frame,
        text="Экспортировать",
        font=("Inter", 14, "bold"),
        height=39,
        width=84,
        corner_radius=15,
        fg_color=const.BUTTON_PRIMARY_BG,
        text_color=const.BUTTON_PRIMARY_TEXT,
        command=lambda: import_from_csv(),
    )
    create_Button.grid(row=0, column=1)

    export_TopUp.after(100, export_TopUp.lift)


def create_card(deck, app) -> None:
    def cancel():
        createCard_TopUp.destroy()
        createCard_TopUp.update()

    def create():
        question = (question_Textbox.get("0.0", ctk.END)).strip("\n")
        answer = (answer_Textbox.get("0.0", ctk.END)).strip("\n")

        if not question and not answer:
            alert(createCard_TopUp, "\nВы не ввели вопрос и ответ!")
            return
        elif not question:
            alert(createCard_TopUp, "Вы не ввели вопрос!")
            return
        elif not answer:
            alert(createCard_TopUp, "Вы не ввели ответ!")
            return

        _create_card(deck["id"], question, answer)

        createCard_TopUp.destroy()
        createCard_TopUp.update()

        editor_cards(app, deck, True)

    # Модальное окно создания карточки
    createCard_TopUp = ctk.CTkToplevel(app)
    createCard_TopUp.title("Создать карточку")
    createCard_TopUp.geometry("490x440")
    createCard_TopUp.configure(fg_color=const.COLOR_BG, corner_radius=15)
    createCard_TopUp.resizable(False, False)
    createCard_TopUp.rowconfigure((0, 1, 2, 3), weight=0)
    createCard_TopUp.columnconfigure(0, weight=1)

    # Шапка
    header_Frame = ctk.CTkFrame(createCard_TopUp, fg_color=const.COLOR_BG, height=64)
    header_Frame.grid(row=0, column=0, padx=15, pady=10, sticky="EW")
    header_Frame.rowconfigure(0, weight=0)
    header_Frame.columnconfigure(0, weight=1)
    header_Frame.columnconfigure(1, weight=0)

    header_Label = ctk.CTkLabel(
        header_Frame, text="Создать карточку", font=("Inter", 16, "bold")
    )
    header_Label.grid(row=0, column=0, sticky="W")

    header_Button = ctk.CTkButton(
        header_Frame,
        text="X",
        height=20,
        width=20,
        font=("Inter", 16, "bold"),
        fg_color="transparent",
        command=lambda: cancel(),
    )
    header_Button.grid(row=0, column=1, sticky="E")

    # Поле ввода вопроса
    question_Frame = ctk.CTkFrame(createCard_TopUp, fg_color=const.COLOR_BG)
    question_Frame.grid(row=1, column=0, padx=15, pady=10, sticky="EW")
    question_Frame.rowconfigure((0, 1), weight=1)
    question_Frame.columnconfigure(0, weight=1)

    question_Label = ctk.CTkLabel(
        question_Frame, text="Вопрос", font=("Inter", 14, "bold")
    )
    question_Label.grid(row=0, column=0, sticky="W", pady=(0, 7))

    question_Textbox = ctk.CTkTextbox(
        question_Frame,
        height=100,
        width=450,
        font=("Inter", 14),
        corner_radius=15,
        fg_color=const.ENTRY_BG,
        border_width=2,
        border_color=const.FRAME_BORDER,
    )
    question_Textbox.grid(row=1, column=0, sticky="EW")

    # Поле ввода ответа
    answer_Frame = ctk.CTkFrame(createCard_TopUp, fg_color=const.COLOR_BG)
    answer_Frame.grid(row=2, column=0, padx=15, pady=10, sticky="EW")
    answer_Frame.rowconfigure((0, 1), weight=1)
    answer_Frame.columnconfigure(0, weight=1)

    answer_Label = ctk.CTkLabel(answer_Frame, text="Ответ", font=("Inter", 14, "bold"))
    answer_Label.grid(row=0, column=0, sticky="W", pady=(0, 7))

    answer_Textbox = ctk.CTkTextbox(
        answer_Frame,
        height=100,
        width=450,
        font=("Inter", 14),
        corner_radius=15,
        fg_color=const.ENTRY_BG,
        border_width=2,
        border_color=const.FRAME_BORDER,
    )
    answer_Textbox.grid(row=1, column=0, sticky="EW")

    # Кнопки
    buttons_Frame = ctk.CTkFrame(createCard_TopUp, fg_color=const.COLOR_BG)
    buttons_Frame.grid(row=3, column=0, sticky="E", padx=15, pady=25)

    cancel_Button = ctk.CTkButton(
        buttons_Frame,
        text="Отмена",
        font=("Inter", 14),
        height=39,
        width=86,
        corner_radius=15,
        fg_color=const.BUTTON_SECONDARY_BG,
        text_color=const.BUTTON_SECONDARY_TEXT,
        command=lambda: cancel(),
    )
    cancel_Button.grid(row=0, column=0, padx=10)

    create_Button = ctk.CTkButton(
        buttons_Frame,
        text="Создать",
        font=("Inter", 14, "bold"),
        height=39,
        width=84,
        corner_radius=15,
        fg_color=const.BUTTON_PRIMARY_BG,
        text_color=const.BUTTON_PRIMARY_TEXT,
        command=lambda: create(),
    )
    create_Button.grid(row=0, column=1)

    createCard_TopUp.after(100, createCard_TopUp.lift)


def settings_card(card, deck, app):
    def cancel():
        cardSettings_TopUp.destroy()
        cardSettings_TopUp.update()

    def update():
        card_id = card["id"]
        new_question = (question_Textbox.get("0.0", ctk.END)).strip("\n")
        new_answer = (answer_Textbox.get("0.0", ctk.END)).strip("\n")
        new_deck_id = 0

        q_deck_name = deck_OptionMenu.get()
        for deck_id, deck_name in decks.items():
            if deck_name == q_deck_name:
                new_deck_id = deck_id

        _update_card(card_id, new_question, new_answer, new_deck_id)

        cardSettings_TopUp.destroy()
        cardSettings_TopUp.update()

        editor_cards(app, deck, True)

    question = card["question"]
    answer = card["answer"]
    deck_id = card["deck_id"]
    deck_name = _get_deck_by_id(deck_id)["name"]

    decks = {deck["id"]: deck["name"] for deck in _get_all_decks()}

    cardSettings_TopUp = ctk.CTkToplevel(app)
    cardSettings_TopUp.title("Настройки карточки")
    cardSettings_TopUp.geometry("490x541")
    cardSettings_TopUp.configure(fg_color=const.COLOR_BG, corner_radius=15)
    cardSettings_TopUp.resizable(False, False)
    cardSettings_TopUp.rowconfigure((0, 1, 2, 3, 4), weight=0)
    cardSettings_TopUp.columnconfigure(0, weight=1)

    # Шапка
    header_Frame = ctk.CTkFrame(cardSettings_TopUp, fg_color=const.COLOR_BG, height=64)
    header_Frame.grid(row=0, column=0, padx=15, pady=10, sticky="EW")
    header_Frame.rowconfigure(0, weight=0)
    header_Frame.columnconfigure(0, weight=1)
    header_Frame.columnconfigure(1, weight=0)

    header_Label = ctk.CTkLabel(
        header_Frame, text="Настройки карточки", font=("Inter", 16, "bold")
    )
    header_Label.grid(row=0, column=0, sticky="W")

    header_Button = ctk.CTkButton(
        header_Frame,
        text="X",
        height=20,
        width=20,
        font=("Inter", 16, "bold"),
        fg_color="transparent",
        command=lambda: cancel(),
    )
    header_Button.grid(row=0, column=1, sticky="E")

    # Фрейм с вопросом
    question_Frame = ctk.CTkFrame(cardSettings_TopUp, fg_color=const.COLOR_BG)
    question_Frame.grid(row=1, column=0, padx=15, pady=10, sticky="EW")

    question_Label = ctk.CTkLabel(question_Frame, text="Вопрос", font=("Inter", 14))
    question_Label.grid(row=0, column=0, sticky="W", pady=(0, 10))

    question_Textbox = ctk.CTkTextbox(
        question_Frame,
        width=454,
        height=100,
        corner_radius=15,
        fg_color=const.ENTRY_BG,
        border_width=2,
        border_color=const.FRAME_BORDER,
        font=("Inter", 14),
    )
    question_Textbox.insert("0.0", question)
    question_Textbox.grid(row=1, column=0, sticky="EW")

    answer_Frame = ctk.CTkFrame(cardSettings_TopUp, fg_color=const.COLOR_BG)
    answer_Frame.grid(row=2, column=0, padx=15, sticky="EW")

    answer_Label = ctk.CTkLabel(answer_Frame, text="Ответ", font=("Inter", 14))
    answer_Label.grid(row=0, column=0, sticky="W", pady=(0, 10))

    answer_Textbox = ctk.CTkTextbox(
        answer_Frame,
        width=454,
        height=100,
        corner_radius=15,
        fg_color=const.ENTRY_BG,
        border_width=2,
        border_color=const.FRAME_BORDER,
        font=("Inter", 14),
    )
    answer_Textbox.insert("0.0", answer)
    answer_Textbox.grid(row=1, column=0, sticky="EW")

    deck_Frame = ctk.CTkFrame(
        cardSettings_TopUp, fg_color=const.COLOR_BG, height=74, width=454
    )
    deck_Frame.grid(row=3, column=0, padx=5, pady=10, sticky="EW")

    deck_Label = ctk.CTkLabel(deck_Frame, text="Колода", font=("Inter", 14))
    deck_Label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="W")

    optionMenu_var = ctk.StringVar(value=deck_name)

    deck_OptionMenu = ctk.CTkOptionMenu(
        deck_Frame,
        values=list(decks.values()),
        variable=optionMenu_var,
        height=50,
        width=454,
        fg_color=const.ENTRY_BG,
        font=("Inter", 14),
        dropdown_font=("Inter", 14),
        dropdown_fg_color=const.ENTRY_BG,
        button_color=const.ENTRY_BG,
        button_hover_color=const.ENTRY_BG,
    )
    deck_OptionMenu.grid(row=1, column=0, padx=10, sticky="EW")

    # Кнопки
    buttons_Frame = ctk.CTkFrame(cardSettings_TopUp, fg_color=const.COLOR_BG)
    buttons_Frame.grid(row=4, column=0, sticky="E", padx=15, pady=25)

    cancel_Button = ctk.CTkButton(
        buttons_Frame,
        text="Отмена",
        font=("Inter", 14),
        height=39,
        width=86,
        corner_radius=15,
        fg_color=const.BUTTON_SECONDARY_BG,
        text_color=const.BUTTON_SECONDARY_TEXT,
        command=lambda: cancel(),
    )
    cancel_Button.grid(row=0, column=0, padx=10)

    save_Button = ctk.CTkButton(
        buttons_Frame,
        text="Сохранить",
        font=("Inter", 14, "bold"),
        height=39,
        width=84,
        corner_radius=15,
        fg_color=const.BUTTON_PRIMARY_BG,
        text_color=const.BUTTON_PRIMARY_TEXT,
        command=lambda: update(),
    )
    save_Button.grid(row=0, column=1)

    cardSettings_TopUp.after(100, cardSettings_TopUp.lift)


# Модальное окно подтверждения удаления карточки
def delete_card(card, deck, app):
    def cancel():
        confirmation_TopUp.destroy()
        confirmation_TopUp.update()

    def delete():
        _delete_card(card["id"])

        confirmation_TopUp.destroy()
        confirmation_TopUp.update()

        editor_cards(app, deck, True)

    confirmation_TopUp = ctk.CTkToplevel(app)
    confirmation_TopUp.title("Удалить карточку")
    confirmation_TopUp.geometry("490x150")
    confirmation_TopUp.configure(fg_color=const.COLOR_BG)
    confirmation_TopUp.resizable(False, False)
    confirmation_TopUp.rowconfigure((0, 1, 2), weight=0)
    confirmation_TopUp.columnconfigure(0, weight=1)

    # Шапка
    header_Frame = ctk.CTkFrame(confirmation_TopUp, fg_color=const.COLOR_BG, height=64)
    header_Frame.grid(row=0, column=0, padx=15, pady=10, sticky="EW")
    header_Frame.rowconfigure(0, weight=0)
    header_Frame.columnconfigure(0, weight=1)
    header_Frame.columnconfigure(1, weight=0)

    header_Label = ctk.CTkLabel(
        header_Frame, text="Удалить карточку", font=("Inter", 16, "bold")
    )
    header_Label.grid(row=0, column=0, sticky="W")

    header_Button = ctk.CTkButton(
        header_Frame,
        text="X",
        height=20,
        width=20,
        font=("Inter", 16, "bold"),
        fg_color="transparent",
        command=lambda: cancel(),
    )
    header_Button.grid(row=0, column=1, sticky="E")

    confirmation_Label = ctk.CTkLabel(
        confirmation_TopUp,
        text="Удалить карточку? Это действие нельзя отменить.",
        font=("Inter", 14),
        wraplength=450,
        anchor="w",
        justify="left",
    )
    confirmation_Label.grid(row=1, column=0, padx=15, pady=(10, 0), sticky="EW")

    # Кнопки
    buttons_Frame = ctk.CTkFrame(confirmation_TopUp, fg_color=const.COLOR_BG)
    buttons_Frame.grid(row=2, column=0, sticky="E", padx=15, pady=10)

    cancel_Button = ctk.CTkButton(
        buttons_Frame,
        text="Отмена",
        font=("Inter", 14),
        height=38,
        width=86,
        corner_radius=15,
        fg_color=const.BUTTON_SECONDARY_BG,
        text_color=const.BUTTON_SECONDARY_TEXT,
        command=lambda: cancel(),
    )
    cancel_Button.grid(row=0, column=0, padx=10)

    delete_Button = ctk.CTkButton(
        buttons_Frame,
        text="Удалить",
        font=("Inter", 14, "bold"),
        height=38,
        width=80,
        corner_radius=15,
        fg_color=const.BUTTON_CONFIRM_BG,
        text_color=const.BUTTON_CONFIRM_TEXT,
        command=lambda: delete(),
    )
    delete_Button.grid(row=0, column=1)

    confirmation_TopUp.after(100, confirmation_TopUp.lift)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.title("PyCards")
    app.geometry("800x600")
    app.resizable(False, False)

    app.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
    app.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

    editor_decks(app)
    app.mainloop()
