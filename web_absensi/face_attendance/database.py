import sqlite3

def init_db():
    conn = sqlite3.connect("absensi.db")
    c = conn.cursor()

    # Tabel Karyawan
    c.execute("""
    CREATE TABLE IF NOT EXISTS karyawan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        status TEXT NOT NULL, -- Karyawan / Magang
        instansi TEXT,
        encoding TEXT
    )
    """)

    # Tabel Absensi
    c.execute("""
    CREATE TABLE IF NOT EXISTS absensi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        karyawan_id INTEGER,
        waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        keterangan TEXT,
        FOREIGN KEY (karyawan_id) REFERENCES karyawan (id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database berhasil dibuat ✅")
