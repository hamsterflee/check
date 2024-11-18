import unittest
from freezegun import freeze_time
from task import Task, HighPriorityTask, LowPriorityTask

class TestTask(unittest.TestCase):
    def test_create_task(self):
        """Проверка создания задачи"""
        task = Task(name="Задача 1", description="Описание задачи", priority="высокий", deadline="2024-12-01")
        self.assertEqual(task.name, "Задача 1")
        self.assertEqual(task.description, "Описание задачи")
        self.assertEqual(task.priority, "высокий")
        self.assertEqual(task.deadline, "2024-12-01")
        self.assertEqual(task.status, "ожидает")

    def test_create_task_with_empty_values(self):
        """Проверка создания задачи с пустыми значениями"""
        with self.assertRaises(ValueError):
            Task(name="", description="Описание задачи", priority="высокий", deadline="2024-12-01")

        with self.assertRaises(ValueError):
            Task(name="Задача 1", description="", priority="высокий", deadline="2024-12-01")

        with self.assertRaises(ValueError):
            Task(name="Задача 1", description="Описание задачи", priority="", deadline="2024-12-01")

        with self.assertRaises(ValueError):
            Task(name="Задача 1", description="Описание задачи", priority="высокий", deadline="")

    def test_validate_deadline_valid(self):
        """Тест: корректный формат дедлайна не вызывает исключений"""
        try:
            Task(name="Задача", description="Описание", priority="высокий", deadline="2024-12-01")
        except ValueError as e:
            self.fail(f"Непредвиденное исключение: {e}")

    def test_validate_deadline_invalid_format(self):
        """Тест: некорректный формат дедлайна вызывает ValueError"""
        with self.assertRaises(ValueError):
            Task(name="Задача", description="Описание", priority="высокий", deadline="01-12-2024")

    def test_change_status(self):
        """Проверка изменения статуса задачи"""
        task = Task(name="Задача 1", description="Описание задачи", priority="высокий", deadline="2024-12-01")
        task.change_status("выполняется")
        self.assertEqual(task.status, "выполняется")

    @freeze_time("2024-11-02")
    def test_is_due(self):
        """Проверка просроченности задачи"""
        task = Task(name="Задача 1", description="Описание задачи", priority="высокий", deadline="2024-11-01")
        self.assertTrue(task.is_due())
        task.change_status("выполнена")
        self.assertFalse(task.is_due())

    @freeze_time("2024-11-02")
    def test_is_due_not_due(self):
        """Проверка, что задача не просрочена"""
        task = Task(name="Задача 1", description="Описание задачи", priority="высокий", deadline="2024-12-01")
        self.assertFalse(task.is_due())  # Текущая дата перед 2024-12-01

    @freeze_time("2024-11-02")
    def test_high_priority_task_is_due(self):
        """Проверка просроченности задачи с высоким приоритетом"""
        task = HighPriorityTask(name="Задача 1", description="Описание задачи", deadline="2024-11-01")
        result = task.is_due()
        self.assertEqual(result, "Внимание: Задача с высоким приоритетом просрочена! Задача 1")

    @freeze_time("2024-11-02")
    def test_low_priority_task_is_due(self):
        """Проверка просроченности задачи с низким приоритетом"""
        task = LowPriorityTask(name="Задача 1", description="Описание задачи", deadline="2024-11-01")
        result = task.is_due()
        self.assertEqual(result, "Задача с низким приоритетом Задача 1 просрочена, но её можно выполнить позже.")

    def test_allocate_resources_high_priority(self):
        """Проверка выделения ресурсов для задачи с высоким приоритетом"""
        task = HighPriorityTask(name="Задача 1", description="Описание задачи", deadline="2024-12-01", status="выполняется")
        result = task.allocate_resources()
        self.assertEqual(result, "Ресурсы выделены для задачи: Задача 1")

    def test_allocate_resources_low_priority(self):
        """Проверка выделения ресурсов для задачи с низким приоритетом"""
        task = LowPriorityTask(name="Задача 1", description="Описание задачи", deadline="2024-12-01", status="выполняется")
        result = task.allocate_resources()
        self.assertEqual(result, "Ресурсы выделены для задачи: Задача 1")

    def test_allocate_resources_high_priority_waiting(self):
        """Проверка выделения ресурсов для ожидающей задачи с высоким приоритетом"""
        task = HighPriorityTask(name="Задача 1", description="Описание задачи", deadline="2024-12-01", status="ожидает")
        result = task.allocate_resources()
        self.assertEqual(result, "Задача с высоким приоритетом Задача 1 ожидает начала выполнения.")

    def test_allocate_resources_low_priority_waiting(self):
        """Проверка выделения ресурсов для ожидающей задачи с низким приоритетом"""
        task = LowPriorityTask(name="Задача 1", description="Описание задачи", deadline="2024-12-01", status="ожидает")
        result = task.allocate_resources()
        self.assertEqual(result, "Задача с низким приоритетом Задача 1 может быть выполнена позже.")

if __name__ == '__main__':
    unittest.main()
