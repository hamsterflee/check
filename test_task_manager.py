import unittest
from datetime import datetime
from task import Task, HighPriorityTask, LowPriorityTask
from task_manager import TaskManager
from datetime import timedelta

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        """Создание экземпляров для тестов"""
        self.task_manager = TaskManager()
        self.task1 = Task(name="Задача 1", description="Описание задачи", priority="высокий", deadline="2024-12-01")
        self.task2 = Task(name="Задача 2", description="Описание задачи", priority="низкий", deadline="2024-12-02")
        self.task_manager.add_task(self.task1)
        self.task_manager.add_task(self.task2)

        self.project = self.task_manager.create_project(name="Проект 1")

    def test_add_task(self):
        """Тестирование добавления задачи"""
        task3 = Task(name="Задача 3", description="Описание задачи", priority="высокий", deadline="2024-12-03")
        self.task_manager.add_task(task3)
        self.assertIn(task3, self.task_manager.tasks)

    def test_remove_task(self):
        """Тестирование удаления задачи"""
        self.task_manager.remove_task(self.task1)
        self.assertNotIn(self.task1, self.task_manager.tasks)

    def test_find_task_by_name(self):
        """Тестирование поиска задачи по имени"""
        found_tasks = self.task_manager.find_task_by_name("Задача 1")
        self.assertEqual(len(found_tasks), 1)
        self.assertEqual(found_tasks[0], self.task1)

    def test_find_due_tasks(self):
        """Тестирование поиска просроченных задач"""
        self.task1.deadline = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        overdue_tasks = self.task_manager.find_due_tasks()
        self.assertIn(self.task1, overdue_tasks)

    def test_find_pending_tasks(self):
        """Тестирование поиска задач в ожидании"""
        self.task1.change_status("ожидает")
        pending_tasks = self.task_manager.find_pending_tasks()
        self.assertIn(self.task1, pending_tasks)

    def test_sort_tasks_by_deadline(self):
        """Тестирование сортировки задач по сроку выполнения"""
        sorted_tasks = self.task_manager.sort_tasks_by_deadline()
        self.assertEqual(sorted_tasks[0], self.task1)
        self.assertEqual(sorted_tasks[1], self.task2)

    def test_sort_tasks_by_priority(self):
        """Тестирование сортировки задач по приоритету"""
        self.task1 = HighPriorityTask(name="Задача 1", description="Описание задачи", deadline="2024-12-01")
        self.task2 = LowPriorityTask(name="Задача 2", description="Описание задачи", deadline="2024-12-02")
        self.task3 = Task(name="Задача 3", description="Обычная задача", priority="средний", deadline="2024-12-05")

        self.task_manager.add_task(self.task1)
        self.task_manager.add_task(self.task2)
        self.task_manager.add_task(self.task3)

        sorted_tasks = self.task_manager.sort_tasks_by_priority()

        self.assertIsInstance(sorted_tasks[0], HighPriorityTask)
        self.assertIsInstance(sorted_tasks[1], LowPriorityTask)
        self.assertIsInstance(sorted_tasks[2], Task)

    def test_change_task_status(self):
        """Тестирование изменения статуса задачи"""
        self.task_manager.change_task_status(self.task1, "выполняется")
        self.assertEqual(self.task1.status, "выполняется")

    def test_allocate_resources(self):
        """Тестирование выделения ресурсов для задачи"""
        if isinstance(self.task1, (HighPriorityTask, LowPriorityTask)):
            result = self.task_manager.allocate_resources(self.task1)
            self.assertTrue(result.startswith("Ресурсы выделены"))
        else:
            with self.assertRaises(AttributeError):
                self.task_manager.allocate_resources(self.task1)

    def test_create_project(self):
        """Тестирование создания проекта"""
        project = self.task_manager.create_project(name="Новый проект")
        self.assertIn(project, self.task_manager.projects)
        self.assertEqual(project.name, "Новый проект")

    def test_add_task_to_project(self):
        """Тестирование добавления задачи в проект"""
        self.task_manager.add_task_to_project(self.task1, self.project)
        self.assertIn(self.task1, self.project.tasks)

    def test_remove_task_from_project(self):
        """Тестирование удаления задачи из проекта"""
        self.task_manager.add_task_to_project(self.task1, self.project)
        self.task_manager.remove_task_from_project(self.task1, self.project)
        self.assertNotIn(self.task1, self.project.tasks)

    def test_get_project(self):
        """Тестирование получения проекта по имени"""
        project = self.task_manager.get_project("Проект 1")
        self.assertEqual(project, self.project)

    def test_add_invalid_task_to_project(self):
        """Тестирование попытки добавить несуществующую задачу в проект"""
        with self.assertRaises(TypeError):
            self.task_manager.add_task_to_project("Некорректная задача", self.project)

    def test_add_task_to_invalid_project(self):
        """Тестирование попытки добавить задачу в несуществующий проект"""
        with self.assertRaises(TypeError):
            self.task_manager.add_task_to_project(self.task1, "Некорректный проект")

if __name__ == '__main__':
    unittest.main()
