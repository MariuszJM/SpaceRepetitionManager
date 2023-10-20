from src.google_calendar import GoogleCalendar
from src.task_scheduler import TaskScheduler


def main():
    credentials_file = 'credentials.json'
    calendar_id = 'mariusz.michna.j@gmail.com'
    config_file = 'config.yaml'

    google_calendar = GoogleCalendar(calendar_id=calendar_id, credentials_file=credentials_file)
    task_scheduler = TaskScheduler(config_file, google_calendar)

    task_scheduler.create_scheduled_tasks()

    print("Zaplanowane zadania:")
    task_scheduler.display_scheduled_tasks()

    confirm = input("\nCzy chcesz dodać powyższe zadania do kalendarza Google? (t/n): ")
    if confirm.lower() == 't':
        task_scheduler.add_tasks_to_calendar()
        print("Zadania zostały dodane do kalendarza.")

        undo = input("\nCzy chcesz cofnąć dodanie zadań do kalendarza? (t/n): ")
        if undo.lower() == 't':
            task_scheduler.undo_last_added_tasks()
            print("Dodanie zadań zostało cofnięte.")
        else:
            print("Zadania pozostają w kalendarzu.")

    else:
        print("Zadania nie zostały dodane do kalendarza.")

if __name__ == "__main__":
    main()
