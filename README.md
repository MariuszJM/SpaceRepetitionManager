# Task Insertion to Google Calendar

## About the Project

This project is designed to streamline the process of managing daily tasks by utilizing Google Calendar events as a centralized task list. The primary goal is to reduce the feeling of being overwhelmed by focusing solely on tasks that need to be accomplished today. 

### Key Features:
- **Task Management in Google Calendar:** Tasks for the day are stored in a single event, making them easy to access and manage.
- **Integration with Notion:** The list of tasks can be copied from the Google Calendar event and pasted into a Notion Kanban board, where tasks are automatically formatted and organized.
- **Custom Repetition Patterns:** Supports defining custom repetition patterns for tasks, beyond what Google Calendar offers, including spaced repetition for reinforcing knowledge over time.

## Problem Solving
- **Reduces Overwhelm:** By focusing on just the day's tasks, it minimizes the anxiety of managing a long to-do list.
- **Efficiency:** Streamlines the process of transferring tasks to Notion, saving time and effort.
- **Customizability:** Allows for the creation of personalized task repetition schedules to enhance learning and task management.

## Configuration and Setup

### Prerequisites
- Python environment setup. (Pyton 3.9)
- Google Calendar API enabled and credentials obtained. (https://developers.google.com/calendar/api/quickstart/python)

### Configuration (`config.yaml`)
- `event_name`: Name of the Google Calendar event where tasks will be listed (e.g., "#Tasks_for_Today").
- `history_dir`: Directory to store task history.
- `max_tasks_per_day`: Maximum number of tasks to schedule per day.
- `event_time`: The start and end time for the task event.
- `event_horizon`: The end date for scheduling tasks.
- `tasks`: List of tasks with detailed properties:
  - `name`: Unique identifier for the task.
  - `category`: Type or category of the task (e.g., "exercise").
  - `start_date`: The date when the task scheduling starts.
  - `intervals`: Defines repetition intervals and their frequency. Each interval has:
    - `range`: A list with two elements that specify the starting and ending days for the interval. This range helps to manage workload by setting specific times for task occurrences, thus preventing overload.
    - `repetitions`: How many times the task should repeat within this interval.
  - `avoid_days`: Specifies days to avoid scheduling tasks.
    - `weekdays`: A list of weekdays to skip (0=Sunday, 6=Saturday).
    - `dates`: Specific dates to avoid (e.g., ["2024-12-25"] for Christmas).

### Basic Usage
1. **Modify `config.yaml`** according to your task scheduling needs.
2. **Execute the script**:

python main_add_tasks.py

When you run the script, you will be presented with a preview of the tasks proposed to be added to your calendar, including those placed outside the defined interval ranges. 
If you approve, the script will automatically insert the tasks into your Google Calendar based on the configurations set in `config.yaml`.

## Conclusion

By automating the process of task management through Google Calendar and Notion, this project aims to simplify daily planning, reduce stress, and enhance productivity through custom task repetition patterns.
