from src.google_calendar import GoogleCalendar
from src.task_scheduler import TaskScheduler
from src.utils import get_last_n_files  # Import utility function

CREDENTIALS_FILE = 'credentials.json'
CALENDAR_ID = 'mariusz.michna.j@gmail.com'
CONFIG_FILE = 'config.yaml'
LAST_N = 1

def main():
    google_calendar = GoogleCalendar(calendar_id=CALENDAR_ID, credentials_file=CREDENTIALS_FILE)
    task_scheduler = TaskScheduler(CONFIG_FILE, google_calendar)

    last_n_files = get_last_n_files(LAST_N)  # Use utility function
    for history_file in last_n_files:
        print(f"Undoing changes from file: {history_file}")
        task_scheduler.undo_added_tasks(history_file.replace('.yaml', ''))

if __name__ == "__main__":
    main()
