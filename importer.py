# Импорт CSV
import csv
import os
from deck_model import create_deck, is_name_taken
from card_model import create_card
from sqlite3 import IntegrityError


def load_deck(filename, encoding, deck_name=None):
    if not deck_name:
        deck_name = os.path.splitext(os.path.basename(filename))[0]
    result = is_name_taken(deck_name)
    if not result[1]:
        deck_id = create_deck(deck_name)
    else:
        deck_id = result[0]["id"]
    try:
        with open(filename, "r", encoding=encoding) as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                if len(row) >= 2:
                    question, answer = row[0], row[1]

                    if question.lower().startswith(
                        "question"
                    ) and answer.lower().startswith("answer"):
                        continue
                else:
                    continue
                try:
                    create_card(deck_id, question, answer)
                except IntegrityError:
                    pass
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
