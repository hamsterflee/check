from datetime import datetime

class Task:
    def __init__(self, name, description, priority, deadline, status="ожидает"):
        if not name or not description or not priority or not deadline:
            raise ValueError("Все поля (название, описание, приоритет, срок) должны быть заполнены.")
        self._validate_deadline(deadline)
        self.name = name
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.status = status

    def _validate_deadline(self, deadline):
        """Проверка корректности формата срока"""
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Срок должен быть в формате YYYY-MM-DD.")

    def change_status(self, new_status):
        """Изменить статус задачи."""
        self.status = new_status

    def set_deadline(self, new_deadline):
        """Изменить срок задачи."""
        self.deadline = new_deadline

    def is_due(self):
        """Проверка, просрочена ли задача."""
        today = datetime.today().date()
        deadline_date = datetime.strptime(self.deadline, "%Y-%m-%d").date()
        return today > deadline_date and self.status != "выполнена"

    def __str__(self):
        """Строковое представление задачи."""
        return f"{self.name} - {self.status.capitalize()}"


class HighPriorityTask(Task):
    def __init__(self, name, description, deadline, status="ожидает"):
        super().__init__(name, description, priority="высокий", deadline=deadline, status=status)

    def is_due(self):
        """Проверка просроченной задачи с высоким приоритетом"""
        is_due = super().is_due()
        if is_due:
            return f"Внимание: Задача с высоким приоритетом просрочена! {self.name}"
        return None

    def allocate_resources(self):
        """Выделить больше ресурсов для задачи с высоким приоритетом"""
        if self.status == "выполняется":
            return f"Ресурсы выделены для задачи: {self.name}"
        else:
            return f"Задача с высоким приоритетом {self.name} ожидает начала выполнения."


class LowPriorityTask(Task):
    def __init__(self, name, description, deadline, status="ожидает"):
        super().__init__(name, description, priority="низкий", deadline=deadline, status=status)

    def is_due(self):
        """Проверка просроченной задачи с низким приоритетом"""
        is_due = super().is_due()
        if is_due:
            return f"Задача с низким приоритетом {self.name} просрочена, но её можно выполнить позже."
        return None

    def allocate_resources(self):
        """Ресурсы выделяются по мере наличия для задачи с низким приоритетом"""
        if self.status == "выполняется":
            return f"Ресурсы выделены для задачи: {self.name}"
        else:
            return f"Задача с низким приоритетом {self.name} может быть выполнена позже."
