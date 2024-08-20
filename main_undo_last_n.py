from src.google_calendar import GoogleCalendar
from src.task_scheduler import TaskScheduler
from src.data_presenter import DataPresenter

LAST_N = 1
CREDENTIALS_FILE = "credentials.json"
CALENDAR_ID = "mariusz.michna.j@gmail.com"
CONFIG_FILE = "config.yaml"


def main():
    """Main function to undo the last set of scheduled tasks in Google Calendar."""
    google_calendar = GoogleCalendar(
        calendar_id=CALENDAR_ID, credentials_file=CREDENTIALS_FILE
    )
    data_presenter = DataPresenter()
    task_scheduler = TaskScheduler(CONFIG_FILE, google_calendar, data_presenter)

    last_n_files = task_scheduler.get_last_n_files(LAST_N)

    print("Expected changes:")
    aggregated_changes = task_scheduler.aggregate_undo_changes(last_n_files)
    data_presenter.display_tasks(aggregated_changes)

    choice = input("Do you want to confirm these changes? (y/n): ").strip().lower()

    if choice == "y":
        for history_file in last_n_files:
            print(f"Undoing changes from file: {history_file}")
            task_scheduler.undo_added_tasks(history_file.replace(".yaml", ""))
        print("Changes have been applied.")
    else:
        print("Changes have not been applied.")


if __name__ == "__main__":
    main()
