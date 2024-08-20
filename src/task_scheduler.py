import yaml
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import os
from collections import defaultdict
from typing import Dict, Any


class TaskScheduler:
    """Manages task scheduling, including loading configurations, scheduling tasks, and interacting with Google Calendar."""

    def __init__(
        self, config_file: str, google_calendar: Any, data_presenter: Any
    ) -> None:
        """Initializes task scheduler with config file, calendar interface, and data presenter."""
        self.config = self.load_config(config_file)
        self.calendar = google_calendar
        self.data_presenter = data_presenter
        self.set_start_date()
        self.scheduled_tasks = {}
        self.last_history_id = ""
        self.history_dir = self.config.get("history_dir", "history")
        os.makedirs(self.history_dir, exist_ok=True)

    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Loads task configuration from a YAML file."""
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
            return config

    def create_scheduled_tasks(self) -> None:
        """Schedules tasks based on configuration intervals and limitations."""
        for task_name in self.config["tasks"]:
            self.schedule_task(task_name)

    def set_start_date(self) -> None:
        """Sets the start date based on the configuration."""
        if self.config["start_date"].lower() == "yesterday":
            self.start_date = datetime.now() - timedelta(days=1)
        elif self.config["start_date"].lower() == "today":
            self.start_date = datetime.now()
        else:
            self.start_date = datetime.fromisoformat(
                self.config["start_date"]
            ) - timedelta(days=1)

    def schedule_task(self, task_name):
        """Schedules a task according to the intervals defined in the configuration."""
        task_date = self.start_date
        for interval in self.config["intervals"]:
            if task_date is not None:
                task_date = self.schedule_task_for_interval(
                    task_name, interval, task_date
                )

    def schedule_task_for_interval(self, task_name, interval, task_date):
        """Schedules a task for a specific interval."""
        initial_task_date = task_date
        task_date += timedelta(days=interval[0])

        task_date = self.get_next_task_date(task_date)

        if task_date is None:
            return task_date

        self.check_and_display_task_delay(
            task_name, interval, task_date, initial_task_date
        )
        self._add_task_to_schedule(task_date, task_name)
        return task_date

    def get_next_task_date(self, task_date):
        """Finds the next available date for scheduling a task."""
        while not self.can_schedule_task(task_date):
            task_date += timedelta(days=1)
        return task_date

    def check_and_display_task_delay(
        self, task_name, interval, task_date, initial_task_date
    ):
        """Checks if a task is delayed beyond the allowed interval and displays a message if it is."""
        days_to_next_event = (task_date - initial_task_date).days
        if days_to_next_event > interval[1]:
            self.data_presenter.display_task_delay(
                task_name, days_to_next_event, interval, task_date
            )

    def can_schedule_task(self, task_date):
        """Determines if a task can be scheduled on a given date."""
        return self.is_date_available(task_date) and self.is_within_max_tasks_limit(
            task_date
        )

    def is_date_available(self, task_date):
        """Checks if a given date is available for scheduling a task."""
        avoid_days = self.config["avoid_days"]
        return task_date.weekday() not in avoid_days.get(
            "weekdays", []
        ) and task_date not in avoid_days.get("dates", [])

    def is_within_max_tasks_limit(self, task_date):
        """Checks if the number of tasks scheduled for a given date is within the allowed limit."""
        max_tasks_per_day = self.config.get("max_tasks_per_day", None)
        if max_tasks_per_day is not None:
            date_str = task_date.strftime("%Y-%m-%d")
            event_start = task_date.replace(hour=0, minute=0).isoformat()
            event_end = task_date.replace(hour=23, minute=59).isoformat()
            existing_events = self.calendar.get_events(event_start, event_end)

            total_tasks_for_the_day = sum(
                self.count_tasks_in_description(event["description"])
                for event in existing_events
                if self.config["task_phrase"] in event.get("summary", "")
                and date_str in event["start"]["dateTime"]
            ) + len(self.scheduled_tasks.get(date_str, []))

            return total_tasks_for_the_day < max_tasks_per_day

        return True

    def count_tasks_in_description(self, description):
        """Counts the number of tasks in an event description."""
        soup = BeautifulSoup(description, "html.parser")
        tasks = soup.find_all("li")
        return len(tasks)

    def _add_task_to_schedule(self, date, task_name):
        """Adds a task to the schedule for a given date."""
        date_str = date.strftime("%Y-%m-%d")
        if date_str not in self.scheduled_tasks:
            self.scheduled_tasks[date_str] = []
        self.scheduled_tasks[date_str].append(task_name)

    def display_scheduled_tasks(self):
        """Displays the scheduled tasks using the data presenter."""
        self.data_presenter.display_tasks(self.scheduled_tasks)

    def save_tasks_to_history(self, tasks):
        """Saves the scheduled tasks to a history file."""
        self.last_history_id = datetime.now().strftime("%Y%m%d%H%M%S")
        history_file = os.path.join(self.history_dir, f"{self.last_history_id}.yaml")
        with open(history_file, "w") as file:
            yaml.dump(tasks, file)

    def get_matching_events(self, pattern, start_date, end_date):
        """Retrieves events that match a certain pattern within a specified date range."""
        events = self.calendar.get_events(start_date, end_date)
        return [
            event for event in events if pattern in event.get("summary", "(Untitled)")
        ]

    def delete_events(self, events):
        """Deletes specified events from the calendar."""
        for event in events:
            self.calendar.delete_event(event["id"])

    def add_tasks_to_calendar(self):
        """Adds the scheduled tasks to the Google Calendar."""
        added_tasks = []
        for date_str, tasks in self.scheduled_tasks.items():
            date = datetime.strptime(date_str, "%Y-%m-%d")
            event_description = self._create_event_description(tasks)
            event_start_end_time = self._get_event_start_end_time(date)
            event_exists, existing_day_events = self._get_existing_day_events(date)

            if event_exists:
                self._update_existing_event(existing_day_events, event_description)
            else:
                self.calendar.create_event(
                    self.config["event_name"], event_description, *event_start_end_time
                )

            added_tasks.append(
                self._prepare_added_tasks_record(date_str, tasks, event_exists)
            )

        self.save_tasks_to_history(added_tasks)

    def undo_added_tasks(self, history_id):
        """Undoes the tasks added to the calendar by deleting or updating events."""
        history_file = os.path.join(self.history_dir, f"{history_id}.yaml")

        if not os.path.exists(history_file):
            print(f"History file with ID {history_id} not found.")
            return

        with open(history_file, "r") as file:
            tasks = yaml.safe_load(file)

        for task_info in tasks:
            date, end_date, existing_day_events = self._prepare_undo_data(
                task_info["date"]
            )

            for event in existing_day_events:
                if event["summary"] == self.config["event_name"]:
                    self._process_event_undo(task_info, event)
                    break
            else:
                print(f"Cannot find event for date {task_info['date']}")

        self._delete_history_file(history_file)

    def _create_event_description(self, tasks):
        """Creates a description for the event from the list of tasks."""
        return "\n".join([f"- {task_name}" for task_name in tasks])

    def _get_event_start_end_time(self, date):
        """Gets the start and end time for an event."""
        start_hour, start_minute = map(
            int, self.config["event_time"]["start"].split(":")
        )
        return (
            date.replace(hour=start_hour, minute=start_minute).isoformat(),
            date.replace(hour=start_hour, minute=start_minute).isoformat(),
        )

    def _get_existing_day_events(self, date):
        """Retrieves events scheduled on a specific day."""
        existing_day_events = self.calendar.get_events(
            date.replace(hour=0, minute=0).isoformat(),
            date.replace(hour=23, minute=59).isoformat(),
        )
        event_exists = any(
            event["summary"] == self.config["event_name"]
            for event in existing_day_events
        )
        return event_exists, existing_day_events

    def _update_existing_event(self, existing_day_events, event_description):
        """Updates an existing event with new tasks."""
        for event in existing_day_events:
            if event["summary"] == self.config["event_name"]:
                original_description = event.get("description", "")
                updated_description = (
                    original_description.strip() + "\n" + event_description.strip()
                )
                update_body = {
                    "description": updated_description,
                    "start": event["start"],
                    "end": event["end"],
                    "summary": self.config["event_name"],
                    "colorId": event["colorId"],
                }
                self.calendar.update_event(event["id"], update_body)
                break

    def _prepare_added_tasks_record(self, date_str, tasks, event_exists):
        """Prepares a record of the added tasks for saving to history."""
        return {
            "date": date_str,
            "tasks": [task_name for task_name in tasks],
            "updated_existing_event": event_exists,
        }

    def _prepare_undo_data(self, task_info_date):
        """Prepares data for undoing a task addition."""
        date = (
            datetime.strptime(task_info_date, "%Y-%m-%d")
            .replace(hour=0, minute=0)
            .isoformat()
        )
        end_date = (
            datetime.strptime(task_info_date, "%Y-%m-%d")
            .replace(hour=23, minute=59)
            .isoformat()
        )
        existing_day_events = self.calendar.get_events(date, end_date)
        return date, end_date, existing_day_events

    def _process_event_undo(self, task_info, event):
        """Processes the undo of an event by either updating or deleting it."""
        if task_info["updated_existing_event"]:
            original_description = event.get("description", "").split("\n")
            updated_description = "\n".join(
                original_description[: -len(task_info["tasks"])]
            ).strip()
            update_body = {
                "description": updated_description,
                "start": event["start"],
                "end": event["end"],
                "summary": self.config["event_name"],
                "colorId": event["colorId"],
            }
            self.calendar.update_event(event["id"], update_body)
        else:
            self.calendar.delete_event(event["id"])

    def _delete_history_file(self, history_file):
        """Deletes a history file after tasks have been undone."""
        try:
            os.remove(history_file)
            print(f"History file {history_file} has been deleted.")
        except Exception as e:
            print(f"Failed to delete history file {history_file}. Error: {e}")

    def aggregate_undo_changes(self, files):
        """Aggregates changes to be undone from multiple history files."""
        folder_path = self.history_dir
        aggregated_changes = defaultdict(list)

        for file in files:
            with open(os.path.join(folder_path, file), "r") as f:
                tasks = yaml.safe_load(f)
                for task in tasks:
                    aggregated_changes[task["date"]].append(task)

        return aggregated_changes

    def get_files_before_datetime(self, target_datetime):
        """Gets history files created before a specific datetime."""
        folder_path = self.history_dir
        files = [
            f
            for f in os.listdir(folder_path)
            if f.endswith(".yaml")
            and datetime.strptime(f.replace(".yaml", ""), "%Y%m%d%H%M%S")
            > target_datetime
        ]
        return sorted(files, reverse=True)

    def get_last_n_files(self, n):
        """Gets the last n history files."""
        folder_path = self.history_dir
        files = [f for f in os.listdir(folder_path) if f.endswith(".yaml")]
        return sorted(files, reverse=True)[:n]
