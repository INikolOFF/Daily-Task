import tkinter as tk
from tkinter import messagebox
from datetime import datetime

tasks = []  # List of tasks, each as a tuple (task_name, deadline)
reminded_tasks = set()  # NEW: keep tasks already reminded

# Function to load tasks from a file
def load_tasks():
    try:
        with open("tasks.txt", "r") as file:  # Open file for reading
            for line in file:
                if ";" in line:
                    # Split each line into task name and deadline
                    name, deadline = line.strip().split(";", 1)
                    tasks.append((name, deadline))
    except FileNotFoundError:
        pass  # If file does not exist, continue without error

# Function to save tasks to a file
def save_tasks():
    with open("tasks.txt", "w") as file:  # Open file for writing
        for task, deadline in tasks:
            file.write(f"{task};{deadline}\n")  # Write task and deadline separated by ;

# Load tasks when program starts
load_tasks()

# ---------------- GUI PART ----------------

def start_gui():
    window = tk.Tk()
    window.title("Simple Task Manager")
    window.geometry("400x350")

    title = tk.Label(window, text="Task Manager", font=("Arial", 16))
    title.pack(pady=10)

    task_entry = tk.Entry(window, width=35)
    task_entry.pack(pady=5)
    task_entry.insert(0, "Task name")

    deadline_entry = tk.Entry(window, width=35)
    deadline_entry.pack(pady=5)
    deadline_entry.insert(0, "Deadline (YYYY-MM-DD)")

    def add_task_gui():
        task = task_entry.get()
        deadline = deadline_entry.get()

        if task and deadline:
            tasks.append((task, deadline))
            save_tasks()
            messagebox.showinfo("Success", "Task added!")
            task_entry.delete(0, tk.END)
            deadline_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Fill all fields!")

    def show_tasks_gui():
        if not tasks:
            messagebox.showinfo("Tasks", "No tasks yet.")
        else:
            text = ""
            for i, (task, deadline) in enumerate(tasks, 1):
                text += f"{i}. {task} (Deadline: {deadline})\n"
            messagebox.showinfo("Tasks", text)

    def search_tasks_gui():
        keyword = task_entry.get().lower()
        results = ""

        for i, (task, deadline) in enumerate(tasks, 1):
            if keyword in task.lower():
                results += f"{i}. {task} ({deadline})\n"

        if results:
            messagebox.showinfo("Search results", results)
        else:
            messagebox.showinfo("Search results", "No matching tasks found.")

    # ---------------- NOTIFICATIONS / REMINDERS ----------------
    def check_deadlines():
        today = datetime.now().strftime("%Y-%m-%d")

        for task, deadline in tasks:
            if deadline == today and (task, deadline) not in reminded_tasks:
                messagebox.showwarning(
                    "Reminder",
                    f"⚠️ Task due today:\n\n{task}"
                )
                reminded_tasks.add((task, deadline))

        # Check again after 60 seconds
        window.after(60000, check_deadlines)

    # Start reminder checker
    check_deadlines()

    tk.Button(window, text="Add Task", width=20, command=add_task_gui).pack(pady=5)
    tk.Button(window, text="Show Tasks", width=20, command=show_tasks_gui).pack(pady=5)
    tk.Button(window, text="Search Task", width=20, command=search_tasks_gui).pack(pady=5)
    tk.Button(window, text="Exit", width=20, command=window.destroy).pack(pady=10)

    window.mainloop()


# Start GUI only if this file is run directly
if __name__ == "__main__":
    start_gui()