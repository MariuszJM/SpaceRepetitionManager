import os
from datetime import datetime
from collections import defaultdict
import yaml


def get_files_before_datetime(target_datetime):
    folder_path = 'history'
    files = [f for f in os.listdir(folder_path) if f.endswith('.yaml')
             and datetime.strptime(f.replace('.yaml', ''), "%Y%m%d%H%M%S") > target_datetime]
    return sorted(files, reverse=True)

def get_last_n_files(n):
    folder_path = 'history'
    files = [f for f in os.listdir(folder_path) if f.endswith('.yaml')]
    return sorted(files, reverse=True)[:n]


def display_aggregated_undo_changes(files):
    folder_path = 'history'
    aggregated_changes = defaultdict(list)

    for file in files:
        with open(os.path.join(folder_path, file), 'r') as f:
            tasks = yaml.safe_load(f)
            for task in tasks:
                aggregated_changes[task['date']].append(task)

    for date, tasks in aggregated_changes.items():

        updated_existing_event = any(task['updated_existing_event'] for task in tasks)
        if updated_existing_event:
            print(f"Update wydarzenia z dnia {date}:")
        else:
            print(f"Usunięcie wydarzenia z dnia {date}:")

        task_names = [task['tasks'] for task in tasks]
        flattened_task_names = [item for sublist in task_names for item in sublist]

        for task_name in flattened_task_names:
            print(f"  - {task_name}")

