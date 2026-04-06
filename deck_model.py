# Работа с таблицей колод
from db import get_connection
from sqlite3 import IntegrityError, Row


def _create_deck(name: str) -> int | None:
    """Создаёт новую колоду с заданным именем."""
    try:
        with get_connection() as conn:
            cursor = conn.execute("INSERT INTO decks (name) VALUES (?)", (name,))
            return cursor.lastrowid
    except IntegrityError:
        return None


def _get_all_decks() -> list[Row]:
    """Возвращает все колоды в виде списка словарей."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM decks")
        return cursor.fetchall()


def _get_deck_by_id(deck_id):
    """Возвращает колоду по её идентификатору"""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM decks WHERE id = ?", (deck_id,))
        return cursor.fetchone()


def _get_decks_with_counts() -> list[Row]:
    """Возвращает колоды с количеством карточек в каждой."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
                SELECT
                    d.id,
                    d.name,
                    COUNT(c.id) AS card_count
                FROM decks d
                LEFT JOIN cards c ON d.id = c.deck_id
                GROUP BY d.id
            """
        )
        return cursor.fetchall()


def _rename_deck(deck_id: int, new_name: str) -> bool | None:
    """Обновляет название колоды."""
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                    UPDATE decks
                    SET name = ?
                    WHERE id = ? 
                """,
                (new_name, deck_id),
            )
            return cursor.rowcount > 0
    except IntegrityError:
        return False
    except Exception:
        return None


def _delete_deck(deck_id: int) -> bool:
    """Удаляет колоду."""
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
        return cursor.rowcount > 0


def _is_name_taken(name: str) -> bool:
    """Проверяет, существует ли колода с таким именем."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT id FROM decks WHERE name = ?", (name,))
        result = cursor.fetchone()
        return (
            result,
            result is not None,
        )


if __name__ == "__main__":
    print(_rename_deck(133, "Немецкий::Существительные"))
#     # 🌍 Иностранные языки
#     create_deck("Английский::Грамматика")
#     create_deck("Английский::Словарный запас")
#     create_deck("Немецкий::Существительные")
#     create_deck("Испанский::Глаголы")
#     create_deck("Японский::Хирагана")
#     create_deck("Японский::Кандзи")

#     # 💻 Программирование
#     create_deck("Python::Встроенные функции")
#     create_deck("Python::Библиотеки")
#     create_deck("SQL::Команды")
#     create_deck("Алгоритмы и структуры данных")
#     create_deck("Git::Команды")
#     create_deck("Linux::Терминал")

#     # 🔬 Наука и математика
#     create_deck("Математика::Формулы")
#     create_deck("Физика::Законы и константы")
#     create_deck("Химия::Таблица Менделеева")
#     create_deck("Биология::Термины")
#     create_deck("Анатомия::Органы и системы")

#     # 📜 История и география
#     create_deck("История::Древний мир")
#     create_deck("История::XX век")
#     create_deck("История::Даты и события")
#     create_deck("География::Столицы мира")
#     create_deck("География::Флаги стран")

#     # 🎨 Культура и профессия
#     create_deck("Литература::Цитаты")
#     create_deck("Музыка::Теория")
#     create_deck("Философия::Понятия")
#     create_deck("Экономика::Термины")
#     create_deck("Психология::Эффекты и теории")
#     create_deck("Медицина::Симптомы и диагнозы")
#     create_deck("Право::Основные понятия")
#     create_deck("Маркетинг::Инструменты")
#     create_deck("Кулинария::Техники и термины")
#     create_deck("Шахматы::Дебюты")
