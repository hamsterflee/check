import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from src.task_manager import TaskManager
from src.task import Task, HighPriorityTask, LowPriorityTask

manager = TaskManager()

def add_task():
    name = name_entry.get()
    description = description_entry.get()
    priority = priority_var.get()
    deadline = deadline_entry.get()

    if not name or not description or not priority or not deadline:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
        return

    try:
        if priority == "Высокий":
            task = HighPriorityTask(name, description, deadline)
        elif priority == "Низкий":
            task = LowPriorityTask(name, description, deadline)
        else:
            task = Task(name, description, priority, deadline)

        manager.add_task(task)
        messagebox.showinfo("Успех", f"Задача '{task.name}' добавлена!")
        update_task_list()

    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def remove_task():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        task = manager.tasks[selected_task_index]
        manager.remove_task(task)
        messagebox.showinfo("Успех", f"Задача '{task.name}' удалена!")
        update_task_list()
    except IndexError:
        messagebox.showerror("Ошибка", "Не выбрана задача.")

def find_task_by_name():
    name = simpledialog.askstring("Поиск задачи", "Введите название задачи:")
    if name:
        tasks = manager.find_task_by_name(name)
        tasks_listbox.delete(0, tk.END)
        for task in tasks:
            tasks_listbox.insert(tk.END, f"{task.name} - {task.status.capitalize()}")
        if not tasks:
            messagebox.showinfo("Результаты поиска", "Задача не найдена.")

def change_status():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        task = manager.tasks[selected_task_index]
        new_status = status_var.get()
        manager.change_task_status(task, new_status)
        messagebox.showinfo("Успех", f"Статус задачи '{task.name}' изменен на {new_status}!")
        update_task_list()
    except IndexError:
        messagebox.showerror("Ошибка", "Не выбрана задача.")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def allocate_resources():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        task = manager.tasks[selected_task_index]
        result = manager.allocate_resources(task)
        messagebox.showinfo("Ресурсы", result)
    except IndexError:
        messagebox.showerror("Ошибка", "Не выбрана задача.")

def update_task_list():
    tasks_listbox.delete(0, tk.END)
    tasks = manager.display_all_tasks()
    for task in tasks:
        tasks_listbox.insert(tk.END, f"{task.name} - {task.status.capitalize()}")

def show_due_tasks():
    tasks_listbox.delete(0, tk.END)
    due_tasks = manager.find_due_tasks()
    for task in due_tasks:
        tasks_listbox.insert(tk.END, f"{task.name} - {task.status.capitalize()}")

def show_pending_tasks():
    tasks_listbox.delete(0, tk.END)
    pending_tasks = manager.find_pending_tasks()
    for task in pending_tasks:
        tasks_listbox.insert(tk.END, f"{task.name} - {task.status.capitalize()}")

def create_project():
    project_name = simpledialog.askstring("Создание проекта", "Введите название проекта:")
    if project_name:
        project = manager.create_project(project_name)
        messagebox.showinfo("Успех", f"Проект '{project.name}' создан!")
        update_project_list()

def add_task_to_project():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        task = manager.tasks[selected_task_index]
        selected_project = project_combobox.get()  # Выбираем проект из комбобокса
        project = manager.get_project(selected_project)
        if project:
            manager.add_task_to_project(task, project)
            messagebox.showinfo("Успех", f"Задача '{task.name}' добавлена в проект '{project.name}'!")
        else:
            messagebox.showerror("Ошибка", "Проект не найден.")
    except IndexError:
        messagebox.showerror("Ошибка", "Не выбрана задача.")

def show_project_summary():
    selected_project = project_combobox.get()  # Выбираем проект из комбобокса
    project = manager.get_project(selected_project)
    if project:
        summary = project._get_task_summary()
        messagebox.showinfo(f"Статистика проекта '{selected_project}'", summary)
    else:
        messagebox.showerror("Ошибка", "Проект не найден.")

def show_all_project_tasks():
    selected_project = project_combobox.get()  # Выбираем проект из комбобокса
    project = manager.get_project(selected_project)
    if project:
        tasks = project.get_all_tasks()
        task_list = "\n".join(str(task) for task in tasks)
        messagebox.showinfo(f"Задачи проекта '{selected_project}'", task_list)
    else:
        messagebox.showerror("Ошибка", "Проект не найден.")

def show_due_project_tasks():
    selected_project = project_combobox.get()  # Выбираем проект из комбобокса
    project = manager.get_project(selected_project)
    if project:
        due_tasks = project.get_due_tasks()
        task_list = "\n".join(str(task) for task in due_tasks)
        messagebox.showinfo(f"Просроченные задачи проекта '{selected_project}'", task_list)
    else:
        messagebox.showerror("Ошибка", "Проект не найден.")

def sort_tasks_by_deadline():
    sorted_tasks = manager.sort_tasks_by_deadline()
    tasks_listbox.delete(0, tk.END)
    for task in sorted_tasks:
        tasks_listbox.insert(tk.END, f"{task.name} - {task.status.capitalize()}")

def sort_tasks_by_priority():
    sorted_tasks = manager.sort_tasks_by_priority()
    tasks_listbox.delete(0, tk.END)
    for task in sorted_tasks:
        tasks_listbox.insert(tk.END, f"{task.name} - {task.status.capitalize()}")

def update_project_list():
    project_combobox.set('')  # Очищаем выбор проекта
    project_combobox['values'] = [project.name for project in manager.projects]  # Обновляем список проектов

# Создание окна приложения
root = tk.Tk()
root.title("Менеджер задач")
root.geometry("600x600")

# Создание Notebook для разделения функционала
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Вкладка для задач
task_tab = ttk.Frame(notebook)
notebook.add(task_tab, text='Задачи')

# Фрейм для ввода данных о задаче
task_input_frame = ttk.Frame(task_tab)
task_input_frame.pack(padx=10, pady=10)

ttk.Label(task_input_frame, text="Название задачи:").grid(row=0, column=0, padx=5, pady=5)
name_entry = ttk.Entry(task_input_frame, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(task_input_frame, text="Описание задачи:").grid(row=1, column=0, padx=5, pady=5)
description_entry = ttk.Entry(task_input_frame, width=30)
description_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(task_input_frame, text="Приоритет:").grid(row=2, column=0, padx=5, pady=5)
priority_var = tk.StringVar()
priority_combobox = ttk.Combobox(task_input_frame, textvariable=priority_var, values=["Высокий", "Низкий", "Обычный"])
priority_combobox.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(task_input_frame, text="Срок выполнения (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
deadline_entry = ttk.Entry(task_input_frame, width=30)
deadline_entry.grid(row=3, column=1, padx=5, pady=5)

add_task_button = ttk.Button(task_input_frame, text="Добавить задачу", command=add_task)
add_task_button.grid(row=4, column=1, padx=5, pady=5)

# Список задач
tasks_listbox = tk.Listbox(task_tab, width=50, height=10)
tasks_listbox.pack(padx=10, pady=10)

# Кнопки для сортировки
sort_by_deadline_button = ttk.Button(task_tab, text="Сортировать по сроку", command=sort_tasks_by_deadline)
sort_by_deadline_button.pack(padx=10, pady=5)

sort_by_priority_button = ttk.Button(task_tab, text="Сортировать по приоритету", command=sort_tasks_by_priority)
sort_by_priority_button.pack(padx=10, pady=5)

# Запуск главного цикла
root.mainloop()
