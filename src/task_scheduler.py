import yaml
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import os


class TaskScheduler:
    def __init__(self, config_file, google_calendar):
        self.config = self.load_config(config_file)
        self.calendar = google_calendar
        self.scheduled_tasks = {}
        self.set_event_horizon()
        self.last_history_id = ''
        self.history_dir = self.config.get('history_dir', 'history')
        os.makedirs(self.history_dir, exist_ok=True)

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)

    def set_event_horizon(self):
        self.event_horizon = datetime.now() + timedelta(days=int(self.config['horyzont_zdarzen']))

    def create_scheduled_tasks(self):
        for task in self.config['tasks']:
            self.schedule_task(task)

    def schedule_task(self, task):
        start_date = datetime.fromisoformat(task['start_date'])
        task_date = start_date

        for interval in task['intervals']:
            self.schedule_task_for_interval(task, interval, task_date)

    def schedule_task_for_interval(self, task, interval, task_date):
        for _ in range(interval['repetitions']):
            initial_task_date = task_date
            task_date += timedelta(days=interval['range'][0])

            task_date = self.get_next_task_date(task, task_date)

            if task_date is None:
                return

            self.check_task_delay(task, interval, task_date, initial_task_date)
            self._add_task_to_schedule(task_date, task)

    def get_next_task_date(self, task, task_date):
        while not self.can_schedule_task(task, task_date):
            task_date += timedelta(days=1)

            if task_date >= self.event_horizon:
                return None

        return task_date

    def check_task_delay(self, task, interval, task_date, initial_task_date):
        days_delay = (task_date - initial_task_date).days - interval['range'][0]

        if days_delay > interval['range'][1] - interval['range'][0]:
            print(
                "=============" * 4,
                f"\nZadanie '{task['name']}' zostało przesunięte o {days_delay} dni,",
                f"\nco przekracza dozwolony zakres od {interval['range'][0]} do {interval['range'][1]} dni.",
                f"\nData zadania: {task_date.strftime('%Y-%m-%d')}."
            )

    def can_schedule_task(self, task, task_date):
        return (self.is_date_available(task, task_date) and
                self.is_category_available(task, task_date) and
                self.is_within_max_tasks_limit(task, task_date))

    def is_date_available(self, task, task_date):
        return (task_date.weekday() not in task['avoid_days'].get('weekdays', []) and
                task_date not in task['avoid_days'].get('dates', []))

    def is_category_available(self, task, task_date):
        date_str = task_date.strftime("%Y-%m-%d")
        return not any(t['category'] == task['category'] for t in self.scheduled_tasks.get(date_str, []))

    def is_within_max_tasks_limit(self, task, task_date):
        max_tasks_per_day = self.config.get('max_tasks_per_day', None)
        if max_tasks_per_day is not None:
            date_str = task_date.strftime("%Y-%m-%d")
            event_start = task_date.replace(hour=0, minute=0).isoformat()
            event_end = task_date.replace(hour=23, minute=59).isoformat()
            existing_events = self.calendar.get_events(event_start, event_end)

            total_tasks_for_the_day = sum(
                self.count_tasks_in_description(event['description'])
                for event in existing_events
                if self.config['task_phrase'] in event.get('summary', '')
                and date_str in event['start']['dateTime']
            ) + len(self.scheduled_tasks.get(date_str, []))

            return total_tasks_for_the_day < max_tasks_per_day

        return True

    def count_tasks_in_description(self, description):
        soup = BeautifulSoup(description, 'html.parser')
        tasks = soup.find_all('li')
        return len(tasks)

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
        added_tasks = []
        for date_str, tasks in self.scheduled_tasks.items():
            date = datetime.strptime(date_str, "%Y-%m-%d")
            event_description = '\n'.join([f"- {task['name']}" for task in tasks])
            event_start = date.replace(hour=int(self.config['event_time']['start'].split(':')[0]),
                                       minute=int(self.config['event_time']['start'].split(':')[1])).isoformat()
            event_end = date.replace(hour=int(self.config['event_time']['start'].split(':')[0]),
                                     minute=int(self.config['event_time']['start'].split(':')[1])).isoformat()
            existing_day_events = self.calendar.get_events(date.replace(hour=0, minute=0).isoformat(),
                                                           date.replace(hour=23, minute=59).isoformat())
            event_exists = False

            for event in existing_day_events:
                if event['summary'] == self.config['event_name']:
                    event_exists = True
                    original_description = event.get('description', '')
                    updated_description = original_description + '\n' + event_description
                    update_body = {'description': updated_description.strip(),
                                   'start': event['start'],
                                   'end': event['end'],
                                   'summary': self.config['event_name']}
                    self.calendar.update_event(event['id'], update_body)
                    break

            if not event_exists:
                self.calendar.create_event(
                    self.config['event_name'],
                    event_description,
                    event_start,
                    event_end
                )
            added_tasks.append({
                'date': date_str,
                'tasks': [task['name'] for task in tasks],
                'updated_existing_event': event_exists
            })
        self.save_tasks_to_history(added_tasks)

    def save_tasks_to_history(self, tasks):
        self.last_history_id = datetime.now().strftime("%Y%m%d%H%M%S")
        history_file = os.path.join(self.history_dir, f'{self.last_history_id}.yaml')
        with open(history_file, 'w') as file:
            yaml.dump(tasks, file)

    def get_matching_events(self, pattern, start_date, end_date):
        events = self.calendar.get_events(start_date, end_date)
        return [event for event in events if pattern in event.get('summary', "(Bez tytułu)")]

    def delete_events(self, events):
        for event in events:
            self.calendar.delete_event(event['id'])

    def undo_added_tasks(self, history_id):
        history_file = os.path.join(self.history_dir, f'{history_id}.yaml')
        if not os.path.exists(history_file):
            print(f"Nie znaleziono pliku historii o ID {history_id}")
            return

        with open(history_file, 'r') as file:
            tasks = yaml.safe_load(file)

        for task_info in tasks:
            date = datetime.strptime(task_info['date'], "%Y-%m-%d").replace(hour=0, minute=0).isoformat()
            end_date = datetime.strptime(task_info['date'], "%Y-%m-%d").replace(hour=23, minute=59).isoformat()
            existing_day_events = self.calendar.get_events(date, end_date)

            for event in existing_day_events:
                if event['summary'] == self.config['event_name']:
                    if task_info['updated_existing_event']:
                        # Zaktualizuj opis wydarzenia, aby usunąć ostatnio dodane zadania
                        original_description = event.get('description', '').split('\n')
                        updated_description = '\n'.join(original_description[:-len(task_info['tasks'])]).strip()
                        update_body = {'description': updated_description,
                                       'start': event['start'],
                                       'end': event['end'],
                                       'summary': self.config['event_name']}
                        self.calendar.update_event(event['id'], update_body)
                    else:
                        # Usuń wydarzenie, jeśli zostało utworzone w ostatniej operacji
                        self.calendar.delete_event(event['id'])
                    break
            else:
                print(f"Nie można odnaleźć wydarzenia dla daty {task_info['date']}")