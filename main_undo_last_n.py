from src.google_calendar import GoogleCalendar
from src.task_scheduler import TaskScheduler
from src.utils import get_last_n_files, display_aggregated_undo_changes  # Import utility functions

CREDENTIALS_FILE = 'credentials.json'
CALENDAR_ID = 'mariusz.michna.j@gmail.com'
CONFIG_FILE = 'config.yaml'
LAST_N = 1

def main():
    google_calendar = GoogleCalendar(calendar_id=CALENDAR_ID, credentials_file=CREDENTIALS_FILE)
    task_scheduler = TaskScheduler(CONFIG_FILE, google_calendar)

    last_n_files = get_last_n_files(LAST_N)

    print("Spodziewane zmiany:")
    display_aggregated_undo_changes(last_n_files)

    choice = input("Czy chcesz zatwierdzić te zmiany? (t/n): ").strip().lower()

    if choice == 't':
        for history_file in last_n_files:
            print(f"Undoing changes from file: {history_file}")
            task_scheduler.undo_added_tasks(history_file.replace('.yaml', ''))
        print("Zmiany zostały wprowadzone.")
    else:
        print("Zmiany nie zostały wprowadzone.")

if __name__ == "__main__":
    main()
