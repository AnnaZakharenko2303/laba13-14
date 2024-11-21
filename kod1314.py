import random
import math
import threading

def generate_random_points(n):
    """Генерация случайных точек."""
    return [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(n)]

def input_points():
    """Ввод точек вручную."""
    points = input("Введите точки в формате (x1, y1), (x2, y2), ... : ")
    points = points.strip().split('), (')
    points = [tuple(map(float, point.strip('()').split(','))) for point in points]
    return points

def distance(point1, point2):
    """Вычисление расстояния между двумя точками."""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

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

def calculate_nearest_points(points):
    """Функция для запуска расчетов в отдельном потоке."""
    results = find_nearest_points(points)
    for point, nearest in results:
        print(f"Точка {point} ближайшая точка {nearest}")

def main_menu():
    """Главное меню приложения."""
    points = []

    while True:
        print("\nМеню:")
        print("1) Генерация случайных точек")
        print("2) Ввод точек вручную")
        print("3) Найти ближайшие точки")
        print("0) Завершение работы")

        choice = input("Выберите пункт меню: ")

        if choice == '1':
            num_points = int(input("Введите количество случайных точек: "))
            # Создаем поток для генерации случайных точек
            generation_thread = threading.Thread(target=lambda: generate_and_display(num_points))
            generation_thread.start()
            generation_thread.join()  # Ждем завершения потока

        elif choice == '2':
            # Создаем поток для ввода точек вручную
            input_thread = threading.Thread(target=lambda: input_and_display())
            input_thread.start()
            input_thread.join()  # Ждем завершения потока

        elif choice == '3':
            if not points:
                print("Ошибка: Необходимо сначала ввести или сгенерировать точки.")
                continue
            
            # Создаем поток для выполнения расчетов
            calculation_thread = threading.Thread(target=calculate_nearest_points, args=(points,))
            calculation_thread.start()
            calculation_thread.join()  # Ждем завершения потока
            
        elif choice == '0':
            print("Завершение работы программы.")
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")

def generate_and_display(num_points):
    """Генерирует случайные точки и отображает их."""
    global points
    points = generate_random_points(num_points)
    print(f"Сгенерированные точки: {points}")

def input_and_display():
    """Вводит точки вручную и отображает их."""
    global points
    points = input_points()
    print(f"Введенные точки: {points}")

if __name__ == "__main__":
    main_menu()
