from src.google_calendar import GoogleCalendar
from src.task_scheduler import TaskScheduler
from src.data_presenter import DataPresenter

CREDENTIALS_FILE = "credentials.json"
CALENDAR_ID = "mariusz.michna.j@gmail.com"
CONFIG_FILE = "config.yaml"


def main():
    """
    Main function to orchestrate the task scheduling and insertion into Google Calendar.

    Utilizes GoogleCalendar for calendar interactions, DataPresenter for displaying tasks,
    and TaskScheduler for scheduling tasks based on configuration.
    """
    google_calendar = GoogleCalendar(
        calendar_id=CALENDAR_ID, credentials_file=CREDENTIALS_FILE
    )
    data_presenter = DataPresenter()
    task_scheduler = TaskScheduler(CONFIG_FILE, google_calendar, data_presenter)
    task_scheduler.create_scheduled_tasks()
    print("Scheduled tasks:")
    task_scheduler.display_scheduled_tasks()
    confirm = input("\nDo you want to add the above tasks to Google Calendar? (y/n): ")
    if confirm.lower() == "y":
        task_scheduler.add_tasks_to_calendar()
        print("Tasks have been added to the calendar.")
    else:
        print("Tasks were not added to the calendar.")


if __name__ == "__main__":
    main()
    print("Scheduled tasks")
