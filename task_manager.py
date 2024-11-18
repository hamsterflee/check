from datetime import datetime
from src.task import Task, HighPriorityTask, LowPriorityTask
from src.project import Project

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.projects = []

    def add_task(self, task: Task):
        """Добавление новой задачи в список."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Удаление задачи из списка."""
        if task in self.tasks:
            self.tasks.remove(task)

    def find_task_by_name(self, name: str):
        """Поиск задачи по названию."""
        return [task for task in self.tasks if task.name.lower() == name.lower()]

    def find_due_tasks(self):
        """Поиск просроченных задач."""
        return [task for task in self.tasks if task.is_due()]

    def find_pending_tasks(self):
        """Поиск задач с ожиданием начала выполнения."""
        return [task for task in self.tasks if task.status == "ожидает"]

    def sort_tasks_by_deadline(self):
        """Сортировка задач по приоритету и сроку выполнения (по возрастанию)."""
        return sorted(self.tasks, key=lambda task: (isinstance(task, HighPriorityTask),
                                                    datetime.strptime(task.deadline, "%Y-%m-%d")))

    def sort_tasks_by_priority(self):
        """Сортировка задач по приоритету (высокий, низкий, без приоритета)."""
        high_priority_tasks = [task for task in self.tasks if isinstance(task, HighPriorityTask)]
        low_priority_tasks = [task for task in self.tasks if isinstance(task, LowPriorityTask)]
        regular_tasks = [task for task in self.tasks if not isinstance(task, (HighPriorityTask, LowPriorityTask))]

        return high_priority_tasks + low_priority_tasks + regular_tasks

    def change_task_status(self, task: Task, status: str):
        """Изменение статуса задачи."""
        if task in self.tasks:
            task.change_status(status)

    def allocate_resources(self, task: Task):
        """Выделение ресурсов для задачи, в зависимости от её статуса и приоритета."""
        if task in self.tasks:
            return task.allocate_resources()

    def display_all_tasks(self):
        """Возвращает список всех задач."""
        return self.tasks

    def create_project(self, name):
        project = Project(name)
        self.projects.append(project)
        return project

    def display_all_projects(self):
        return self.projects

    def add_task_to_project(self, task: Task, project: Project):
        """Добавление задачи в проект."""
        if not isinstance(task, Task):
            raise TypeError("Можно добавить только задачи")
        if not isinstance(project, Project):
            raise TypeError("Можно добавить задачу только в проект")
        project.tasks.append(task)

    def remove_task_from_project(self, task: Task, project: Project):
        """Удаление задачи из проекта."""
        if task in project.tasks:
            project.tasks.remove(task)

    def get_project(self, project_name):
        """Получить проект по имени."""
        for project in self.projects:
            if project.name == project_name:
                return project
        return None
