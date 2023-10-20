from datetime import datetime
from src.google_calendar import GoogleCalendar
from src.task_scheduler import TaskScheduler
from src.utils import get_files_before_datetime

# Global variables
CREDENTIALS_FILE = 'credentials.json'
CALENDAR_ID = 'mariusz.michna.j@gmail.com'
CONFIG_FILE = 'config.yaml'
TARGET_DATETIME = datetime(2023, 10, 20, 12, 37)

def main():
    google_calendar = GoogleCalendar(calendar_id=CALENDAR_ID, credentials_file=CREDENTIALS_FILE)
    task_scheduler = TaskScheduler(CONFIG_FILE, google_calendar)

    history_files_before_datetime = get_files_before_datetime(TARGET_DATETIME)
    for history_file in history_files_before_datetime:
        print(f"Undoing changes from file: {history_file}")
        task_scheduler.undo_added_tasks(history_file.replace('.yaml', ''))

if __name__ == "__main__":
    main()
