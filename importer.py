# Импорт CSV
from card_model import _get_cards_by_deck
import csv
import os
from deck_model import _create_deck, _is_name_taken
from card_model import _create_card
from sqlite3 import IntegrityError


def load_deck(filename, encoding, deck_name=None) -> tuple[int, int] | None:
    """Читаёт файл и создаёт карточки в указанной колоде. По умолчанию пытается получить deck_id по названию переданного файла"""
    if not deck_name:
        deck_name = os.path.splitext(os.path.basename(filename))[0]

    record, exists = _is_name_taken(deck_name)

    if not exists:
        deck_id = _create_deck(deck_name)
    else:
        deck_id = record["id"]

    cards_added = 0
    cards_skipped = 0

    try:
        enc = "utf-8-sig" if encoding.lower() in ("utf-8", "utf8") else encoding
        with open(filename, "r", encoding=enc) as f:
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
                    _create_card(deck_id, first_row[0], first_row[1])
                    cards_added += 1
                except (IntegrityError, IndexError):
                    cards_skipped += 1

            # Основной цикл
            for row in reader:
                if len(row) >= 2:
                    question, answer = row[0], row[1]
                    try:
                        _create_card(deck_id, question, answer)
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


def save_deck(deck_id, filename, path):
    cards = _get_cards_by_deck(deck_id)
    file = f"{filename}.csv"
    full_path = os.path.join(path, file)

    os.makedirs(path, exist_ok=True)

    with open(full_path, "w", encoding="UTF-8", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["question", "answer"])
        for card in cards:
            writer.writerow([card["question"], card["answer"]])

    return full_path


if __name__ == "__main__":
    path = r"E:\Учёба\2 семестр\Программирование\Курсовая\Тестовая папка"
    name = "Файлик"
    deck_id = 160
    save_deck(deck_id, name, path)
