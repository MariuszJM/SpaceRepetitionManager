from src.google_calendar import GoogleCalendar
from src.task_scheduler import TaskScheduler


def main():
    # Definicja plików i identyfikatorów
    credentials_file = 'credentials.json'
    calendar_id = 'mariusz.michna.j@gmail.com'  # Zamień na swój adres email powiązany z kalendarzem Google
    config_file = 'config.yaml'

    # Utworzenie instancji klas
    google_calendar = GoogleCalendar(calendar_id=calendar_id, credentials_file=credentials_file)
    task_scheduler = TaskScheduler(config_file, google_calendar)

    # Planowanie zadań
    task_scheduler.delete_events_with_pattern(pattern="(bez tytułu)", start_date="2023-10-10", end_date="2023-11-20")

if __name__ == "__main__":
    main()
