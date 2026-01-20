import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from datetime import datetime, timedelta
import json
import os

TASK_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.reminded_tasks = set()
        self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(TASK_FILE):
            self.save_tasks()
            return
        try:
            with open(TASK_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
                self.reminded_tasks = set(tuple(x) for x in data.get("reminded", []))
        except:
            self.tasks = []
            self.reminded_tasks = set()

    def save_tasks(self):
        with open(TASK_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "tasks": self.tasks,
                    "reminded": list(self.reminded_tasks),
                },
                f,
                indent=2,
            )

    def add_task(self, task):
        if any(t["name"] == task["name"] and t["deadline"] == task["deadline"] for t in self.tasks):
            return False
        self.tasks.append(task)
        self.save_tasks()
        return True

    def update_task(self, index, task):
        if 0 <= index < len(self.tasks):
            self.tasks[index] = task
            self.save_tasks()
            return True
        return False

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            task = self.tasks.pop(index)
            self.save_tasks()
            return task
        return None

    def search_tasks(self, keyword):
        return [
            (i, t)
            for i, t in enumerate(self.tasks)
            if keyword.lower() in t["name"].lower()
            or keyword.lower() in t["notes"].lower()
        ]

    def sorted_tasks(self, mode):
        if mode == "priority":
            order = {"High": 0, "Medium": 1, "Low": 2}
            return sorted(enumerate(self.tasks), key=lambda x: order.get(x[1]["priority"], 3))
        return sorted(enumerate(self.tasks), key=lambda x: x[1]["deadline"])


class TaskManagerGUI:
    def __init__(self):
        self.manager = TaskManager()
        self.selected_index = None

        self.root = tk.Tk()
        self.root.title("Enhanced Task Manager")
        self.root.geometry("750x680")

        self.setup_ui()
        self.refresh_tasks()
        self.check_deadlines()

        self.root.bind("<Return>", lambda e: self.add_task())
        self.root.bind("<Delete>", lambda e: self.delete_task())

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#2c3e50")
        header.pack(fill="x")
        tk.Label(
            header,
            text="📋 TASK MANAGER",
            font=("Arial", 22, "bold"),
            bg="#2c3e50",
            fg="white",
        ).pack(pady=15)

        form = tk.LabelFrame(self.root, text="Task Details", padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Task Name").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(form, width=50)
        self.name_entry.grid(row=0, column=1, columnspan=3, padx=5)

        tk.Label(form, text="Deadline (YYYY-MM-DD)").grid(row=1, column=0, sticky="w")
        self.deadline_entry = tk.Entry(form, width=20)
        self.deadline_entry.grid(row=1, column=1, sticky="w")
        self.deadline_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(form, text="Priority").grid(row=1, column=2, sticky="e")
        self.priority_var = tk.StringVar(value="Medium")
        ttk.Combobox(
            form,
            textvariable=self.priority_var,
            values=["High", "Medium", "Low"],
            state="readonly",
            width=10,
        ).grid(row=1, column=3, padx=5)

        tk.Label(form, text="Notes").grid(row=2, column=0, sticky="nw")
        self.notes_text = tk.Text(form, height=3, width=50)
        self.notes_text.grid(row=2, column=1, columnspan=3, padx=5)

        btns = tk.Frame(self.root)
        btns.pack(pady=5)

        tk.Button(btns, text="➕ Add", width=12, command=self.add_task).grid(row=0, column=0, padx=4)
        tk.Button(btns, text="✏️ Update", width=12, command=self.update_task).grid(row=0, column=1, padx=4)
        tk.Button(btns, text="🗑️ Delete", width=12, command=self.delete_task).grid(row=0, column=2, padx=4)
        tk.Button(btns, text="🔍 Search", width=12, command=self.search_task).grid(row=0, column=3, padx=4)
        tk.Button(btns, text="🔄 Clear", width=12, command=self.clear_fields).grid(row=0, column=4, padx=4)

        sort_frame = tk.Frame(self.root)
        sort_frame.pack(pady=5)
        self.sort_var = tk.StringVar(value="deadline")
        ttk.Radiobutton(sort_frame, text="Sort by Deadline", variable=self.sort_var,
                        value="deadline", command=self.refresh_tasks).pack(side="left", padx=5)
        ttk.Radiobutton(sort_frame, text="Sort by Priority", variable=self.sort_var,
                        value="priority", command=self.refresh_tasks).pack(side="left", padx=5)

        list_frame = tk.LabelFrame(self.root, text="Tasks")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.task_list = scrolledtext.ScrolledText(list_frame, font=("Consolas", 10))
        self.task_list.pack(fill="both", expand=True)
        self.task_list.bind("<Double-Button-1>", self.select_task)

        self.status = tk.Label(self.root, text="", anchor="w")
        self.status.pack(fill="x", padx=10, pady=5)

    def refresh_tasks(self):
        self.task_list.delete("1.0", tk.END)
        today = datetime.now().date()

        for i, (idx, task) in enumerate(self.manager.sorted_tasks(self.sort_var.get()), 1):
            deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
            days = (deadline - today).days

            if days < 0:
                status = "❌ OVERDUE"
            elif days == 0:
                status = "⚠️ TODAY"
            elif days <= 3:
                status = "⏰ SOON"
            else:
                status = "📅 OK"

            icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[task["priority"]]

            self.task_list.insert(
                tk.END,
                f"{i}. {icon} {task['name']}\n"
                f"   Deadline: {task['deadline']} | {status}\n"
                f"   Notes: {task['notes']}\n\n",
            )

        overdue = sum(
            datetime.strptime(t["deadline"], "%Y-%m-%d").date() < today
            for t in self.manager.tasks
        )

        self.status.config(text=f"Total: {len(self.manager.tasks)} | Overdue: {overdue}")

    def add_task(self):
        name = self.name_entry.get().strip()
        deadline = self.deadline_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()
        priority = self.priority_var.get()

        if not name:
            messagebox.showerror("Error", "Task name required")
            return

        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format")
            return

        task = {
            "name": name,
            "deadline": deadline,
            "priority": priority,
            "notes": notes,
            "created": datetime.now().isoformat(),
        }

        if not self.manager.add_task(task):
            messagebox.showwarning("Duplicate", "Task already exists")
            return

        self.clear_fields()
        self.refresh_tasks()

    def select_task(self, event):
        try:
            line = self.task_list.get("insert linestart", "insert lineend")
            num = int(line.split(".")[0]) - 1
            sorted_tasks = self.manager.sorted_tasks(self.sort_var.get())
            self.selected_index = sorted_tasks[num][0]
            task = sorted_tasks[num][1]

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, task["name"])
            self.deadline_entry.delete(0, tk.END)
            self.deadline_entry.insert(0, task["deadline"])
            self.priority_var.set(task["priority"])
            self.notes_text.delete("1.0", tk.END)
            self.notes_text.insert("1.0", task["notes"])
        except:
            pass

    def update_task(self):
        if self.selected_index is None:
            return

        task = {
            "name": self.name_entry.get(),
            "deadline": self.deadline_entry.get(),
            "priority": self.priority_var.get(),
            "notes": self.notes_text.get("1.0", tk.END).strip(),
            "created": datetime.now().isoformat(),
        }

        self.manager.update_task(self.selected_index, task)
        self.clear_fields()
        self.refresh_tasks()

    def delete_task(self):
        if self.selected_index is None:
            return
        if not messagebox.askyesno("Confirm", "Delete this task?"):
            return
        self.manager.delete_task(self.selected_index)
        self.clear_fields()
        self.refresh_tasks()

    def search_task(self):
        keyword = self.name_entry.get().strip()
        results = self.manager.search_tasks(keyword)
        if not results:
            messagebox.showinfo("Search", "No results")
            return

        text = ""
        for i, (_, t) in enumerate(results, 1):
            text += f"{i}. {t['name']} ({t['deadline']})\n"
        messagebox.showinfo("Results", text)

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.deadline_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.notes_text.delete("1.0", tk.END)
        self.priority_var.set("Medium")
        self.selected_index = None

    def check_deadlines(self):
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        for t in self.manager.tasks:
            key = (t["name"], t["deadline"])
            if t["deadline"] in (today, tomorrow) and key not in self.manager.reminded_tasks:
                messagebox.showinfo("Reminder", f"{t['name']} due on {t['deadline']}")
                self.manager.reminded_tasks.add(key)
                self.manager.save_tasks()

        self.root.after(300000, self.check_deadlines)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    TaskManagerGUI().run()