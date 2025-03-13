# Bot Discord Inteligent cu Python

## Descriere
Acest proiect implementează un bot inteligent pentru Discord, creat în Python, care poate interacționa cu utilizatorii, răspunde la comenzi textuale, reda muzică în canale audio și folosește API-ul OpenAI pentru generarea inteligentă a răspunsurilor (ChatGPT).

## Funcționalități principale
- Interacțiune textuală cu utilizatorii
- Redare muzică din Soundcloud în canale audio
- Mesaje automate la intrarea/ieșirea membrilor pe server
- Răspunsuri inteligente generate prin ChatGPT (API OpenAI)

## Tehnologii utilizate
- Python
- Discord.py (pentru interacțiunea cu Discord)
- YouTube_dl (pentru gestionarea melodiilor)
- OpenAI API (ChatGPT)
- dotenv (pentru gestionarea cheilor API în siguranță)

## Instalare și rulare
1. Clonează repository-ul:
```
git clone https://github.com/user/bot-discord-python.git
```

2. Creează un mediu virtual și instalează dependențele:
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

3. Configurează fișierul `.env` cu cheile tale:
```env
DISCORD_TOKEN_BOT=token-ul-tau-discord
OPEN_AI_KEY=cheia-ta-openai
```

4. Rulează bot-ul:
```bash
python cod_proiect_bot_discord.py
```

## Exemple comenzi
```bash
!hello
!join
!play <link_soundcloud>
!ask <întrebare>
```

---

# Intelligent Discord Bot with Python

## Description
This project implements an intelligent Discord bot developed in Python. The bot interacts with users, responds to textual commands, plays music in voice channels, and uses OpenAI's API (ChatGPT) for intelligent replies.

## Main Features
- Text-based interaction with users
- Soundcloud music playback in voice channels
- Automatic welcome/goodbye messages for server members
- Intelligent responses using ChatGPT (OpenAI API)

## Technologies Used
- Python
- Discord.py (for Discord interactions)
- YouTube_dl (for music management)
- OpenAI API (ChatGPT)
- dotenv (for secure API key management)

## Installation and Running
1. Clone the repository:
```
git clone https://github.com/user/bot-discord-python.git
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

3. Configure the `.env` file with your API keys:
```env
DISCORD_TOKEN_BOT=your-discord-token
OPEN_AI_KEY=your-openai-key
```

4. Run the bot:
```bash
python cod_proiect_bot_discord.py
```

## Example commands
```bash
!hello
!join
!play <soundcloud_link>
!ask <question>
```

