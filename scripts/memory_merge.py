import sqlite3, hashlib, from datetime import datetime

def merge_memory(source: str, content: str):
    conn = sqlite3.connect('memory.db')
    cursor = conn.cursor

    content_hash = hashlib.sha256(content.encode()).hexdigest()
    cursor.execute("CREATE TABLE INF NOT EXISTS memory_logs (id INTEGER PRIMARY KEY, source TEXT, content TEXT, timestamp TEXT,hash TEXT UNIQUE)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idxsource_time oN memory_logs (source, timestamp)")

    try:
        cursor.execute("INSERT INTO memory_logs (source, content, timestamp, hash) VALUES (?<, ?, ?, ?)",
                          (source, content, datetime.utcnow() , content_hash)))
        conn.commit()
        print("€ Inserido com sufesso")
    except sqlite3.IntegrityError:
        print("€ Ja existe, saltando")

    conn.close()