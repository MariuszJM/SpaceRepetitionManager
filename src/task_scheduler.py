import yaml
from datetime import datetime, timedelta


class TaskScheduler:
    def __init__(self, config_file, google_calendar):
        self.config = self.load_config(config_file)
        self.calendar = google_calendar
        self.scheduled_tasks = {}
        self.event_horizon = datetime.now() + timedelta(days=int(self.config['horyzont_zdarzen']))

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)

    def create_scheduled_tasks(self):
        for task in self.config['tasks']:
            start_date = datetime.fromisoformat(task['start_date'])
            task_date = start_date

            for interval in task['intervals']:
                for _ in range(interval['repetitions']):
                    initial_task_date = task_date  # Zapisz oryginalną datę zadania
                    task_date += timedelta(days=interval['range'][0])

                    # Dodana logika przenoszenia zadań na kolejny dzień, gdy osiągnięto limit zadań
                    while not self.can_schedule_task(task, task_date):
                        task_date += timedelta(days=1)

                        if task_date >= self.event_horizon:
                            break

                    if task_date >= self.event_horizon:
                        break

                    # Sprawdzanie, czy zadanie zostało przesunięte poza dozwolony zakres
                    days_delay = (task_date - initial_task_date).days - interval['range'][0]
                    if days_delay > interval['range'][1] - interval['range'][0]:
                        print("============="*4,
                              f"\nZadanie '{task['name']}' zostało przesunięte o {days_delay} dni, "
                              f"\nco przekracza dozwolony zakres od {interval['range'][0]} do {interval['range'][1]} dni."
                              f"\nData zadania: {task_date.strftime('%Y-%m-%d')}.")

                    self._add_task_to_schedule(task_date, task)

    def can_schedule_task(self, task, task_date):
        date_str = task_date.strftime("%Y-%m-%d")
        max_tasks_per_day = self.config.get('max_tasks_per_day', None)

        if task_date.weekday() in task['avoid_days'].get('weekdays', []):
            return False

        if task_date in task['avoid_days'].get('dates', []):
            return False

        if date_str in self.scheduled_tasks and \
                (max_tasks_per_day is not None and len(self.scheduled_tasks[date_str]) >= max_tasks_per_day):
            return False

        if any(t['category'] == task['category'] for t in self.scheduled_tasks.get(date_str, [])):
            return False

        return True

    def _add_task_to_schedule(self, date, task):
        date_str = date.strftime("%Y-%m-%d")
        if date_str not in self.scheduled_tasks:
            self.scheduled_tasks[date_str] = []
        self.scheduled_tasks[date_str].append(task)

    def display_scheduled_tasks(self):
        for date, tasks in sorted(self.scheduled_tasks.items()):
            print(f"Data: {date}")
            for task in tasks:
                print(f" - {task['name']}")

    def add_tasks_to_calendar(self):
        for date_str, tasks in self.scheduled_tasks.items():
            date = datetime.strptime(date_str, "%Y-%m-%d")
            event_description = '\n'.join([f"- {task['name']}" for task in tasks])
            event_start = date.replace(hour=6, minute=0).isoformat()
            event_end = date.replace(hour=23, minute=0).isoformat()

            existing_events = self.calendar.get_events(event_start, event_end)
            event_exists = False

            for event in existing_events:
                if event['summary'] == self.config['event_name']:
                    event_exists = True
                    updated_description = event.get('description', '') + '\n' + event_description
                    update_body = {'description': updated_description.strip(),
                                   'start': event['start'],
                                   'end': event['end']}
                    self.calendar.update_event(event['id'], update_body)
                    break

            if not event_exists:
                self.calendar.create_event(
                    self.config['event_name'],
                    event_description,
                    event_start,
                    event_end
                )

    def delete_events_with_pattern(self, pattern, start_date, end_date):
        # Pobieranie wydarzeń z kalendarza
        events = self.calendar.get_events(start_date, end_date)

        # Filtracja wydarzeń, które zawierają wzorzec w nazwie
        matching_events = [event for event in events if pattern in event.get('summary', "(bez tytułu)")]

        if not matching_events:
            print("Nie znaleziono wydarzeń pasujących do wzorca.")
            return

        # Wyświetlanie wydarzeń do usunięcia
        print("\nZnalezione wydarzenia:")
        for event in matching_events:
            event_title = event.get('summary', "(bez tytułu)")
            print(f"- {event_title} ({event['start']['dateTime']} - {event['end']['dateTime']})")

        # Prośba o potwierdzenie
        confirm = input("\nCzy na pewno chcesz usunąć powyższe wydarzenia? (t/n): ")

        if confirm.lower() == 't':
            # Usuwanie wydarzeń
            for event in matching_events:
                self.calendar.delete_event(event['id'])
            print("Wydarzenia zostały usunięte.")
        else:
            print("Operacja anulowana. Wydarzenia nie zostały usunięte.")

    def undo_last_added_tasks(self):
        # implementacja logiki do cofania ostatnio dodanych zadań (może być potrzebne zastosowanie odpowiedniej struktury danych lub zapisywanie informacji o dodanych zadaniach, aby umożliwić ich wycofanie)
        pass
