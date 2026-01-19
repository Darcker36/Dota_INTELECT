# ⚔️ Dota 2 Impact Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Data Science](https://img.shields.io/badge/Model-Random%20Forest-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Release-brightgreen?style=for-the-badge)

[🇺🇸 **English**](#-english-version) | [🇷🇺 **Русский**](#-russian-version)

---

<a name="-english-version"></a>

## 🇺🇸 English Version

**Stop arguing about who ruined the game. Let the data decide.**
This application analyzes joint matches between two players, uses a Machine Learning model to evaluate their contribution (Impact Score), and visualizes the efficiency gap.

### 🚀 Quick Start

Get it running in 1 minute. You need [Python](https://www.python.org/downloads/) installed.

#### 1. Download
Clone the repository or download the ZIP:
```bash
git clone [https://github.com/YOUR_USERNAME/dota-impact-analyzer.git](https://github.com/YOUR_USERNAME/dota-impact-analyzer.git)
cd dota-impact-analyzer
```
#### 2. Insatll Dependencies
```bash
pip install -r requirements.txt
```
#### 3. Run
```bash
python main.py
```
#### 4. Follow Instructions
1. Enter Your Steam ID and Friend's Steam ID.

2. Wait for the analysis (~30 seconds).

3. Check the console output and the generated result_battle.png chart.

---

## 📊 How It Works (The Science)
Unlike standard KDA stats, which can be misleading, this tool uses a Random Forest model trained on 1000+ ranked matches.

### Key Features:

1. Smart Roles: Automatically detects Core/Support roles based on farm, not just hero pick.

2. Relative Metrics: Uses GPM Ratio (compared to match average) instead of raw GPM to normalize game duration.

3. Weighted Scoring:

    * Core: High weight on Farm Efficiency & Survival.

    * Support: High weight on Assists & XPM. Kills have minimal impact.
---

<a name="-russian-version"></a>

## 🇷🇺 Russian Version

**Узнайте, кто реально тащит в ваших совместных играх.**
Программа анализирует матчи, применяет ML-модель для оценки вклада (Impact Score) и строит график эффективности.

---

## 🚀 Быстрый старт (Инструкция)

Запустите проект за 1 минуту. Вам понадобится установленный Python.

### 1. Скачайте проект
Нажмите зеленую кнопку **Code -> Download ZIP** (и распакуйте) или выполните команду в терминале:
```bash
git clone https://github.com/ВАШ_НИКНЕЙМ/dota-impact-analyzer.git
cd dota-impact-analyzer
```
### 2. Установите библиотеки
Откройте терминал (консоль) в папке с проектом и выполните:
```bash
pip install -r requirements.txt
```
### 3. Запустите
```bash
python main.py
```

### 4. Следуйте инструкциям
1. Программа попросит ввести **ваш Steam ID** и **Steam ID друга**.
   *(ID — это цифры, которые можно найти в ссылке на профиль Dotabuff или в клиенте Dota 2).*
2. Дождитесь окончания анализа (обычно 20-30 секунд).
3. Получите результат в консоли и график в файле `result_battle.png`.

---

## 📊 О проекте: Как это работает?

В отличие от обычной статистики (KDA), которая часто обманчива, этот инструмент использует **алгоритм Машинного Обучения (Random Forest)**, обученный на 1000+ рейтинговых матчах.

### Почему это точнее?
1.  **Умные роли:** Алгоритм сам определяет, кто был Core, а кто Support, и оценивает их по разным критериям.
2.  **Относительные метрики:** Мы не смотрим на "голый" GPM. Мы используем `GPM Ratio` — насколько вы богаче среднего игрока в конкретном матче. Это нивелирует разницу между быстрыми (20 мин) и долгими (60 мин) играми.
3.  **Взвешенные показатели:**
    * Для **Core** важен фарм и выживаемость.
    * Для **Support** критически важны Ассисты и опыт (XPM). Киллы почти не дают очков.

### Пример результата
Программа генерирует график, разделенный на зоны влияния:
* **Зеленые точки:** Победные матчи.
* **Красные точки:** Проигранные матчи.
* **Выше линии:** Друг внес больше импакта.
* **Ниже линии:** Вы внесли больше импакта.

---

## 📂 Файлы проекта

* `main.py` — Главный скрипт запуска.
* `dota_rules.json` — Файл с весами модели ("мозги" программы).
* `requirements.txt` — Список необходимых библиотек.
* `result_battle.png` — (Появляется после запуска) График с результатами.

---

*Разработано в рамках исследования Data Science в киберспорте. При использовании Google Gemini.*