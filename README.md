🚀 Advanced URL Shortener

A full-featured URL Shortener built using Flask, SQLite, and modern UI design.
This project allows users to create short links, track clicks, set expiry dates, and manage links through a clean dashboard.

🌟 Features

🔗 Shorten long URLs

✨ Custom short codes

📊 Click counter tracking

⏳ Expiry date option

🔍 Search functionality in history

❌ Delete links

🌙 Dark / Light mode toggle

📋 Copy short link button

🎨 Modern responsive UI

🗂 Template-based structure (Flask + Jinja2)

🛠 Tech Stack

Backend: Flask (Python)

Database: SQLite

Frontend: HTML, CSS, JavaScript

Deployment: Render

Server: Gunicorn

📂 Project Structure
CodeAlpha_URLShortener
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── templates
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   └── history.html

⚙️ Installation (Run Locally)
1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/CodeAlpha_URLShortener.git
cd CodeAlpha_URLShortener

2️⃣ Create Virtual Environment
python -m venv venv
Activate:
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the App
python app.py

Open in browser:

http://127.0.0.1:5000

🌍 Live Demo

👉 Deployed on Render
🔗 https://smart-url-shortener-yuqm.onrender.com/

📌 Future Improvements

User authentication
Permanent cloud database (PostgreSQL)
QR code generation for links
Analytics dashboard
Rate limiting
