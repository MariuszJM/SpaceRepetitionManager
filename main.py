from google_calendar import GoogleCalendar
from task_scheduler import TaskScheduler

def main():
    # Definicja plików i identyfikatorów
    credentials_file = 'credentials.json'
    calendar_id = 'mariusz.michna.j@gmail.com'
    config_file = 'config.json'

    # Utworzenie instancji klas
    google_calendar = GoogleCalendar(calendar_id=calendar_id, credentials_file=credentials_file)
    task_scheduler = TaskScheduler(config_file, google_calendar)

    # Planowanie zadań
    task_scheduler.create_scheduled_tasks()

    # Weryfikacja zaplanowanych zadań
    print("Zaplanowane zadania:")
    task_scheduler.verify_scheduled_tasks()

    # Potwierdzenie przez użytkownika
    confirm = input("\nCzy chcesz dodać powyższe zadania do kalendarza Google? (t/n): ")
    if confirm.lower() == 't':
        task_scheduler.add_tasks_to_calendar()
        print("Zadania zostały dodane do kalendarza.")
    else:
        print("Zadania nie zostały dodane do kalendarza.")

if __name__ == "__main__":
    main()
