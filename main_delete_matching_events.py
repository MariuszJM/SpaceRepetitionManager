from src.google_calendar import GoogleCalendar
from src.task_scheduler import TaskScheduler
from src.data_presenter import DataPresenter


def display_matching_events(matching_events):
    """Displays matching events found in Google Calendar."""
    if not matching_events:
        print("No events matching the pattern were found.")
        return

    print("\nFound events:")
    for event in matching_events:
        event_title = event.get("summary", "(Untitled)")
        print(
            f"- {event_title} ({event['start']['dateTime']} - {event['end']['dateTime']})"
        )


def confirm_and_delete_events(task_scheduler, matching_events):
    """Confirms with the user before deleting the matching events."""
    confirm = input("\nAre you sure you want to delete the above events? (y/n): ")

    if confirm.lower() == "y":
        task_scheduler.delete_events(matching_events)
        print("Events have been deleted.")
    else:
        print("Operation canceled. Events were not deleted.")


def main():
    """Main function to manage the retrieval and deletion of matching Google Calendar events."""
    credentials_file = "credentials.json"
    calendar_id = "mariusz.michna.j@gmail.com"
    config_file = "config.yaml"
    data_presenter = DataPresenter()

    google_calendar = GoogleCalendar(
        calendar_id=calendar_id, credentials_file=credentials_file
    )
    task_scheduler = TaskScheduler(config_file, google_calendar, data_presenter)

    matching_events = task_scheduler.get_matching_events(
        pattern="Lot:", start_date="2023-11-10", end_date="2024-01-20"
    )

    display_matching_events(matching_events)

    if matching_events:
        confirm_and_delete_events(task_scheduler, matching_events)


if __name__ == "__main__":
    main()
