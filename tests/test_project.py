import unittest
from freezegun import freeze_time
from task import Task, HighPriorityTask, LowPriorityTask
from project import Project

class TestProject(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        self.project = Project(name="Проект 1", description="Описание проекта")
        self.task1 = Task(name="Задача 1", description="Описание задачи 1", priority="средний", deadline="2024-12-01")
        self.task2 = HighPriorityTask(name="Задача 2", description="Описание задачи 2", deadline="2024-11-01")
        self.task3 = LowPriorityTask(name="Задача 3", description="Описание задачи 3", deadline="2024-11-30")

    def test_project_initialization(self):
        """Тест инициализации проекта"""
        self.assertEqual(self.project.name, "Проект 1")
        self.assertEqual(self.project.description, "Описание проекта")
        self.assertEqual(len(self.project.tasks), 0)

    def test_project_without_name(self):
        """Тест создания проекта без имени"""
        with self.assertRaises(ValueError):
            Project(name="")

    def test_get_all_tasks(self):
        """Тест получения всех задач проекта"""
        self.project.tasks.extend([self.task1, self.task2, self.task3])
        tasks = self.project.get_all_tasks()
        self.assertEqual(len(tasks), 3)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)
        self.assertIn(self.task3, tasks)

    def test_get_task_summary(self):
        """Тест анализа задач проекта"""
        self.project.tasks.extend([self.task1, self.task2, self.task3])
        self.task1.change_status("выполнена")
        summary = self.project._get_task_summary()
        self.assertEqual(summary, "Задач завершено: 1, в ожидании: 2")

    @freeze_time("2024-12-01")
    def test_get_due_tasks(self):
        """Тест получения просроченных задач с использованием freezegun"""
        self.task1.deadline = "2024-11-30"  # Просрочена
        self.task2.deadline = "2024-12-02"  # Не просрочена
        self.task3.deadline = "2024-11-29"  # Просрочена
        self.project.tasks.extend([self.task1, self.task2, self.task3])
        due_tasks = self.project.get_due_tasks()
        self.assertEqual(len(due_tasks), 2)
        self.assertIn(self.task1, due_tasks)
        self.assertIn(self.task3, due_tasks)
        self.assertNotIn(self.task2, due_tasks)

    def test_project_str(self):
        """Тест строкового представления проекта"""
        self.project.tasks.extend([self.task1, self.task2])
        self.assertEqual(str(self.project), "Проект: Проект 1, Задач: 2")

if __name__ == '__main__':
    unittest.main()
