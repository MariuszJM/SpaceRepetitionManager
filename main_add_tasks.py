from src.google_calendar import GoogleCalendar
from src.task_scheduler import TaskScheduler
from src.data_presenter import DataPresenter

CREDENTIALS_FILE = 'credentials.json'
CALENDAR_ID = 'mariusz.michna.j@gmail.com'
CONFIG_FILE = 'config.yaml'

def main():
    google_calendar = GoogleCalendar(calendar_id=CALENDAR_ID, credentials_file=CREDENTIALS_FILE)
    data_presenter = DataPresenter()
    task_scheduler = TaskScheduler(CONFIG_FILE, google_calendar, data_presenter)
    task_scheduler.create_scheduled_tasks()
    print("Zaplanowane zadania:")
    task_scheduler.display_scheduled_tasks()
    confirm = input("\nCzy chcesz dodać powyższe zadania do kalendarza Google? (t/n): ")
    if confirm.lower() == 't':
        task_scheduler.add_tasks_to_calendar()
        print("Zadania zostały dodane do kalendarza.")
    else:
        print("Zadania nie zostały dodane do kalendarza.")


if __name__ == "__main__":
    main()
