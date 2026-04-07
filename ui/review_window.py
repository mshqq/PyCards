# Окно просмотра
# Основное окно
from scheduler import calculate_next
from card_model import _get_cards_for_review, _get_cards_by_deck, _update_card_sm2
from deck_model import _get_decks_with_counts
from ui import main_window
from ui.utils import alert
import ui.constants as const

from PIL import Image
import customtkinter as ctk

IMG_ARROW = ctk.CTkImage(Image.open("icons/arrow.png"), size=(16, 12))


def select_Window(app):
    def back():
        main_window.main_menu(app)

    app.configure(fg_color=const.COLOR_BG)
    app.title("PyCards - Выбор колоды")

    for widget in app.winfo_children():
        widget.destroy()

    for i in range(8):
        app.grid_rowconfigure(i, weight=0)
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    # header_frame
    header_Frame = ctk.CTkFrame(
        master=app, height=38, width=740, fg_color=const.COLOR_BG
    )
    header_Frame.grid(row=0, column=0, pady=(15, 0), sticky="EW", padx=20)
    header_Frame.rowconfigure((0, 1), weight=0)
    header_Frame.columnconfigure(0, weight=0)
    header_Frame.columnconfigure(1, weight=1)

    # Кнопка "Назад"
    back_Button = ctk.CTkButton(
        master=header_Frame,
        image=IMG_ARROW,
        text="",
        width=30,
        height=30,
        fg_color="transparent",
        hover_color=const.COLOR_BORDER,
        command=lambda: back(),
        font=("Inter", 18, "bold"),
    
        text_color=const.TEXT_PRIMARY,)
    back_Button.grid(row=0, column=0, sticky="W", padx=10)

    # Заголовок "Выбор колоды"
    header_Label = ctk.CTkLabel(
        master=header_Frame, text="Выбор колоды", font=("Inter", 24, "bold")
    ,
        text_color=const.TEXT_PRIMARY)
    header_Label.grid(row=0, column=1, sticky="W")

    decks_Frame = ctk.CTkScrollableFrame(
        app,
        width=760,
        height=500,
        fg_color=const.COLOR_BG,
        scrollbar_button_color=const.SCROLLBAR_BG,
    )
    decks_Frame.grid(row=1, column=0, sticky="EW", padx=20)
    decks_Frame.columnconfigure((0, 1, 2), weight=1)

    all_decks = _get_decks_with_counts()
    decks = [all_decks[i : i + 3] for i in range(0, len(all_decks), 3)]

    for row_index, row in enumerate(decks):
        for deck_index, deck in enumerate(row):
            deck_Frame = ctk.CTkFrame(
                decks_Frame,
                fg_color=const.FRAME_BG,
                border_width=2,
                border_color=const.FRAME_BORDER,
                height=155,
                width=226,
                corner_radius=15,
            )
            deck_Frame.grid(
                row=1 + row_index,
                column=0 + deck_index,
                padx=10,
                pady=(0, 15),
            )
            deck_Frame.grid_columnconfigure(0, weight=1)
            deck_Frame.grid_rowconfigure((0, 1, 2), weight=0)
            deck_Frame.grid_propagate(False)

            # Название колоды
            name_Label = ctk.CTkLabel(
                master=deck_Frame,
                text=deck["name"],
                font=("Inter", 14, "bold"),
                anchor="w",
            
        text_color=const.TEXT_PRIMARY,)
            name_Label.grid(row=0, column=0, padx=(15, 10), pady=(10, 0), sticky="W")

            stats_Frame = ctk.CTkFrame(
                deck_Frame,
                height=23,
                width=93,
                fg_color=const.FRAME_BG,
            )
            stats_Frame.grid(row=1, column=0, padx=(15, 10), pady=(4, 0), sticky="W")
            stats_Frame.columnconfigure(0, weight=0)
            stats_Frame.rowconfigure((0, 1), weight=0)

            countCards = len(_get_cards_by_deck(deck["id"]))

            countCards_Label = ctk.CTkLabel(
                stats_Frame,
                text=f"Всего карточек: {countCards}",
                font=("Inter", 14),
                fg_color=const.FRAME_BG,
            
        text_color=const.TEXT_PRIMARY,)
            countCards_Label.grid(row=0, column=0, sticky="W", pady=0)

            toLearnCards = len(_get_cards_for_review(deck["id"]))

            toLearnCards_Label = ctk.CTkLabel(
                stats_Frame,
                text=f"К повторению: {toLearnCards}",
                font=("Inter", 14),
                fg_color=const.FRAME_BG,
            
        text_color=const.TEXT_PRIMARY,)
            toLearnCards_Label.grid(row=1, column=0, sticky="W")

            buttons_Frame = ctk.CTkFrame(deck_Frame, fg_color=const.FRAME_BG)
            buttons_Frame.grid(row=2, column=0, padx=(15, 10), pady=(5, 0), sticky="EW")
            buttons_Frame.rowconfigure(0, weight=0)
            buttons_Frame.columnconfigure((0, 1), weight=1)

            learning_Button = ctk.CTkButton(
                buttons_Frame,
                text="Обучение",
                height=38,
                width=90,
                font=("Inter", 12, "bold"),
                corner_radius=15,
                fg_color=const.BUTTON_PRIMARY_BG,
                command=lambda deck=deck: learning_Window(app, deck),
            
        text_color=const.TEXT_PRIMARY,
        hover_color=const.BUTTON_PRIMARY_HOVER)
            learning_Button.grid(row=0, column=0, padx=(0, 6))

            view_Button = ctk.CTkButton(
                buttons_Frame,
                text="Просмотр",
                height=38,
                width=90,
                font=("Inter", 12, "bold"),
                corner_radius=15,
                fg_color=const.BUTTON_SECONDARY_BG,
                command=lambda deck=deck: viewer_Window(app, deck),
            
        text_color=const.TEXT_PRIMARY,
        hover_color=const.BUTTON_SECONDARY_HOVER)
            view_Button.grid(row=0, column=1, padx=(6, 0))


def learning_Window(app, deck):
    def back():
        select_Window(app)

    def showAnswer(
        answer_Label,
        showAnswer_Button,
        buttons_Frame,
        badMark_Button,
        normalMark_Button,
        goodMark_Button,
        easyMark_Button,
    ):
        answer_Label.configure(text_color=const.TEXT_PRIMARY)
        showAnswer_Button.grid_forget()

        buttons_Frame.grid(row=2, column=0, pady=25)
        buttons_Frame.columnconfigure((0, 1, 2, 3), weight=1)
        badMark_Button.grid(row=0, column=0, padx=(0, 10))
        normalMark_Button.grid(row=0, column=1, padx=(0, 10))
        goodMark_Button.grid(row=0, column=2, padx=(0, 10))
        easyMark_Button.grid(row=0, column=3, padx=(0, 10))

    def send_feedback(cards_for_review, card, pointer, repeated, mark):
        interval = card["interval"]
        repetitions = card["repetitions"]

        new_interval, new_repetitions, next_review_iso = calculate_next(
            interval, repetitions, mark
        )
        _update_card_sm2(card["id"], new_interval, new_repetitions, next_review_iso)

        if mark == "bad":
            cards_for_review.append(card)
            render(cards_for_review, pointer + 1, repeated)
            return

        render(cards_for_review, pointer + 1, repeated + 1)

    def render(cards_for_review, pointer, repeated):
        try:
            current_card = cards_for_review[pointer]
        except IndexError:
            if pointer != 0:
                alert(
                    app,
                    "Карточки к обучению закончились.",
                    on_close=lambda: select_Window(app),
                )
                return
            alert(app, "Карточек к обучению нет", on_close=lambda: select_Window(app))
            return

        app.configure(fg_color=const.COLOR_BG)
        app.title("PyCards - обучение")

        for widget in app.winfo_children():
            widget.destroy()

        for i in range(8):
            app.grid_rowconfigure(i, weight=0)
        app.grid_columnconfigure(0, weight=1)
        app.grid_rowconfigure((0, 1, 2), weight=0)

        # header_frame
        header_Frame = ctk.CTkFrame(
            master=app, height=38, width=740, fg_color=const.COLOR_BG
        )
        header_Frame.grid(row=0, column=0, pady=15, sticky="EW", padx=20)
        header_Frame.rowconfigure(0, weight=1)
        header_Frame.columnconfigure((0, 1, 2), weight=1)
        header_Frame.columnconfigure(0, weight=0)

        # Кнопка "Назад"
        back_button = ctk.CTkButton(
            master=header_Frame,
            image=IMG_ARROW,
            text="",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=const.COLOR_BORDER,
            command=lambda: back(),
            font=("Inter", 18, "bold"),
        
        text_color=const.TEXT_PRIMARY,)
        back_button.grid(row=0, column=0, sticky="W", padx=10)

        # Статистика "Режим просмотра: 1/2"
        stats_Frame = ctk.CTkFrame(
            header_Frame,
            height=30,
            width=190,
            fg_color=const.STATS_FRAME_BG,
            border_width=1,
            border_color=const.FRAME_BORDER,
            corner_radius=15,
        )
        stats_Frame.grid(row=0, column=1, columnspan=2, sticky="E")
        stats_Frame.columnconfigure(0, weight=1)
        stats_Frame.rowconfigure(0, weight=1)
        stats_Frame.grid_propagate(False)

        msg = f"Осталось: {len(cards_for_review) - pointer} / Повторено: {repeated}"

        stats_Label = ctk.CTkLabel(
            master=stats_Frame,
            text=msg,
            font=("Inter", 12, "bold"),
        
        text_color=const.TEXT_PRIMARY,)
        stats_Label.grid(row=0, column=0)

        question_Frame = ctk.CTkFrame(
            app,
            fg_color=const.FRAME_BG,
            height=453,
            width=600,
            border_width=2,
            border_color=const.FRAME_BORDER,
            corner_radius=15,
        )
        question_Frame.grid(row=1, column=0, padx=50)
        question_Frame.columnconfigure(0, weight=1)
        question_Frame.rowconfigure(1, weight=0)
        question_Frame.grid_propagate(False)

        question_Label = ctk.CTkLabel(
            question_Frame,
            text=current_card["question"],
            font=("Inter", 16, "bold"),
        
        text_color=const.TEXT_PRIMARY,)
        question_Label.grid(row=0, column=0, pady=(140, 40))

        answer_Label = ctk.CTkLabel(
            question_Frame,
            text=current_card["answer"],
            font=("Inter", 14),
            text_color=const.FRAME_BG,
        )
        answer_Label.grid(row=1, column=0)

        showAnswer_Button = ctk.CTkButton(
            app,
            text="Показать ответ",
            font=("Inter", 14, "bold"),
            corner_radius=15,
            height=38,
            width=280,
            fg_color=const.BUTTON_PRIMARY_BG,
            command=lambda: showAnswer(
                answer_Label,
                showAnswer_Button,
                buttons_Frame,
                badMark_Button,
                normalMark_Button,
                goodMark_Button,
                easyMark_Button,
            ),
        
        text_color=const.TEXT_PRIMARY,
        hover_color=const.BUTTON_PRIMARY_HOVER)
        showAnswer_Button.grid(row=2, column=0, pady=25)

        buttons_Frame = ctk.CTkFrame(app, fg_color=const.COLOR_BG)

        badMark_Button = ctk.CTkButton(
            buttons_Frame,
            font=("Inter", 14, "bold"),
            fg_color=const.BUTTON_DELETE_BG,
            text="Плохо",
            height=38,
            width=140,
            corner_radius=15,
            border_width=2,
            border_color=const.BUTTON_DELETE_TEXT,
            text_color=const.BUTTON_DELETE_TEXT,
            command=lambda: send_feedback(
                cards_for_review, current_card, pointer, repeated, "bad"
            ),
        hover_color=const.BUTTON_DELETE_HOVER)

        normalMark_Button = ctk.CTkButton(
            buttons_Frame,
            font=("Inter", 14, "bold"),
            fg_color=const.FRAME_BG,
            text="Нормально",
            height=38,
            width=140,
            corner_radius=15,
            border_width=2,
            border_color=const.FRAME_BORDER,
            text_color=const.BUTTON_SECONDARY_TEXT,
            command=lambda: send_feedback(
                cards_for_review, current_card, pointer, repeated, "normal"
            ),
        hover_color=const.FRAME_BG_HOVER)

        goodMark_Button = ctk.CTkButton(
            buttons_Frame,
            font=("Inter", 14, "bold"),
            fg_color=const.BUTTON_GOOD_BG,
            text="Хорошо",
            height=38,
            width=140,
            corner_radius=15,
            border_width=2,
            border_color=const.BUTTON_GOOD_BORDER,
            text_color=const.BUTTON_GOOD_TEXT,
            command=lambda: send_feedback(
                cards_for_review, current_card, pointer, repeated, "good"
            ),
        hover_color=const.BUTTON_GOOD_BG_HOVER)
        easyMark_Button = ctk.CTkButton(
            buttons_Frame,
            font=("Inter", 14, "bold"),
            fg_color=const.BUTTON_EASY_BG,
            text="Легко",
            height=38,
            width=140,
            corner_radius=15,
            border_width=2,
            border_color=const.BUTTON_EASY_BORDER,
            text_color=const.BUTTON_EASY_TEXT,
            command=lambda: send_feedback(
                cards_for_review, current_card, pointer, repeated, "easy"
            ),
        hover_color=const.BUTTON_EASY_BG_HOVER)

    cards_for_review = _get_cards_for_review(deck["id"])
    pointer = 0
    repeated = 0
    render(cards_for_review, pointer, repeated)


def viewer_Window(app, deck):
    def back():
        select_Window(app)

    def go_next(pointer):
        pointer += 1
        render(pointer)

    def go_prev(pointer):
        pointer -= 1
        render(pointer)

    def showAnswer(answer_Label, showAnswer_Button):
        answer_Label.configure(text_color=const.TEXT_PRIMARY)
        showAnswer_Button.configure(
            state="disabled",
            fg_color=const.COLOR_BG,
            text_color=const.COLOR_BG,
            text_color_disabled=const.COLOR_BG,
        )

    def render(pointer):
        if not all_cards:
            alert(app, "В колоде нет карточек", on_close=lambda: back())
            return
        pointer = max(0, min(pointer, len(all_cards) - 1))
        current_card = all_cards[pointer]

        app.configure(fg_color=const.COLOR_BG)
        app.title("PyCards - Просмотр колоды")

        for widget in app.winfo_children():
            widget.destroy()

        for i in range(8):
            app.grid_rowconfigure(i, weight=0)
        app.grid_columnconfigure(0, weight=1)
        app.grid_rowconfigure((0, 1, 2), weight=0)

        # header_frame
        header_Frame = ctk.CTkFrame(
            master=app, height=38, width=740, fg_color=const.COLOR_BG
        )
        header_Frame.grid(row=0, column=0, pady=15, sticky="EW", padx=20)
        header_Frame.rowconfigure(0, weight=1)
        header_Frame.columnconfigure((0, 1, 2), weight=1)
        header_Frame.columnconfigure(0, weight=0)

        # Кнопка "Назад"
        back_button = ctk.CTkButton(
            master=header_Frame,
            image=IMG_ARROW,
            text="",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=const.COLOR_BORDER,
            command=lambda: back(),
            font=("Inter", 18, "bold"),
        
        text_color=const.TEXT_PRIMARY,)
        back_button.grid(row=0, column=0, sticky="W", padx=10)

        # # Статистика "Режим просмотра: 1/2"
        stats_Frame = ctk.CTkFrame(
            header_Frame,
            height=30,
            width=161,
            fg_color=const.STATS_FRAME_BG,
            border_width=1,
            border_color=const.FRAME_BORDER,
            corner_radius=15,
        )
        stats_Frame.grid(row=0, column=1, columnspan=2, sticky="E")
        stats_Frame.columnconfigure(0, weight=1)
        stats_Frame.rowconfigure(0, weight=1)
        stats_Frame.grid_propagate(False)

        msg = f"Режим просмотра: {pointer + 1}/{len(all_cards)}"

        stats_Label = ctk.CTkLabel(
            master=stats_Frame,
            text=msg,
            font=("Inter", 12, "bold"),
        
        text_color=const.TEXT_PRIMARY,)
        stats_Label.grid(row=0, column=0)

        question_Frame = ctk.CTkFrame(
            app,
            fg_color=const.FRAME_BG,
            height=453,
            width=600,
            border_width=2,
            border_color=const.FRAME_BORDER,
            corner_radius=15,
        )
        question_Frame.grid(row=1, column=0, padx=50)
        question_Frame.columnconfigure(0, weight=1)
        question_Frame.rowconfigure(1, weight=0)
        question_Frame.grid_propagate(False)

        question_Label = ctk.CTkLabel(
            question_Frame,
            text=current_card["question"],
            font=("Inter", 16, "bold"),
        
        text_color=const.TEXT_PRIMARY,)
        question_Label.grid(row=0, column=0, pady=(140, 40))

        answer_Label = ctk.CTkLabel(
            question_Frame,
            text=current_card["answer"],
            font=("Inter", 14),
            text_color=const.FRAME_BG,
        )
        answer_Label.grid(row=1, column=0)

        app.grid_rowconfigure(1, weight=0)

        buttons_Frame = ctk.CTkFrame(app, fg_color=const.COLOR_BG)
        buttons_Frame.grid(row=2, column=0, pady=(15, 0))
        buttons_Frame.rowconfigure(0, weight=0)
        buttons_Frame.columnconfigure((0, 1, 2), weight=1)

        prev_Button = ctk.CTkButton(
            buttons_Frame,
            fg_color=const.BUTTON_SECONDARY_BG,
            font=("Inter", 14, "bold"),
            height=38,
            width=123,
            corner_radius=15,
            text="Назад",
            command=lambda: go_prev(pointer),
        
        text_color=const.TEXT_PRIMARY,
        hover_color=const.BUTTON_SECONDARY_HOVER)
        prev_Button.grid(row=0, column=0)
        showAnswer_Button = ctk.CTkButton(
            buttons_Frame,
            fg_color=const.BUTTON_PRIMARY_BG,
            font=("Inter", 14, "bold"),
            height=38,
            width=123,
            corner_radius=15,
            text="Показать ответ",
            command=lambda: showAnswer(answer_Label, showAnswer_Button),
        
        text_color=const.TEXT_PRIMARY,
        hover_color=const.BUTTON_PRIMARY_HOVER)
        showAnswer_Button.grid(row=0, column=1, padx=110)
        next_Button = ctk.CTkButton(
            buttons_Frame,
            fg_color=const.BUTTON_SECONDARY_BG,
            font=("Inter", 14, "bold"),
            height=38,
            width=123,
            corner_radius=15,
            text="Вперед",
            command=lambda: go_next(pointer),
        
        text_color=const.TEXT_PRIMARY,
        hover_color=const.BUTTON_SECONDARY_HOVER)
        next_Button.grid(row=0, column=2)

    all_cards = _get_cards_by_deck(deck["id"])
    pointer = 0
    render(pointer)
