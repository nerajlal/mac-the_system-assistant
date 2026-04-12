import sqlite3
import os
import logging
from datetime import datetime
from threading import Lock

# Path to the database file
DB_PATH = os.path.join(os.path.dirname(__file__), "memory.db")

# Thread lock for SQLite access
_db_lock = Lock()

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    with _db_lock:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        
        # Table 1: Interactions (Short-term context)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                role TEXT,
                content TEXT
            )
        ''')
        
        # Table 2: User Memories (Long-term facts)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact_key TEXT UNIQUE,
                fact_value TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logging.info(f"Database initialized at {DB_PATH}")

def log_interaction(role: str, content: str):
    """Logs a conversation turn to the database."""
    with _db_lock:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO interactions (role, content) VALUES (?, ?)",
                (role, content)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Failed to log interaction: {e}")

def get_recent_history(limit: int = 5):
    """Retrieves the last N interactions for context."""
    with _db_lock:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, content FROM interactions ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            conn.close()
            # Reverse to get chronological order
            return [{"role": r[0], "content": r[1]} for r in reversed(rows)]
        except Exception as e:
            logging.error(f"Failed to fetch history: {e}")
            return []

def save_memory(key: str, value: str):
    """Saves or updates a learned fact about the user."""
    with _db_lock:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO user_memories (fact_key, fact_value, timestamp) VALUES (?, ?, ?)",
                (key, value, datetime.now().isoformat())
            )
            conn.commit()
            conn.close()
            logging.info(f"Memory saved: {key} = {value}")
        except Exception as e:
            logging.error(f"Failed to save memory: {e}")

def get_all_memories():
    """Returns all learned facts as a dictionary."""
    with _db_lock:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT fact_key, fact_value FROM user_memories ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            conn.close()
            return {r[0]: r[1] for r in rows}
        except Exception as e:
            logging.error(f"Failed to fetch memories: {e}")
            return {}

def delete_memory(key: str):
    """Deletes a specific memory by key."""
    with _db_lock:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_memories WHERE fact_key = ?", (key,))
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Failed to delete memory: {e}")

# Initialize when imported
init_db()
