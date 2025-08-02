# 🗳️ Blockchain Voting System

A secure, transparent, and tamper-proof voting system built using Python and Flask, backed by blockchain technology. Designed to simulate a real-world voting process using blockchain principles for integrity and trust.

---

## 🚀 Features

- Blockchain-based vote recording
- Admin and Voter login system
- Passwords securely hashed using Werkzeug
- Vote tracking and results display
- Simple web interface (HTML + Flask)
- Double voting prevention during active session

---

## 🛠️ Tech Stack

- Frontend: HTML, CSS (Flask templates)
- Backend: Python, Flask
- Security: Werkzeug password hashing
- Blockchain: Custom implementation (no external libraries)
- Data Storage: JSON files

---

## 📁 Project Structure

Blockchain-Voting-System/
├── app.py                  # Main Flask app (routes + logic)
├── blockchain.py           # Blockchain class & validation
├── blockchain_data.json    # Stores blockchain (vote) data
├── users.json              # Stores user credentials (hashed)
├── templates/              # HTML templates (Flask)
│   ├── login.html
│   ├── vote.html
│   └── result.html
├── static/                 # CSS or JS files (optional)
├── .flaskenv               # Flask environment config
├── venv/                   # Python virtual environment
└── README.md               # This file

---

## ⚙️ Setup Instructions

1. Clone the repository:
   git clone https://github.com/RishAbh-8821/BlockChain-Voting-System.git
   cd BlockChain-Voting-System

2. Set up virtual environment:
   python -m venv venv
   venv\Scripts\activate    # (for Windows)

3. Install dependencies:
   pip install -r requirements.txt

   OR manually:
   pip install flask
   pip install werkzeug

4. Run the Flask app:
   flask run

   Open in browser: http://127.0.0.1:5000

---

## 🔐 Login Credentials

Admin:
- Username: admin
- Password: admin123

Voters:
- voter1 → voter123
- voter2 → voter123

(You can add more voters in users.json)

---

## 📊 How Voting Works

1. Voters login with their credentials.
2. Each voter can cast one vote per session.
3. Votes are recorded as blocks in a custom blockchain.
4. Blockchain data is saved in blockchain_data.json.
5. Admin can view current voting results.

Note: Votes and users reset every time the server restarts. For persistent data, implement DB storage.

---

## 📦 Dependencies (requirements.txt)

Flask==2.3.3
Werkzeug==3.0.1

---

## 🧠 Future Improvements

- Store data in an actual database (SQLite / PostgreSQL)
- Prevent double voting across sessions
- Implement OTP/email verification
- Encrypt user and blockchain data
- Deploy online using Render or Heroku


---

## 🙌 Author

Made by Rishabh Tripathi  
CSE (AI) @ PSIT Kanpur  
GitHub: https://github.com/RishAbh-8821  
Email: rishabhkt421@gmail.com  
LinkedIn: www.linkedin.com/in/rishabh-tripathi21
