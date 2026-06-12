# 🎮 Connect 4 Web Game with AI

### Indian Institute of Technology, Palakkad

This repository contains a full-stack, browser-based Connect 4 game. The project connects a custom Python AI engine to a lightweight web interface, allowing users to play matches against either a casual random bot or a smart computer opponent using multiple difficulty levels.

---

## 🧪 Project Architecture & Modules

| Module / File | Topic / Role | Core Concepts Implemented |
| :--- | :--- | :--- |
| **`app.py`** | Web Controller & Routing | Flask routing, state management, HTTP session lockers |
| **`player.py`** | Game Logic & AI Brain | Alpha-Beta Pruning, game trees, matrix-window evaluation functions |
| **`templates/home.html`** | Game Lobby Screen | Mode selection forms (Human vs Bot, Human vs AI) |
| **`templates/difficulty.html`** | AI Configuration Screen | Lookahead depth parameters (Easy, Medium, Hard) |
| **`templates/index.html`** | Active Gameplay Arena | Jinja2 conditional grid looping, circular cell state handling |
| **`static/main.css`** | UI Styling Layout | Clean Flexbox centering, matte token token-coloring |

---

## 🛠️ Tech Stack

* **Language:** Python
* **Web Framework:** Flask
* **Math Library:** NumPy (Matrix manipulation)
* **Frontend:** HTML5, CSS3, Jinja2 Templating

---

## 👨‍💻 Author

* **Jatin Vimal** — B.Tech Data Science & Engineering, IIT Palakkad
