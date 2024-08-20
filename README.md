# Spaced Repetition Task Scheduling in Google Calendar

## About the Project

This project automates the scheduling of tasks in Google Calendar, specifically designed to implement the **spaced repetition technique** for learning. By using spaced repetition, tasks are strategically repeated at optimal intervals to enhance memory retention and learning efficiency. Tasks are grouped into a single event per day in Google Calendar, making it easier to manage and track your learning progress.

### Key Features:

- **Spaced Repetition for Learning:** Schedule tasks using intervals that support the spaced repetition technique, helping to solidify knowledge over time.
- **Task Management in Google Calendar:** Automatically group daily tasks into a single event, simplifying task management and retrieval.
- **Custom Repetition Patterns:** Define personalized task repetition schedules that align with your learning goals.
- **History Tracking:** Maintain a record of scheduled tasks, allowing for easy review and undo operations.

## Problem Solving

- **Enhances Learning:** Spaced repetition improves long-term memory retention by strategically timing task reviews.
- **Reduces Overwhelm:** Focuses on daily tasks, minimizing the stress of handling an extensive to-do list.
- **Efficiency:** Automates the scheduling process, ensuring that tasks are organized and spaced correctly for maximum retention.
- **Customizability:** Offers the flexibility to create personalized learning schedules tailored to your specific needs.

## Configuration and Setup

### Prerequisites

- Python 3.9 environment.
- Google Calendar API enabled with credentials obtained from the [Google Developers Console](https://developers.google.com/calendar/api/quickstart/python).

### Configuration (`config.yaml`)

- **`event_name`:** The name of the Google Calendar event where tasks will be listed (e.g., "#Zadania").
- **`task_phrase`:** A keyword to identify tasks in calendar events (e.g., "Zadania").
- **`history_dir`:** The directory where task scheduling history is stored (default: 'history').
- **`max_tasks_per_day`:** The maximum number of tasks allowed per day (e.g., 2).
- **`event_time`:** The time frame for the task event (e.g., `"start": "8:00"`, `"end": "9:00"`).
- **`start_date`:** The starting date for task scheduling (e.g., "today").
- **`intervals`:** A list of intervals that define how tasks are repeated over time to support spaced repetition (e.g., `[1, 1]`, `[2, 4]`).
- **`avoid_days`:** Specifies days to avoid scheduling tasks:
    - **`weekdays`:** A list of weekdays to skip (e.g., `[6]` to avoid Saturdays).
    - **`dates`:** Specific dates to avoid (e.g., `["2024-12-25"]`).

### Basic Usage

1. **Configure `config.yaml`:** Adjust the configuration file to set up intervals that optimize learning through spaced repetition.
2. **Run the Script:**
    
    ```bash
    python main_add_tasks.py
    
    ```
    
    The script will display a preview of the tasks that will be added to your Google Calendar. You can confirm the addition based on the preview.
    

### Undoing Changes

To undo the last set of task additions:

1. **Run the undo script:**
    
    ```bash
    python main_undo_tasks.py
    
    ```
    
    This command will remove the last scheduled tasks according to the history stored.
    

## Conclusion

This project leverages the power of spaced repetition to enhance your learning process by automating task scheduling in Google Calendar. It reduces stress, optimizes knowledge retention, and boosts productivity by focusing on the strategic repetition of tasks.