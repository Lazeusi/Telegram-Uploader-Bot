# 🗂 Telegram File Uploader Bot

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)  
[![Aiogram](https://img.shields.io/badge/Aiogram-v3.22.0-green.svg)](https://docs.aiogram.dev/en/latest/)  
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![MongoDB](https://img.shields.io/badge/MongoDB-Connected-brightgreen.svg)](https://www.mongodb.com/)  

A **fast and modular Telegram bot** for uploading files, generating download links, and controlling access with admins and forced join channels/groups.  

---

## 🌟 Features

### 📤 User Features
- Upload any file (photo, video, document) to the bot.  
- Receive **unique download links** for each uploaded file.  
- Access files directly via deep links:  
https://t.me/<bot_username>?start=<file_id>



### 🛡 Admin Features
- **Manage Channels & Groups**
- Add/remove channels/groups via `/channel`.
- Supports **public usernames** and **private invite links**.
- **Admin Management**
- Add new admins: `/add_admin <ID or @username>`.
- Activate yourself if no admin exists: `/active_admin`.
- **Forced Join**
- Users must join required channels/groups to use the bot.
- Inline buttons show required channels/groups with **"✅ Joined"** confirmation.

### ⚡ Technical Details
- Built with **Aiogram v3.22.0**.
- Uses **MongoDB** for persistent storage.
- Fully asynchronous for fast responses.
- Modular codebase:
- `handlers/` → feature-based handlers (`start.py`, `upload.py`, `admin.py`, etc.)
- `middleware/` → user join checks
- `keyboards/inline/` → inline buttons
- Logging and error handling for easy debugging.

---

## 📂 Project Structure

Telegram-Uploader-Bot/
│   .env
│   main.py
│   README.md
│   requirements.txt
│
├───logs
│       bot.log
│
└───src
    │   config.py
    │   logger.py
    │
    ├───database
    │   │   connection.py
    │   │
    │   ├───models
    │   │   │   admin.py
    │   │   │   channel.py
    │   │   │   file.py
    │   │   │   user.py
    │   │
    │   └───__pycache__
    │           connection.cpython-311.pyc
    │
    ├───handlers
    │   │   add_channel.py
    │   │   admin.py
    │   │   channel.py
    │   │   error_handler.py
    │   │   rem_channel.py
    │   │   start.py
    │   │   upload.py
    │   │   view_channel.py
    │   │   __init__.py
    │
    ├───keyboards
    │   ├───inline
    │   │   │   channel.py
    │   │   │   force_join.py
    │   │
    │   └───reply
    ├───middleware
    │   │   user_middleware.py
    │   │   __init__.py
    │
    ├───utils
         │   cash.py

---

## 🚀 Installation

## 1. **Clone the repository**


git clone https://github.com/YourUsername/Telegram-Uploader-Bot.git
cd Telegram-Uploader-Bot
Install dependencies


pip install -r requirements.txt
Create .env file based on .env.example


BOT_TOKEN=your_bot_token_here
MONGO_URI=your_mongodb_connection_string
Run the bot


python main.py
🎮 Usage Guide
## 1️⃣ Upload a File
Start the bot.

Send any file (photo, video, document).

Bot replies with a unique download link.

## 2️⃣ Access File
Click the deep link received from bot:


https://t.me/<bot_username>?start=<file_id>
Bot sends the file automatically.

## 3️⃣ Admin Panel
Add Channel/Group: `/channel`

Add Admin: `/add_admin` <ID or @username>

Activate Admin: `/active_admin`

Example of inline keyboard for channels/groups:


[Channel 1] [Channel 2]
[Group 1]   [Group 2]
## 4️⃣ Forced Join
Users must join required channels/groups.

Inline buttons guide user to join.

After joining, click ✅ Joined to verify.

## ⚙️ Notes
Bot must be admin in channels/groups to check membership.

Works for public and private channels/groups.

Fully async and modular for easy maintenance and extension.

## ✅ Badges & Stats
`Python 3.11`

`Aiogram v3.22.0`

`MongoDB Connected`

`MIT License`