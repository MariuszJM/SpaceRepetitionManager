#!/bin/bash

# Utworzenie struktury katalogów projektu
mkdir -p src

# Utworzenie plików Python
echo 'from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone

# Zawartość klasy GoogleCalendar
# ...

' > src/google_calendar.py

echo 'import json
import yaml
from datetime import datetime, timedelta

# Zawartość klasy TaskScheduler
# ...

' > src/task_scheduler.py

echo 'from google_calendar import GoogleCalendar
from task_scheduler import TaskScheduler

# Zawartość pliku main_add_tasks.py
# ...

' > main_add_tasks.py

# Utworzenie pliku konfiguracyjnego YAML
echo 'event_name: "#zadania na dziś"
event_time:
  start: "8:00"
  end: "9:00"

horyzont_zdarzen: 42

tasks:
  - name: "Ćwiczenie 1"
    category: "exercise"
    start_date: "2023-10-17"
    intervals:
      - range: [1, 1]
        repetitions: 3
      - range: [2, 4]
        repetitions: 1
      - range: [5, 10]
        repetitions: 1
    avoid_days:
      weekdays: [5, 6]
      dates: ["2023-10-25"]

  - name: "Czytanie"
    category: "learning"
    start_date: "2023-10-17"
    intervals:
      - range: [1, 1]
        repetitions: 2
      - range: [3, 5]
        repetitions: 1
    avoid_days:
      weekdays: [6]
      dates: []
' > config.yaml

# Nadanie uprawnień wykonywalnych dla pliku main_add_tasks.py
chmod +x main_add_tasks.py

echo "Projekt został stworzony!"
