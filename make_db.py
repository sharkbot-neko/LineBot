import sqlite3

def make_db():
    # dbを開く
    dbname = 'SAVE.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    # prefixの保存
    cur.execute("""
    CREATE TABLE IF NOT EXISTS prefix (
        group_id TEXT,
        prefix TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS badword (
        group_id TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS warns (
        group_id TEXT,
        mid TEXT,
        count TEXT
    )
    """)

    # 反映
    conn.commit()