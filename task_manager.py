from task import Task, HighPriorityTask, LowPriorityTask
from project import Project

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.projects = []

    def _levenshtein_distance(self, str1, str2):
        """Вычисляет расстояние Левенштейна между двумя строками."""
        len1, len2 = len(str1), len(str2)
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if str1[i - 1] == str2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + cost,
                )
        return dp[len1][len2]

    def _is_similar_task_name(self, task_name, existing_task_name):
        """Проверяет, похоже ли имя задачи на уже существующую задачу."""
        distance = self._levenshtein_distance(task_name.lower(), existing_task_name.lower())
        critical_distance = int(max(len(task_name), len(existing_task_name)) * 0.4)
        return distance <= critical_distance

    def _check_task_similarity(self, task_name):
        """Проверяет, есть ли схожие названия задач среди существующих."""
        for task in self.tasks:
            if self._is_similar_task_name(task_name, task.name):
                return task.name
        return None

    def add_task(self, task):
        """
        Добавляет задачу в менеджер задач.
        Перед добавлением проверяет схожесть с уже существующими задачами.
        """
        similar_task = self._check_task_similarity(task.name)
        if similar_task:
            return f"Задача '{task.name}' очень похожа на уже существующую задачу '{similar_task}'. Вы уверены, что хотите добавить её?", False
        else:
            self.tasks.append(task)
            return f"Задача '{task.name}' успешно добавлена.", True

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
