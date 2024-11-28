class Project:
    MAX_NAME_LENGTH = 50
    MAX_DESCRIPTION_LENGTH = 200

    def __init__(self, name, description=""):
        if not name:
            raise ValueError("Имя проекта обязательно")
        if len(name) > self.MAX_NAME_LENGTH:
            raise ValueError(f"Имя проекта не может превышать {self.MAX_NAME_LENGTH} символов")
        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Описание проекта не может превышать {self.MAX_DESCRIPTION_LENGTH} символов")
        self.name = name
        self.description = description
        self.tasks = []


    def get_all_tasks(self):
        """Возвращает все задачи проекта"""
        return self.tasks

    def get_due_tasks(self):
        """Возвращает просроченные задачи"""
        return [task for task in self.tasks if task.is_due()]

    def __str__(self):
        return f"Проект: {self.name}, Задач: {len(self.tasks)}"

    def _get_task_summary(self):
        """Внутренний метод для анализа задач в проекте"""
        completed_tasks = len([task for task in self.tasks if task.status == "выполнена"])
        pending_tasks = len(self.tasks) - completed_tasks
        return f"Задач завершено: {completed_tasks}, в ожидании: {pending_tasks}"
