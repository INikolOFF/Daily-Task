tasks = []


def show_tasks():
    if not tasks:
        print("No tasks yet.")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")


while True:
    print("\n1. Show tasks\n2. Add task\n3. Remove task\n4. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        show_tasks()
    elif choice == "2":
        task = input("Enter a new task: ")
        tasks.append(task)
    elif choice == "3":
        show_tasks()
        index = int(input("Enter the task number to remove: "))
        if 0 < index <= len(tasks):
            tasks.pop(index - 1)
    elif choice == "4":
        break
    else:
        print("Invalid choice!")