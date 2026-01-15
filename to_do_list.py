import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import os

tasks = []  # List of tasks as (task_name, deadline)
reminded_tasks = set()
TASK_FILE = "tasks.txt"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            for line in file:
                if ";" in line:
                    name, deadline = line.strip().split(";", 1)
                    tasks.append((name, deadline))

def save_tasks():
    with open(TASK_FILE, "w") as file:
        for task, deadline in tasks:
            file.write(f"{task};{deadline}\n")

load_tasks()

def start_gui():
    window = tk.Tk()
    window.title("Enhanced Task Manager")
    window.geometry("500x500")
    window.resizable(False, False)

    tk.Label(window, text="Task Manager", font=("Arial", 18, "bold")).pack(pady=10)

    task_entry = tk.Entry(window, width=35, font=("Arial", 12))
    task_entry.pack(pady=5)
    task_entry.insert(0, "Task name")

    deadline_entry = tk.Entry(window, width=35, font=("Arial", 12))
    deadline_entry.pack(pady=5)
    deadline_entry.insert(0, "Deadline (YYYY-MM-DD)")

    task_list_frame = tk.Frame(window)
    task_list_frame.pack(pady=10, fill="both", expand=True)

    task_list = scrolledtext.ScrolledText(task_list_frame, width=60, height=15, font=("Consolas", 11))
    task_list.pack()

    def refresh_task_list():
        task_list.delete("1.0", tk.END)
        today = datetime.now().strftime("%Y-%m-%d")
        for i, (task, deadline) in enumerate(tasks, 1):
            if deadline == today:
                task_list.insert(tk.END, f"{i}. ⚠️ {task} (Deadline: {deadline})\n")
            else:
                task_list.insert(tk.END, f"{i}. {task} (Deadline: {deadline})\n")

    def add_task():
        task = task_entry.get().strip()
        deadline = deadline_entry.get().strip()
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
            return

        if not task or not deadline:
            messagebox.showerror("Error", "Fill all fields!")
            return

        tasks.append((task, deadline))
        save_tasks()
        task_entry.delete(0, tk.END)
        deadline_entry.delete(0, tk.END)
        refresh_task_list()

    def delete_task():
        index_str = task_entry.get().strip()
        if not index_str.isdigit():
            messagebox.showerror("Error", "Enter task number to delete in Task Name field")
            return
        index = int(index_str) - 1
        if 0 <= index < len(tasks):
            task_name, _ = tasks.pop(index)
            save_tasks()
            messagebox.showinfo("Deleted", f"Task '{task_name}' deleted")
            refresh_task_list()
        else:
            messagebox.showerror("Error", "Invalid task number")

    def search_task():
        keyword = task_entry.get().strip().lower()
        if not keyword:
            messagebox.showerror("Error", "Enter keyword in Task Name field")
            return
        results = ""
        for i, (task, deadline) in enumerate(tasks, 1):
            if keyword in task.lower():
                results += f"{i}. {task} (Deadline: {deadline})\n"
        if results:
            messagebox.showinfo("Search results", results)
        else:
            messagebox.showinfo("Search results", "No matching tasks found")

    def check_deadlines():
        today = datetime.now().strftime("%Y-%m-%d")
        for task, deadline in tasks:
            if deadline == today and (task, deadline) not in reminded_tasks:
                messagebox.showwarning("Reminder", f"⚠️ Task due today:\n\n{task}")
                reminded_tasks.add((task, deadline))
        window.after(60000, check_deadlines)

    tk.Button(window, text="Add Task", width=20, command=add_task, bg="#27ae60", fg="white").pack(pady=3)
    tk.Button(window, text="Delete Task", width=20, command=delete_task, bg="#e74c3c", fg="white").pack(pady=3)
    tk.Button(window, text="Search Task", width=20, command=search_task, bg="#3498db", fg="white").pack(pady=3)
    tk.Button(window, text="Exit", width=20, command=window.destroy, bg="#95a5a6", fg="white").pack(pady=10)

    refresh_task_list()
    check_deadlines()
    window.mainloop()

if __name__ == "__main__":
    start_gui()