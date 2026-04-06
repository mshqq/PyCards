# Работа с таблицей карточек
from db import get_connection
from sqlite3 import IntegrityError, Row


def _create_card(deck_id: int, question: str, answer: str) -> int | None:
    """Создаёт новую карточку с заданным именем."""
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO cards (deck_id, question, answer) VALUES (?, ?, ?)",
                (deck_id, question, answer),
            )
            return cursor.lastrowid
    except IntegrityError:
        return None


def _get_cards_by_deck(deck_id: int) -> list[Row]:
    """Возвращает все карточки заданной колоды."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM cards WHERE deck_id = ?", (deck_id,))
        return cursor.fetchall()


def _get_card_by_id(card_id) -> Row:
    """Возвращает карточку по её идентификатору"""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
        return cursor.fetchone()


def _update_card(
    card_id: int, question: str = None, answer: str = None, deck_id: int = None
):
    """Обновляет данные карточки по её идентификатору."""
    try:
        with get_connection() as conn:
            current = conn.execute(
                "SELECT question, answer, deck_id FROM cards WHERE id = ?", (card_id,)
            ).fetchone()
            if not current:
                return None

            new_question = question if question is not None else current[0]
            new_answer = answer if answer is not None else current[1]
            new_deck_id = deck_id if deck_id is not None else current[2]

            query = """
            UPDATE cards 
            SET question = ?, answer = ?, deck_id = ?
            WHERE id = ?
            """

            cursor = conn.execute(
                query, (new_question, new_answer, new_deck_id, card_id)
            )
            return cursor.rowcount > 0
    except IntegrityError:
        print(
            f"Ошибка: Не удалось обновить карточку. Колоды с ID {deck_id} не существует"
        )
        return False


def _delete_card(card_id: int) -> bool:
    """Удаляет карточку по её идентификатору"""
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        return cursor.rowcount > 0


def _get_cards_for_review(deck_id: int) -> list[Row]:
    """Возвращает карточки, срок повторения которых наступил или прошёл"""
    query = """
    SELECT *
    FROM cards
    WHERE deck_id = ?
    AND next_review <= datetime('now')
    ORDER BY next_review ASC
    """
    with get_connection() as conn:
        cursor = conn.execute(query, (deck_id,))
        return cursor.fetchall()


def _update_card_sm2(card_id: int, interval: int, repetitions: int, next_review: str):
    """Обновляет SM-2 карточки по её идентификатору."""
    with get_connection() as conn:
        query = """
        UPDATE cards 
        SET interval = ?, repetitions = ?, next_review = ?
        WHERE id = ?
        """

        cursor = conn.execute(query, (interval, repetitions, next_review, card_id))
        return cursor.rowcount > 0


if __name__ == "__main__":
    # Тест на получение всех карточек колоды
    cards = _get_cards_by_deck(1)
    for c in cards:
        print(f"{c['id']} - {c['question']} - {c['answer']}")
    # SUCCESS

    # Тест на обновление SM-2 данных карточки по её идентификатору
    # print(update_card_sm2(1, 2, 3, "2025-10-15 14:30:00"))
    # SUCCESS

    # Тест на обновление внешни данных карточки по её идентификатору.
    # print(update_card(1, question="Произвондая от X", answer="1"))
    # SUCCESS

    # Тест на создание карточки
    # create_card(1, "Вопрос", "Ответ")
    # SUCCESS

    # Тест на получение карточки по её идентификатору
    # card = get_card_by_id(2)
    # print(f"{card['id']} - {card['question']} - {card['answer']}")
    # SUCCESS

    # Тест на получение карточек для повторения
    # cards = get_cards_for_review(1)
    # for c in cards:
    #     print(f"{c['id']} - {c['question']} - {c['answer']}")
    # SUCCESS

    # Тест на удаление карточки
    # delete_card(2)
    # SUCCESS
