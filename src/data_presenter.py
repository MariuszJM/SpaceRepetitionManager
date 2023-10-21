from tabulate import tabulate
from datetime import datetime, timedelta


class DataPresenter:

    def display_scheduled_tasks(self, scheduled_tasks):
        if not scheduled_tasks:
            print("Brak zaplanowanych zadań.")
            return

        weekdays = [" ", "PN", "WT", "ŚR", "CZ", "PT", "SB", "ND"]
        sorted_dates = sorted(scheduled_tasks.keys())
        first_date = datetime.strptime(sorted_dates[0], "%Y-%m-%d")
        last_date = datetime.strptime(sorted_dates[-1], "%Y-%m-%d")

        rows = [weekdays]
        week_row = [''] * 8
        row_number = 1

        current_date = first_date
        while current_date <= last_date:
            weekday_index = current_date.weekday()
            date_str = current_date.strftime("%Y-%m-%d")

            if date_str in scheduled_tasks:
                tasks = scheduled_tasks[date_str]
                task_names = '\n'.join([task['name'] for task in tasks])
                content = f"{date_str}\n{task_names}"
                week_row[weekday_index + 1] = content
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
        print(tabulate(rows, tablefmt="grid", stralign="center"))

    def display_message(self, message):
        print(message)
