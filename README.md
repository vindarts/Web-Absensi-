Face Recognition Attendance System (Flask + OpenCV + SQLite)

📌 Project Overview
This project is a web-based attendance system that uses Face Recognition technology to automatically record employee attendance.  
It is built using Flask as backend, SQLite as database, and OpenCV / face recognition for identity verification.

This system simulates a real-world attendance solution used in companies or organizations to improve efficiency and reduce manual attendance errors.

---

🎯 Problem Statement
Manual attendance systems are often inefficient and prone to errors such as:
- Proxy attendance (buddy punching)
- Time-consuming manual input
- Lack of real-time monitoring

This project solves these issues by implementing an automated face recognition-based attendance system.

---

💡 Key Features
- Employee data management (add / store employees)
- Face recognition-based attendance system
- Automatic timestamp recording
- Attendance history tracking
- Simple web-based dashboard
- Sidebar navigation UI

---

🧠 Technologies Used
- Python
- Flask (Web Framework)
- OpenCV / Face Recognition Library
- SQLite (Database)
- HTML, CSS, JavaScript (Frontend)

---

🗄️ Database Structure
Table: karyawan
- id (Primary Key)
- nama (Employee name)
- status (Karyawan / Magang)
- instansi (Company/Institution)
- encoding (Face encoding data)

Table: absensi
- id (Primary Key)
- karyawan_id (Foreign Key)
- waktu (Auto timestamp)
- keterangan (Attendance status)

---

⚙️ System Workflow
1. Employee data is registered into the system
2. Face encoding is stored in the database
3. Camera captures real-time face during attendance
4. System compares captured face with stored encodings
5. If matched, attendance is recorded automatically with timestamp


🚀 How to Run This Project

1. Clone repository
```bash
git clone https://github.com/your-username/your-repo-name.git

pip install -r requirements.txt
python app.py
http://127.0.0.1:5000/
