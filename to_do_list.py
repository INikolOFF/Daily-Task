# Този малък To-Do списък е направен с учебна цел.
# Целта на програмата е да упражни работата с функции, списъци,
# цикли, вход/изход от потребителя и работа с файлове.
# Подходящ е за начинаещи, които искат да свикнат със структурата
# на прост Python проект и логиката на основните операции.

tasks = []  # Списък със задачи

# Функция за зареждане на задачите от файл
def load_tasks():
    try:
        with open("tasks.txt", "r") as file:  # Отваряме файла за четене
            for line in file:
                tasks.append(line.strip())  # Добавяме всяка задача без нов ред
    except FileNotFoundError:
        pass  # Ако файлът не съществува – просто продължаваме

# Функция за записване на задачите във файла
def save_tasks():
    with open("tasks.txt", "w") as file:  # Отваряме файла за запис
        for task in tasks:
            file.write(task + "\n")  # Всяка задача на нов ред

# Показване на всички задачи
def show_tasks():
    if not tasks:
        print("No tasks yet.")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")

# Зареждаме задачите при стартиране
load_tasks()

while True:
    print("\n1. Show tasks\n2. Add task\n3. Remove task\n4. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        show_tasks()

    elif choice == "2":
        task = input("Enter a new task: ")
        tasks.append(task)
        save_tasks()  # Записваме след добавяне

    elif choice == "3":
        show_tasks()
        index = int(input("Enter the task number to remove: "))
        if 0 < index <= len(tasks):
            tasks.pop(index - 1)
            save_tasks()  # Записваме след триене

    elif choice == "4":
        save_tasks()  # Записваме последно преди изход
        break

    else:
        print("Invalid choice!")