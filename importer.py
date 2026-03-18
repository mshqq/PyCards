# Импорт CSV
import csv
import os
from deck_model import create_deck, is_name_taken
from card_model import create_card
from sqlite3 import IntegrityError


def load_deck(filename, encoding, deck_name=None) -> tuple[int, int] | None:
    """Читаёт файл и создаёт карточки в указанной колоде. По умолчанию пытается получить deck_id по названию переданного файла"""
    if not deck_name:
        deck_name = os.path.splitext(os.path.basename(filename))[0]

    record, exists = is_name_taken(deck_name)

    if not exists:
        deck_id = create_deck(deck_name)
    else:
        deck_id = record["id"]

    cards_added = 0
    cards_skipped = 0

    try:
        with open(filename, "r", encoding=encoding) as f:
            reader = csv.reader(f, delimiter=";")

            # Первая строка
            first_row = next(reader, None)
            if not first_row:
                return

            # Если первая строка - заголовок, идем дальше
            # Если нет - то как данные обрабатываем
            if not (
                first_row[0].lower().startswith("question")
                and first_row[1].lower().startswith("answer")
            ):
                try:
                    create_card(deck_id, first_row[0], first_row[1])
                    cards_added += 1
                except (IntegrityError, IndexError):
                    cards_skipped += 1

            # Основной цикл
            for row in reader:
                if len(row) >= 2:
                    question, answer = row[0], row[1]
                    try:
                        create_card(deck_id, question, answer)
                        cards_added += 1
                    except IntegrityError:
                        cards_skipped += 1
                else:
                    continue
        return cards_added, cards_skipped

    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден.")
    except UnicodeDecodeError:
        print(
            f"Ошибка: Не удалось прочитать файл в кодировке {encoding}. Попробуйте 'UTF-8' или 'CP1251'."
        )


if __name__ == "__main__":
    path = r"E:\Учёба\2 семестр\Программирование\Курсовая\PyCards\test.csv"
    load_deck(
        path,
        encoding="UTF-8",
    )
