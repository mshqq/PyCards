# Работа с таблицей колод
from unittest import result
from db import get_connection
from sqlite3 import IntegrityError, Row


def create_deck(name: str) -> int | None:
    """Создаёт новую колоду с заданным именем."""
    try:
        with get_connection() as conn:
            cursor = conn.execute("INSERT INTO decks (name) VALUES (?)", (name,))
            return cursor.lastrowid
    except IntegrityError:
        return None


def get_all_decks() -> list[Row]:
    """Возвращает все колоды в виде списка словарей."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM decks")
        return cursor.fetchall()


def get_decks_with_counts() -> list[Row]:
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


def update_deck(deck_id: int, new_name: str) -> bool | None:
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
        return None


def delete_deck(deck_id: int) -> bool:
    """Удаляет колоду."""
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
        return cursor.rowcount > 0


def is_name_taken(name: str) -> bool:
    """Проверяет, существует ли колода с таким именем."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT id FROM decks WHERE name = ?", (name,))
        result = cursor.fetchone()
        return (
            result,
            result is not None,
        )


if __name__ == "__main__":
    print(is_name_taken("test"))
    # create_deck("test")
