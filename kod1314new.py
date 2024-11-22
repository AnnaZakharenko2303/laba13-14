def find_nearest_points(points):
    """Находит ближайшую точку для каждой точки."""
    result = []
    for i, point in enumerate(points):
        nearest_point = None
        min_distance = float('inf')
        for j, other_point in enumerate(points):
            if i != j:
                dist = distance(point, other_point)
                if dist < min_distance:
                    min_distance = dist
                    nearest_point = other_point
        result.append((point, nearest_point))
    return result

def calculate_nearest_points(points_queue):
    """Функция для запуска расчетов в отдельном потоке."""
    while True:
        points = points_queue.get()  # Получаем точки из очереди
        if points is None:  # Если получено значение None, выходим из цикла
            break
        results = find_nearest_points(points)
        for point, nearest in results:
            print(f"Точка {point} ближайшая точка {nearest}")
        points_queue.task_done()  # Указываем, что задача завершена

def main_menu():
    """Главное меню приложения."""
    points_queue = queue.Queue()  # Создаем очередь для передачи точек между потоками
    calculation_thread = threading.Thread(target=calculate_nearest_points, args=(points_queue,))
    calculation_thread.start()  # Запускаем поток для вычислений

    while True:
        print("\nМеню:")
        print("1) Генерация случайных точек")
        print("2) Ввод точек вручную")
        print("3) Найти ближайшие точки")
        print("0) Завершение работы")

        choice = input("Выберите пункт меню: ")

        if choice == '1':
            num_points = int(input("Введите количество случайных точек: "))
            generate_and_display(num_points)

        elif choice == '2':
            input_and_display()

        elif choice == '3':
            if not points:
                print("Ошибка: Необходимо сначала ввести или сгенерировать точки.")
                continue
            
            points_queue.put(points)  # Добавляем точки в очередь для обработки
            
        elif choice == '0':
            print("Завершение работы программы.")
            points_queue.put(None)  # Завершаем поток вычислений
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")
