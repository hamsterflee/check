[![Python CI](https://github.com/hamsterflee/check/actions/workflows/main.yml/badge.svg)](https://github.com/hamsterflee/check/actions/workflows/main.yml)
[![Coverage Status](https://coveralls.io/repos/github/hamsterflee/check/badge.svg?branch=main)](https://coveralls.io/github/hamsterflee/check?branch=main)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=hamsterflee_check&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=hamsterflee_check)

## Тесты
### Блочные тесты
1. **Создание задачи** (позитивный)
   - Название класса: `TestTask`
   - Название метода: `test_create_task`
   - Входные данные: `name="Задача 1", description="Описание задачи", priority="высокий", deadline="2024-12-01"`
   - Ожидаемый результат: Создание задачи с заданными параметрами

2. **Создание задачи с пустыми значениями** (негативный)
   - Название класса: `TestTask`
   - Название метода: `test_create_task_with_empty_values`
   - Входные данные: Попытка создать задачу с пустыми значениями в поле name, description, priority, deadline
   - Ожидаемый результат: Выброс исключения `ValueError`

3. **Проверка корректного формата дедлайна** (позитивный)
   - Название класса: `TestTask`
   - Название метода: `test_validate_deadline_valid`
   - Входные данные: `deadline="2024-12-01"`
   - Ожидаемый результат: Без исключений

4. **Проверка некорректного формата дедлайна** (негативный)
   - Название класса: `TestTask`
   - Название метода: `test_validate_deadline_invalid_format`
   - Входные данные: `deadline="01-12-2024"`
   - Ожидаемый результат: Выброс исключения `ValueError`

5. **Изменение статуса задачи** (позитивный)
   - Название класса: `TestTask`
   - Название метода: `test_change_status`
   - Входные данные: Смена статуса задачи на "выполняется"
   - Ожидаемый результат: Статус задачи изменен на "выполняется"

6. **Проверка просроченности задачи** (позитивный)
   - Название класса: `TestTask`
   - Название метода: `test_is_due`
   - Входные данные: `deadline="2024-11-01"` с текущей датой "2024-11-02"
   - Ожидаемый результат: Возврат `True`

7. **Проверка, что задача не просрочена** (позитивный)
   - Название класса: `TestTask`
   - Название метода: `test_is_due_not_due`
   - Входные данные: `deadline="2024-12-01"` с текущей датой "2024-11-02"
   - Ожидаемый результат: Возврат `False`

8. **Проверка просроченности задачи с высоким приоритетом** (позитивный)
   - Название класса: `TestTask`
   - Название метода: `test_high_priority_task_is_due`
   - Входные данные: `deadline="2024-11-01"` с текущей датой "2024-11-02"
   - Ожидаемый результат: Сообщение о просроченной задаче с высоким приоритетом

9. **Проверка просроченности задачи с низким приоритетом** (позитивный)
   - Название класса: `TestTask`
   - Название метода: `test_low_priority_task_is_due`
   - Входные данные: `deadline="2024-11-01"` с текущей датой "2024-11-02"
   - Ожидаемый результат: Сообщение о просроченной задаче с низким приоритетом

10. **Выделение ресурсов для задачи с высоким приоритетом (выполняется)** (позитивный)
    - Название класса: `TestTask`
    - Название метода: `test_allocate_resources_high_priority`
    - Входные данные: Статус задачи "выполняется"
    - Ожидаемый результат: Сообщение о выделении ресурсов

11. **Выделение ресурсов для задачи с низким приоритетом (выполняется)** (позитивный)
    - Название класса: `TestTask`
    - Название метода: `test_allocate_resources_low_priority`
    - Входные данные: Статус задачи "выполняется"
    - Ожидаемый результат: Сообщение о выделении ресурсов

12. **Выделение ресурсов для ожидающей задачи с высоким приоритетом (ожидает)** (позитивный)
    - Название класса: `TestTask`
    - Название метода: `test_allocate_resources_high_priority_waiting`
    - Входные данные: Статус задачи "ожидает"
    - Ожидаемый результат: Сообщение о том, что задача ожидает начала выполнения

13. **Выделение ресурсов для ожидающей задачи с низким приоритетом (ожидает)** (позитивный)
    - Название класса: `TestTask`
    - Название метода: `test_allocate_resources_low_priority_waiting`
    - Входные данные: Статус задачи "ожидает"
    - Ожидаемый результат: Сообщение о том, что задача может быть выполнена позже

14. **Инициализация проекта** (позитивный)
    - Название класса: `TestProject`
    - Название метода: `test_project_initialization`
    - Входные данные: `name="Проект 1", description="Описание проекта"`
    - Ожидаемый результат: Создание проекта с заданными параметрами и без задач

15. **Создание проекта без имени** (негативный)
    - Название класса: `TestProject`
    - Название метода: `test_project_without_name`
    - Входные данные: Попытка создать проект с пустым значением в поле name
    - Ожидаемый результат: Выброс исключения `ValueError`

16. **Получение всех задач проекта** (позитивный)
    - Название класса: `TestProject`
    - Название метода: `test_get_all_tasks`
    - Входные данные: Добавление трех задач в проект
    - Ожидаемый результат: Получение списка из трех задач

17. **Анализ задач проекта** (позитивный)
    - Название класса: `TestProject`
    - Название метода: `test_get_task_summary`
    - Входные данные: Добавление трех задач в проект, одна из которых выполнена
    - Ожидаемый результат: Сообщение о количестве завершенных и ожидающих задач

18. **Получение просроченных задач** (позитивный)
    - Название класса: `TestProject`
    - Название метода: `test_get_due_tasks`
    - Входные данные: Добавление трех задач с различными сроками выполнения
    - Ожидаемый результат: Получение списка из двух просроченных задач

19. **Строковое представление проекта** (позитивный)
    - Название класса: `TestProject`
    - Название метода: `test_project_str`
    - Входные данные: Добавление двух задач в проект
    - Ожидаемый результат: Строка с названием проекта и количеством задач

20. **Тест расстояния Левенштейна для одинаковых строк** (позитивный)
    - Название класса: `TestLevenshtein`
    - Название метода: `test_levenshtein_distance_identical`
    - Входные данные: строка1="task", строка2="task"
    - Ожидаемый результат: Расстояние Левенштейна равно 0, так как строки идентичны.

21. **Тест расстояния Левенштейна для различных строк** (позитивный)
    - Название класса: `TestLevenshtein`
    - Название метода: `test_levenshtein_distance_different`
    - Входные данные: строка1="task", строка2="mask"
    - Ожидаемый результат: Расстояние Левенштейна равно 1, так как строки отличаются на одну букву.

22. **Тест расстояния Левенштейна для пустой строки** (позитивный)
    - Название класса: `TestLevenshtein`
    - Название метода: `test_levenshtein_distance_empty`
    - Входные данные: строка1="", строка2="task"
    - Ожидаемый результат: Расстояние Левенштейна равно 4, так как пустая строка отличается от "task" на 4 символа.

23. **Тестирование определения схожих названий (позитивный случай)** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_is_similar_task_name_positive`
    - Входные данные: строка1="Hamster", строка2="hamsters"
    - Ожидаемый результат: Метод должен вернуть `True`, так как названия считаются схожими.

24. **Тестирование определения несхожих названий** (негативный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_is_similar_task_name_negative`
    - Входные данные: строка1="Task", строка2="Project"
    - Ожидаемый результат: Метод должен вернуть `False`, так как названия не схожи.

25. **Тестирование регистронезависимости** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_is_similar_task_name_case_insensitive`
    - Входные данные: строка1="task", строка2="TASK"
    - Ожидаемый результат: Метод должен вернуть `True`, так как сравнение должно быть регистронезависимым.

26. **Тестирование поиска похожей задачи среди существующих** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_check_task_similarity_found`
    - Входные данные: строка="Задача 1"
    - Ожидаемый результат: Метод должен вернуть название задачи "Задача 1", если она существует в списке.

27. **Тестирование отсутствия похожей задачи** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_check_task_similarity_not_found`
    - Входные данные: строка="Совершенно новая задача"
    - Ожидаемый результат: Метод должен вернуть `None`, так как задачи с таким названием нет в списке.

28. **Тестирование добавления задачи с похожим названием** (негативный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_add_task_with_similar_name`
    - Входные данные: название="Задача 1а", описание="Описание задачи", приоритет="средний", срок="2024-12-03"
    - Ожидаемый результат: Метод должен вернуть сообщение о схожести названий и запросить подтверждение добавления задачи: `("Задача 'Задача 1а' очень похожа на уже существующую задачу 'Задача 1'. Вы уверены, что хотите добавить её?", False)`.

29. **Тестирование добавления задачи с уникальным названием** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_add_task_no_similar_name`
    - Входные данные: название="Совершенно новая задача", описание="Описание", приоритет="высокий", срок="2024-12-04"
    - Ожидаемый результат: Метод должен добавить задачу в список и подтвердить добавление.

30. **Создание проекта с длинным именем** (негативный)
    - Название класса: TestProject
    - Название метода: test_project_with_long_name
    - Входные данные: Имя проекта длиной 51 символ
    - Ожидаемый результат: Ошибка ValueError с сообщением "Имя проекта не может превышать 50 символов"

31. **Создание проекта с длинным описанием** (негативный)
    - Название класса: TestProject
    - Название метода: test_project_with_long_description
    - Входные данные: Описание проекта длиной 201 символ
    - Ожидаемый результат: Ошибка ValueError с сообщением "Описание проекта не может превышать 200 символов"

32. **Проверка создания задачи с пустым названием** (негативный)
    - Название класса: TestTask
    - Название метода: test_create_task_with_empty_name
    - Входные данные: Пустое название задачи при создании
    - Ожидаемый результат: ValueError, сообщение о том, что название не может быть пустым

33. **Проверка создания задачи с пустым описанием** (негативный)
    - Название класса: TestTask
    - Название метода: test_create_task_with_empty_description
    - Входные данные: Пустое описание задачи при создании
    - Ожидаемый результат: ValueError, сообщение о том, что описание не может быть пустым

34. **Проверка создания задачи с пустым приоритетом** (негативный)
    - Название класса: TestTask
    - Название метода: test_create_task_with_empty_priority
    - Входные данные: Пустой приоритет задачи при создании
    - Ожидаемый результат: ValueError, сообщение о том, что приоритет не может быть пустым

35. **Проверка создания задачи с пустым сроком** (негативный)
    - Название класса: TestTask
    - Название метода: test_create_task_with_empty_deadline
    - Входные данные: Пустой срок задачи при создании
    - Ожидаемый результат: ValueError, сообщение о том, что срок не может быть пустым

36. **Проверка создания задачи с длинным названием** (негативный)
    - Название класса: TestTask
    - Название метода: test_create_task_with_long_name
    - Входные данные: Название задачи длиной более 100 символов
    - Ожидаемый результат: ValueError, сообщение о превышении максимальной длины названия

37. **Проверка создания задачи с длинным описанием** (негативный)
    - Название класса: TestTask
    - Название метода: test_create_task_with_long_description
    - Входные данные: Описание задачи длиной более 500 символов
    - Ожидаемый результат: ValueError, сообщение о превышении максимальной длины описания

38. **Установка дедлайна в прошедшую дату** (негативный)
    - Название класса: TestTask
    - Название метода: test_set_deadline_past_date
    - Входные данные: Дедлайн задачи, установленный на дату в прошлом
    - Ожидаемый результат: ValueError, сообщение о том, что срок не может быть в прошлом

39. **Попытка установить некорректный статус** (негативный)
    - Название класса: TestTask
    - Название метода: test_change_status_invalid
    - Входные данные: Попытка установить статус, который не является допустимым
    - Ожидаемый результат: ValueError, сообщение о недопустимости статуса

40. **Попытка передать число вместо строки в качестве одного из аргументов** (негативный)
    - Название класса: TestTaskManager
    - Название метода: test_levenshtein_distance_non_string
    - Входные данные: Попытка передать в функцию (123, "test")
    - Ожидаемый результат: Выброс исключения ValueError

41. **Попытка передать None вместо строки в качестве одного из аргументов** (негативный)
    - Название класса: TestTaskManager
    - Название метода: test_levenshtein_distance_none
    - Входные данные: Попытка передать в функцию (None, "test")
    - Ожидаемый результат: Выброс исключения ValueError

42. **Попытка передать список вместо строки в качестве одного из аргументов** (негативный)
    - Название класса: TestTaskManager
    - Название метода: test_levenshtein_distance_list_argument
    - Входные данные: Попытка передать в функцию (["test"], "test")
    - Ожидаемый результат: Выброс исключения ValueError

### Интеграционные тесты

1. **Добавление задачи в менеджер задач** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_add_task`
    - Входные данные: Добавление новой задачи
    - Ожидаемый результат: Задача добавлена в список задач менеджера

2. **Удаление задачи из менеджера задач** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_remove_task`
    - Входные данные: Удаление существующей задачи
    - Ожидаемый результат: Задача удалена из списка задач менеджера

3. **Поиск задачи по имени** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_find_task_by_name`
    - Входные данные: Поиск задачи по имени
    - Ожидаемый результат: Найденная задача соответствует запросу

4. **Поиск просроченных задач** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_find_due_tasks`
    - Входные данные: Установка прошедшей даты для одной из задач
    - Ожидаемый результат: Возврат списка просроченных задач

5. **Поиск задач в ожидании** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_find_pending_tasks`
    - Входные данные: Установка статуса "ожидает" для одной из задач
    - Ожидаемый результат: Возврат списка задач в ожидании

6. **Сортировка задач по сроку выполнения** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_sort_tasks_by_deadline`
    - Входные данные: Две задачи с разными сроками выполнения
    - Ожидаемый результат: Задачи отсортированы по возрастанию сроков выполнения

7. **Сортировка задач по приоритету** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_sort_tasks_by_priority`
    - Входные данные: Три задачи с разными приоритетами
    - Ожидаемый результат: Задачи отсортированы по приоритету: высокий, низкий, средний

8. **Изменение статуса задачи через менеджер задач** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_change_task_status`
    - Входные данные: Изменение статуса задачи на "выполняется"
    - Ожидаемый результат: Статус задачи изменен на "выполняется"

9. **Выделение ресурсов для задачи через менеджер задач (выполняется)** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_allocate_resources`
    - Входные данные: Выделение ресурсов для задачи с высоким или низким приоритетом и статусом "выполняется"
    - Ожидаемый результат: Сообщение о выделении ресурсов

10. **Создание проекта через менеджер задач** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_create_project`
    - Входные данные: Создание нового проекта
    - Ожидаемый результат: Проект создан и добавлен в список проектов менеджера

11. **Получение проекта по имени** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_get_project`
    - Входные данные: Получение проекта по имени
    - Ожидаемый результат: Возвращён проект с заданным именем

### Аттестационные тесты
1. **Добавление задачи в проект через менеджер задач** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_add_task_to_project`
    - Входные данные: Добавление существующей задачи в проект
    - Ожидаемый результат: Задача добавлена в список задач проекта

2. **Удаление задачи из проекта через менеджер задач** (позитивный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_remove_task_from_project`
    - Входные данные: Удаление существующей задачи из проекта
    - Ожидаемый результат: Задача удалена из списка задач проекта
   
3. **Добавление невалидной задачи в проект** (негативный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_add_invalid_task_to_project`
    - Входные данные: Попытка добавить несуществующую задачу в проект
    - Ожидаемый результат: Выброс исключения `TypeError`

4. **Добавление задачи в невалидный проект** (негативный)
    - Название класса: `TestTaskManager`
    - Название метода: `test_add_task_to_invalid_project`
    - Входные данные: Попытка добавить задачу в несуществующий проект
    - Ожидаемый результат: Выброс исключения `TypeError`
