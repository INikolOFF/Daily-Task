tasks = []  # List of tasks, each as a tuple (task_name, deadline)

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

# Function to display all tasks with deadlines
def show_tasks():
    if not tasks:
        print("No tasks yet.")
    for i, (task, deadline) in enumerate(tasks, 1):
        print(f"{i}. {task} (Deadline: {deadline})")

# NEW FUNCTION: search tasks by keyword
def search_tasks():
    keyword = input("Enter keyword to search: ").lower()
    found = False

    for i, (task, deadline) in enumerate(tasks, 1):
        if keyword in task.lower():
            print(f"{i}. {task} (Deadline: {deadline})")
            found = True

    if not found:
        print("No matching tasks found.")

# Load tasks when program starts
load_tasks()

while True:
    print("\n1. Show tasks\n2. Add task\n3. Remove task\n4. Search task\n5. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        show_tasks()

    elif choice == "2":
        task = input("Enter a new task: ")
        deadline = input("Enter deadline (e.g., YYYY-MM-DD): ")
        tasks.append((task, deadline))  # Add task with deadline
        save_tasks()  # Save after adding

    elif choice == "3":
        show_tasks()
        index = int(input("Enter the task number to remove: "))
        if 0 < index <= len(tasks):
            tasks.pop(index - 1)  # Remove the selected task
            save_tasks()  # Save after removal

    elif choice == "4":
        search_tasks()

    elif choice == "5":
        save_tasks()  # Save before exiting
        break

    else:
        print("Invalid choice!")