# Основное приложение
from db import init_db
import deck_model


def main() -> None:
    init_db()
    print("БД инициализирована.")

    # deck_model.create_deck("Тест")
    # deck_model.create_deck("Тест")

    # decks = deck_model.get_all_decks()
    # for d in decks:
    #     print(d["name"])

    # print("\n")

    # decks_with_counts = deck_model.get_decks_with_counts()
    # for d in decks_with_counts:
    #     print(d["name"], d["card_count"])

    # deck_model.update_deck(2, "Тест")


if __name__ == "__main__":
    print("PyCards запускается...")
    main()
