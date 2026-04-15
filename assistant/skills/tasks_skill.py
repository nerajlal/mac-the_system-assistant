"""
Tasks Skill — Handles saving reminders, taking notes, and querying the schedule.
"""

import logging
from datetime import datetime
from assistant import memory

def handle_tasks(skill: str, task_data: dict) -> str:
    """
    Main entry point for task-related actions.
    """
    content = task_data.get("content", "")
    due_datetime = task_data.get("due_datetime")
    
    if skill == "set_reminder":
        if not content or not due_datetime:
            return "I'm sorry, I couldn't understand when or what to remind you about."
        
        memory.save_task(content, due_datetime, task_type="reminder")
        # Format for spoken response
        dt_obj = datetime.fromisoformat(due_datetime)
        time_str = dt_obj.strftime("%I:%M %p")
        date_str = dt_obj.strftime("%A, %B %d")
        return f"Got it! I've set a reminder to {content} for {time_str} on {date_str}."

    elif skill == "take_note":
        if not content:
            return "I'm sorry, I didn't catch what you wanted to note down."
        
        # Notes might not have a due_datetime, but we'll save it if they do
        memory.save_task(content, due_datetime, task_type="note")
        return f"Note saved: {content}"

    elif skill == "query_schedule":
        # Extract the date to query (default to today if missing)
        query_date = due_datetime.split('T')[0] if due_datetime else datetime.now().strftime("%Y-%m-%d")
        
        all_tasks = memory.get_all_active_tasks()
        day_tasks = [t for t in all_tasks if t["due_datetime"] and t["due_datetime"].startswith(query_date)]
        
        if not day_tasks:
            if query_date == datetime.now().strftime("%Y-%m-%d"):
                day_tasks = [t for t in all_tasks if not t["due_datetime"]]
                if not day_tasks:
                    return "Your day is clear! No tasks or reminders scheduled."
            else:
                return f"You're all free! Nothing planned for {_friendly_date(query_date)}."

        # Build a natural, conversational response
        total = len(day_tasks)
        date_label = _friendly_date(query_date)
        
        # Count task types for summary
        type_counts = {}
        for t in day_tasks:
            label = t["content"].lower()
            # Try to categorize by keywords
            category = _categorize_task(t["content"])
            type_counts[category] = type_counts.get(category, 0) + 1
        
        # Build summary like "2 meetings and 1 mail"
        summary_parts = []
        for cat, count in type_counts.items():
            summary_parts.append(f"{count} {cat}{'s' if count > 1 else ''}")
        summary_str = " and ".join(summary_parts)
        
        # Opening line
        response = f"You have {total} {'task' if total == 1 else 'tasks'} for {date_label} — {summary_str}. "
        
        # List each task naturally
        task_lines = []
        for i, t in enumerate(day_tasks):
            t_time = datetime.fromisoformat(t["due_datetime"]).strftime("%I:%M %p").lstrip("0")
            task_lines.append(f"{t['content']} at {t_time}")
        
        if len(task_lines) == 1:
            response += task_lines[0] + "."
        elif len(task_lines) == 2:
            response += f"First, {task_lines[0]}, then {task_lines[1]}."
        else:
            response += f"First, {task_lines[0]}, "
            for line in task_lines[1:-1]:
                response += f"then {line}, "
            response += f"and finally {task_lines[-1]}."
                
        return response

    return "I encountered an error handling your task."


def _friendly_date(date_str: str) -> str:
    """Converts a YYYY-MM-DD date string to 'today', 'tomorrow', or a readable name."""
    from datetime import timedelta
    target = datetime.strptime(date_str, "%Y-%m-%d").date()
    today = datetime.now().date()
    
    if target == today:
        return "today"
    elif target == today + timedelta(days=1):
        return "tomorrow"
    else:
        return target.strftime("%A, %B %d")


def _categorize_task(content: str) -> str:
    """Tries to categorize a task into a human-friendly type based on keywords."""
    lower = content.lower()
    if any(w in lower for w in ["meeting", "meet", "standup", "sync", "call"]):
        return "meeting"
    elif any(w in lower for w in ["mail", "email", "send"]):
        return "mail"
    elif any(w in lower for w in ["drink", "eat", "water", "food", "lunch", "snack"]):
        return "reminder"
    else:
        return "task"

