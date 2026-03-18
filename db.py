# Инициализация БД
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "cards.db")


def get_connection() -> sqlite3.Connection:
    """Возвращает соединение с БД с включенной поддержкой внешних ключей."""

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Создаёт таблицы decks и cards, если они ещё не существуют."""

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS decks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    UNIQUE NOT NULL,
                created_at  TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS cards (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                deck_id     INTEGER NOT NULL,
                question    TEXT    NOT NULL,
                answer      TEXT    NOT NULL,
                interval    INTEGER DEFAULT 1,
                repetitions INTEGER DEFAULT 0,
                ease_factor REAL    DEFAULT 2.5,
                next_review TEXT    DEFAULT (datetime('now')),
                created_at  TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY(deck_id) REFERENCES decks(id) ON DELETE CASCADE
                UNIQUE(deck_id, question)
            );
        """)
