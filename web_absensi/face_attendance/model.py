import sqlite3
import numpy as np
import face_recognition
from datetime import datetime

DB_NAME = "absensi.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS karyawan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        status TEXT,
        instansi TEXT,
        encoding TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS absensi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        karyawan_id INTEGER,
        waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        keterangan TEXT,
        FOREIGN KEY (karyawan_id) REFERENCES karyawan(id)
    )
    """)

    conn.commit()
    conn.close()

def tambah_karyawan(nama, status, instansi, encoding):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO karyawan (nama, status, instansi, encoding) VALUES (?,?,?,?)",
              (nama, status, instansi, encoding))
    conn.commit()
    conn.close()

def get_karyawan():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM karyawan")
    data = c.fetchall()
    conn.close()
    return data

def absen_karyawan(encoding):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM karyawan WHERE encoding IS NOT NULL")
    data = c.fetchall()

    for row in data:
        saved_enc = np.array(list(map(float, row[4].split(","))))
        match = face_recognition.compare_faces([saved_enc], encoding)[0]
        if match:
            # cek absensi hari ini
            today = datetime.now().strftime("%Y-%m-%d")
            c.execute("SELECT * FROM absensi WHERE karyawan_id=? AND DATE(waktu)=?",
                      (row[0], today))
            existing = c.fetchone()
            if existing:
                conn.close()
                return {"status": "sudah", "msg": f"{row[1]} sudah absen hari ini"}

            c.execute("INSERT INTO absensi (karyawan_id, keterangan) VALUES (?,?)",
                      (row[0], "Hadir"))
            conn.commit()
            conn.close()
            return {"status": "sukses", "msg": f"{row[1]} berhasil absen"}

    conn.close()
    return {"status": "gagal", "msg": "Wajah tidak dikenali"}

def get_absensi():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
    SELECT absensi.id, karyawan.nama, karyawan.status, karyawan.instansi, absensi.waktu, absensi.keterangan
    FROM absensi
    JOIN karyawan ON absensi.karyawan_id = karyawan.id
    ORDER BY absensi.waktu DESC
    """)
    data = c.fetchall()
    conn.close()
    return data
