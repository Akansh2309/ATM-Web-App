# 🏦 Federal Reserve Virtual ATM

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/akansh-shaw/ATM-Web-App)

![ATM Banner](https://img.shields.io/badge/Status-Live%20on%20Render-brightgreen?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python) ![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask) ![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)

## 🚀 About This Project
Welcome to the Virtual ATM Web App! Originally a command-line script, this project has been fully transformed into a **robust, official-looking Web Application**. 

It simulates a highly secure, government-style ATM kiosk featuring real-time database transactions, encrypted credentials, and advanced banking logic.

## ✨ Features
* **🔒 Secure Authentication:** Multi-user support with Werkzeug-encrypted PIN hashing.
* **🏦 Multi-Account System:** Manage both **Checking** and **Savings** accounts effortlessly.
* **💸 Advanced Transactions:** Deposit, withdraw, transfer, and pay government taxes.
* **📜 Transaction History:** View detailed, timestamped mini-statements for all activities.
* **🎨 Official Kiosk UI:** A beautiful, responsive, dark-mode web interface mimicking a secure government ATM.

## 🛠️ The Tech Stack
* **Backend:** Python 3 & Flask
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3 (Custom Brutalist/Government styling)
* **Deployment:** Render (with Gunicorn)

## 💻 How to Run It Locally
Want to host your own ATM kiosk?

1. **Clone the repository:**
   ```bash
   git clone https://github.com/akansh-shaw/ATM-Web-App.git
   cd ATM-Web-App
   ```
2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Flask server:**
   ```bash
   python app.py
   ```
4. **Access the ATM:** Open your browser and navigate to `http://localhost:5000`

---
*Created by Akansh Shaw. Now upgraded into a full-stack Web Application!* ✌️
