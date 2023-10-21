from src.google_calendar import GoogleCalendar
from src.task_scheduler import TaskScheduler
from src.data_presenter import DataPresenter


def display_matching_events(matching_events):
    if not matching_events:
        print("Nie znaleziono wydarzeń pasujących do wzorca.")
        return

    print("\nZnalezione wydarzenia:")
    for event in matching_events:
        event_title = event.get('summary', "(Bez tytułu)")
        print(f"- {event_title} ({event['start']['dateTime']} - {event['end']['dateTime']})")


def confirm_and_delete_events(task_scheduler, matching_events):
    confirm = input("\nCzy na pewno chcesz usunąć powyższe wydarzenia? (t/n): ")

    if confirm.lower() == 't':
        task_scheduler.delete_events(matching_events)
        print("Wydarzenia zostały usunięte.")
    else:
        print("Operacja anulowana. Wydarzenia nie zostały usunięte.")


def main():
    credentials_file = 'credentials.json'
    calendar_id = 'mariusz.michna.j@gmail.com'
    config_file = 'config.yaml'
    data_presenter = DataPresenter()

    google_calendar = GoogleCalendar(calendar_id=calendar_id, credentials_file=credentials_file)
    task_scheduler = TaskScheduler(config_file, google_calendar, data_presenter)

    matching_events = task_scheduler.get_matching_events(
        pattern="#zadania na dziś",
        start_date="2023-10-10",
        end_date="2023-12-20"
    )

    display_matching_events(matching_events)

    if matching_events:
        confirm_and_delete_events(task_scheduler, matching_events)


if __name__ == "__main__":
    main()
