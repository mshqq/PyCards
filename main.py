# Основное приложение
from db import init_db


def main() -> None:
    init_db()
    print("БД инициализирована.")


if __name__ == "__main__":
    print("PyCards запускается...")
    main()
