import unittest
from datetime import datetime, timedelta
from task import Task, HighPriorityTask, LowPriorityTask
from task_manager import TaskManager

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
        new_task = Task(name="Третья задача", description="Описание задачи", priority="средний", deadline="2024-12-01")
        result = self.task_manager.add_task(new_task)
        self.assertEqual(result, ("Задача 'Третья задача' успешно добавлена.", True))

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

    def test_levenshtein_distance_identical(self):
        """Тестирование расстояния Левенштейна для одинаковых строк"""
        distance = self.task_manager._levenshtein_distance("task", "task")
        self.assertEqual(distance, 0)

    def test_levenshtein_distance_different(self):
        """Тестирование расстояния Левенштейна для различных строк"""
        distance = self.task_manager._levenshtein_distance("task", "mask")
        self.assertEqual(distance, 1)

    def test_levenshtein_distance_empty(self):
        """Тестирование расстояния Левенштейна для пустой строки"""
        distance = self.task_manager._levenshtein_distance("", "task")
        self.assertEqual(distance, 4)

    def test_levenshtein_distance_non_string(self):
        """Тестирование расстояния Левенштейна с нестроковыми аргументами"""
        with self.assertRaises(TypeError):
            self.task_manager._levenshtein_distance(123, "test")

    def test_levenshtein_distance_none(self):
        """Тестирование расстояния Левенштейна с None в качестве аргумента"""
        with self.assertRaises(TypeError):
            self.task_manager._levenshtein_distance(None, "test")

    def test_is_similar_task_name_positive(self):
        """Тестирование определения схожих названий (позитивный случай)"""
        result = self.task_manager._is_similar_task_name("Hamster", "hamsters")
        self.assertTrue(result)

    def test_is_similar_task_name_negative(self):
        """Тестирование определения несхожих названий"""
        result = self.task_manager._is_similar_task_name("Task", "Project")
        self.assertFalse(result)

    def test_is_similar_task_name_case_insensitive(self):
        """Тестирование регистронезависимости"""
        result = self.task_manager._is_similar_task_name("task", "TASK")
        self.assertTrue(result)

    def test_check_task_similarity_found(self):
        """Тестирование поиска похожей задачи среди существующих"""
        similar_name = self.task_manager._check_task_similarity("Задача 1")
        self.assertEqual(similar_name, "Задача 1")

    def test_check_task_similarity_not_found(self):
        """Тестирование отсутствия похожей задачи"""
        similar_name = self.task_manager._check_task_similarity("Совершенно новая задача")
        self.assertIsNone(similar_name)

    def test_add_task_with_similar_name(self):
        """Тестирование добавления задачи с похожим названием"""
        new_task = Task(name="Задача 1а", description="Описание задачи", priority="средний", deadline="2024-12-03")
        result = self.task_manager.add_task(new_task)
        self.assertEqual(result, (
        "Задача 'Задача 1а' очень похожа на уже существующую задачу 'Задача 1'. Вы уверены, что хотите добавить её?",
        False))

    def test_add_task_no_similar_name(self):
        """Тестирование добавления задачи с уникальным названием"""
        new_task = Task(name="Совершенно новая задача", description="Описание", priority="высокий", deadline="2024-12-04")
        self.task_manager.add_task(new_task)
        self.assertIn(new_task, self.task_manager.tasks)

if __name__ == '__main__':
    unittest.main()
