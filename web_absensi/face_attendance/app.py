from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from model import init_db, tambah_karyawan, get_karyawan, absen_karyawan, get_absensi
import cv2
import numpy as np
import face_recognition
from datetime import date
from PIL import Image
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Inisialisasi database saat pertama kali jalan
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    today = date.today()
    
    total_karyawan = len(get_karyawan())
    absensi = get_absensi()
    
    hadir_hari_ini = sum(1 for a in absensi if a[4].split()[0] == str(today))
    total_kehadiran = len(absensi)
    
    return render_template(
        "dashboard.html", 
        absensi=absensi,
        total_karyawan=total_karyawan,
        hadir_hari_ini=hadir_hari_ini,
        total_kehadiran=total_kehadiran
    )

@app.route("/kelola", methods=["GET", "POST"])
def kelola():
    if request.method == "POST":
        nama = request.form["nama"]
        status = request.form["status"]
        instansi = request.form["instansi"] if status == "Mahasiswa Magang" else "-"
        foto = request.files["foto"]

        # Validasi format gambar
        valid_image_types = ['image/jpeg', 'image/png', 'image/gif']
        if foto.content_type not in valid_image_types:
            flash("Format gambar tidak valid. Harap unggah gambar dalam format JPEG, PNG, atau GIF.", "error")
            return redirect(url_for("kelola"))

        # Membaca dan memproses gambar
        try:
            # pastikan 'foto' adalah objek file dari form Flask (request.files)
            image = Image.open(foto).convert("RGB")
            image = image.resize((640, 480))
            
            # ubah ke array numpy (dan pastikan dtype uint8)
            img_array = np.copy(np.array(image, dtype=np.uint8))

            # cek informasi array
            print("Shape:", img_array.shape, "Dtype:", img_array.dtype)

            # pastikan array contiguous (opsional tapi aman)
            img_array = np.ascontiguousarray(img_array, dtype=np.uint8)

            # deteksi wajah
            face_encodings = face_recognition.face_encodings(img_array)

            if len(face_encodings) == 0:
                flash("Wajah tidak terdeteksi, coba lagi.", "error")
                return redirect(url_for("kelola"))

            # konversi encoding ke string
            encoding_str = ",".join([str(v) for v in face_encodings[0]])

        except Exception as e:
            flash(f"Error membuka gambar: {str(e)}", "error")
            return redirect(url_for("kelola"))



        # Simpan data karyawan
        try:
            tambah_karyawan(nama=nama, status=status, instansi=instansi, encoding=encoding_str)
            flash("Karyawan berhasil ditambahkan!", "success")
        except Exception as e:
            flash(f"Terjadi kesalahan saat menyimpan data karyawan: {str(e)}", "error")
            return redirect(url_for("kelola"))

        return redirect(url_for("kelola"))

    karyawan = get_karyawan()
    return render_template("kelola.html", karyawan=karyawan)


@app.route("/absen", methods=["POST"])
def absen():
    file = request.files["frame"]
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    encodings = face_recognition.face_encodings(rgb_img)
    if len(encodings) == 0:
        return jsonify({"status": "gagal", "msg": "Wajah tidak terdeteksi"})

    encoding = encodings[0]
    result = absen_karyawan(encoding)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
