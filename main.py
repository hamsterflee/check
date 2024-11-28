import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from task_manager import TaskManager
from task import Task, HighPriorityTask, LowPriorityTask

manager = TaskManager()

def update_task_list():
    tasks_listbox.delete(0, tk.END)
    for task in manager.tasks:
        tasks_listbox.insert(tk.END, f"{task.name} - {task.status.capitalize()}")

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

        # Проверка на схожесть названий
        similar_task_message, task_added = manager.add_task(task)  # Получаем сообщение от метода add_task
        if not task_added:
            # Запрос подтверждения у пользователя
            confirm = messagebox.askyesno(
                "Предупреждение",
                similar_task_message  # Показываем сообщение с предупреждением
            )
            if confirm:
                # Если пользователь подтверждает добавление
                manager.tasks.append(task)  # Добавляем задачу вручную
                messagebox.showinfo("Успех", f"Задача '{task.name}' успешно добавлена!")
                update_task_list()  # Обновляем список задач
            else:
                print("Задача не добавлена, пользователь отклонил добавление.")
        else:
            messagebox.showinfo("Успех", f"Задача '{task.name}' успешно добавлена!")
            update_task_list()  # Обновляем список задач

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

def update_project_list():
    project_combobox.set('')  # Очищаем выбор проекта
    project_combobox['values'] = [project.name for project in manager.projects]  # Обновляем список проектов

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
        selected_project = project_combobox.get()
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
priority_var = tk.StringVar(value="Средний")
priority_menu = ttk.Combobox(task_input_frame, textvariable=priority_var, values=["Высокий", "Средний", "Низкий"])
priority_menu.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(task_input_frame, text="Срок (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
deadline_entry = ttk.Entry(task_input_frame, width=30)
deadline_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = ttk.Button(task_input_frame, text="Добавить задачу", command=add_task)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Список задач
tasks_listbox = tk.Listbox(task_tab, width=50, height=10)
tasks_listbox.pack(padx=10, pady=10)

# Кнопки для управления задачами
remove_button = ttk.Button(task_tab, text="Удалить задачу", command=remove_task)
remove_button.pack(padx=10, pady=5)

find_button = ttk.Button(task_tab, text="Найти задачу", command=find_task_by_name)
find_button.pack(padx=10, pady=5)

due_button = ttk.Button(task_tab, text="Просроченные задачи", command=show_due_tasks)
due_button.pack(padx=10, pady=5)

pending_button = ttk.Button(task_tab, text="Задачи в ожидании", command=show_pending_tasks)
pending_button.pack(padx=10, pady=5)

status_label = ttk.Label(task_tab, text="Новый статус:")
status_label.pack(padx=10, pady=5)

status_var = tk.StringVar(value="выполняется")
status_menu = ttk.Combobox(task_tab, textvariable=status_var, values=["выполняется", "завершена", "отложена"])
status_menu.pack(padx=10, pady=5)

change_status_button = ttk.Button(task_tab, text="Изменить статус", command=change_status)
change_status_button.pack(padx=10, pady=5)

allocate_button = ttk.Button(task_tab, text="Распределить ресурсы", command=allocate_resources)
allocate_button.pack(padx=10, pady=5)

# Вкладка для проектов
project_tab = ttk.Frame(notebook)
notebook.add(project_tab, text='Проекты')

# Фрейм для выбора проекта
project_input_frame = ttk.Frame(project_tab)
project_input_frame.pack(padx=10, pady=10)

create_project_button = ttk.Button(project_input_frame, text="Создать проект", command=create_project)
create_project_button.pack(padx=10, pady=10)

project_combobox = ttk.Combobox(project_input_frame, width=30)
project_combobox.pack(padx=10, pady=5)

# Кнопки для управления проектами
add_task_to_project_button = ttk.Button(project_tab, text="Добавить задачу в проект", command=add_task_to_project)
add_task_to_project_button.pack(padx=10, pady=5)

show_project_button = ttk.Button(project_tab, text="Показать задачи проекта", command=show_all_project_tasks)
show_project_button.pack(padx=10, pady=5)

show_due_button = ttk.Button(project_tab, text="Показать просроченные задачи проекта", command=show_due_project_tasks)
show_due_button.pack(padx=10, pady=5)

project_summary_button = ttk.Button(project_tab, text="Статистика проекта", command=show_project_summary)
project_summary_button.pack(padx=10, pady=5)

root.mainloop()
