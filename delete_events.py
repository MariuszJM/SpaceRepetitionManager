from src.google_calendar import GoogleCalendar
from src.task_scheduler import TaskScheduler


def main():
    credentials_file = 'credentials.json'
    calendar_id = 'mariusz.michna.j@gmail.com'
    config_file = 'config.yaml'

    google_calendar = GoogleCalendar(calendar_id=calendar_id, credentials_file=credentials_file)
    task_scheduler = TaskScheduler(config_file, google_calendar)

    task_scheduler.delete_events_with_pattern(pattern="#zadania na dziś", start_date="2023-10-10", end_date="2023-12-20")

if __name__ == "__main__":
    main()
