from tabulate import tabulate
from datetime import datetime, timedelta


class DataPresenter:

    def display_tasks(self, tasks_data):
        if not tasks_data:
            self.display_message("Brak danych do wyświetlenia.")
            return

        tasks_display_data = self.prepare_tasks_display_data(tasks_data)
        self.print_tasks_table(tasks_display_data)

    def prepare_tasks_display_data(self, tasks_data):
        weekdays = [" ", "PN", "WT", "ŚR", "CZ", "PT", "SB", "ND"]
        sorted_dates = sorted(tasks_data.keys())
        first_date = datetime.strptime(sorted_dates[0], "%Y-%m-%d")
        last_date = datetime.strptime(sorted_dates[-1], "%Y-%m-%d")
        rows = [weekdays]
        week_row = [''] * 8
        row_number = 1

        current_date = first_date
        while current_date <= last_date:
            date_str = current_date.strftime("%Y-%m-%d")
            weekday_index = current_date.weekday()

            if date_str in tasks_data:
                content = self.format_content(date_str, tasks_data[date_str])
                week_row[weekday_index + 1] = self.replace_spaces_with_underscores(content)
                week_row[0] = row_number

            current_date += timedelta(days=1)

            if current_date.weekday() == 0 or current_date > last_date:
                if week_row[0]:
                    rows.append(week_row)
                    row_number += 1
                rows.append([''] * 8)
                rows.append(weekdays)
                week_row = [''] * 8

        rows.pop()
        return rows

    def display_task_delay(self, task_name, days_delay, allowed_range, task_date):
        print(
            "=============" * 4,
            f"\nZadanie '{task_name}' zostało przesunięte o {days_delay} dni,",
            f"\nco przekracza dozwolony zakres od {allowed_range[0]} do {allowed_range[1]} dni.",
            f"\nData zadania: {task_date.strftime('%Y-%m-%d')}."
        )

    def format_content(self, date_str, tasks_data):
        formatted_date = date_str.replace('-', '_')
        action = self.get_action(tasks_data)
        if action:
            task_names = ', '.join([item for task in tasks_data for item in task['tasks']])
            task_names_newline = task_names.replace(', ', '\n')
            return f"{formatted_date}\n{action}\n{task_names_newline}"

        task_names = '\n'.join([task['name'] for task in tasks_data])
        return f"{formatted_date}\n{task_names}"

    def get_action(self, tasks_data):
        if 'updated_existing_event' in tasks_data[0]:
            return "UPDATE EVENT" if any(item['updated_existing_event'] for item in tasks_data) else "DELETE EVENT"
        return ""

    def print_tasks_table(self, tasks_display_data):
        print(tabulate(tasks_display_data, tablefmt="grid", stralign="center"))

    def display_message(self, message):
        print(message)

    def replace_spaces_with_underscores(self, content):
        lines = content.split('\n')
        underscored_lines = ['_'.join(line.split()) for line in lines]
        return '\n'.join(underscored_lines)