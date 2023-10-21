import os
from datetime import datetime


def get_files_before_datetime(target_datetime):
    folder_path = 'history'
    files = [f for f in os.listdir(folder_path) if f.endswith('.yaml')
             and datetime.strptime(f.replace('.yaml', ''), "%Y%m%d%H%M%S") > target_datetime]
    return sorted(files, reverse=True)

def get_last_n_files(n):
    folder_path = 'history'
    files = [f for f in os.listdir(folder_path) if f.endswith('.yaml')]
    return sorted(files, reverse=True)[:n]
