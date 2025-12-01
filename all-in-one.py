"""
ЛР12 - Все задания в одном файле
Автор: Николай Козик
"""

# ========== ЗАДАНИЕ 1: Класс Client ==========
print("=" * 50)
print("ЗАДАНИЕ 1: Класс Client")
print("=" * 50)

class Client:
    """Класс для представления клиента компании"""
    
    def __init__(self, name: str, cargo_weight: float, is_vip: bool = False):
        """
        Инициализация клиента
        
        Args:
            name: имя клиента
            cargo_weight: вес груза в тоннах
            is_vip: VIP статус (по умолчанию False)
        """
        self.validate_data(name, cargo_weight, is_vip)
        
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip
    
    def validate_data(self, name: str, cargo_weight: float, is_vip: bool):
        """Валидация входных данных"""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя клиента должно быть непустой строкой")
        
        if not isinstance(cargo_weight, (int, float)) or cargo_weight <= 0:
            raise ValueError("Вес груза должен быть положительным числом")
        
        if not isinstance(is_vip, bool):
            raise ValueError("VIP статус должен быть булевым значением")
    
    def __str__(self):
        """Строковое представление клиента"""
        vip_status = "VIP" if self.is_vip else "Обычный"
        return f"Клиент: {self.name} | Груз: {self.cargo_weight} т | Статус: {vip_status}"
    
    def __repr__(self):
        return f"Client(name='{self.name}', cargo_weight={self.cargo_weight}, is_vip={self.is_vip})"


# Демонстрация работы задания 1
try:
    client1 = Client("Иван Иванов", 5.5, True)
    client2 = Client("Петр Петров", 3.2)
    
    print("Созданные клиенты:")
    print(f"1. {client1}")
    print(f"2. {client2}")
    
    # Проверка валидации
    print("\nПроверка валидации:")
    try:
        invalid_client = Client("", -5, "yes")
    except ValueError as e:
        print(f" Ошибка валидации: {e}")
    
    print("\nЗадание 1 выполнено успешно!")
    
except Exception as e:
    print(f" Ошибка: {e}")

input("\nНажмите Enter для продолжения...\n")

# ========== ЗАДАНИЕ 2: Класс Vehicle ==========
print("=" * 50)
print("ЗАДАНИЕ 2: Базовый класс Vehicle")
print("=" * 50)

import uuid

class Vehicle:
    """Базовый класс транспортного средства"""
    
    def __init__(self, capacity: float):
        """
        Инициализация транспортного средства
        
        Args:
            capacity: грузоподъемность в тоннах
        """
        self.validate_capacity(capacity)
        
        self.vehicle_id = str(uuid.uuid4())[:8]  # Короткий уникальный ID
        self.capacity = capacity
        self.current_load = 0.0
        self.clients_list = []
    
    def validate_capacity(self, capacity: float):
        """Валидация грузоподъемности"""
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Грузоподъемность должна быть положительным числом")
    
    def load_cargo(self, client):
        """
        Загрузка груза клиента
        
        Args:
            client: объект Client
            
        Returns:
            bool: True если загрузка успешна, False если нет места
        """
        # Валидация типа клиента
        if not isinstance(client, Client):
            raise TypeError("Аргумент должен быть объектом класса Client")
        
        # Проверка доступного места
        available_capacity = self.capacity - self.current_load
        
        if client.cargo_weight <= available_capacity:
            self.current_load += client.cargo_weight
            self.clients_list.append(client)
            return True
        else:
            return False
    
    def unload_cargo(self):
        """Разгрузка всего транспорта"""
        self.current_load = 0.0
        self.clients_list.clear()
    
    def get_available_capacity(self) -> float:
        """Получить доступную грузоподъемность"""
        return self.capacity - self.current_load
    
    def __str__(self):
        """Строковое представление транспорта"""
        return (f"Транспорт ID: {self.vehicle_id} | "
                f"Грузоподъемность: {self.capacity} т | "
                f"Текущая загрузка: {self.current_load:.1f} т | "
                f"Свободно: {self.get_available_capacity():.1f} т")
    
    def __repr__(self):
        return f"Vehicle(id={self.vehicle_id}, capacity={self.capacity}, load={self.current_load})"


# Демонстрация работы задания 2
try:
    # Создание транспорта
    vehicle = Vehicle(10.0)
    print(f"Создан транспорт: {vehicle}")
    
    # Создание клиентов
    client1 = Client("VIP Клиент", 3.0, True)
    client2 = Client("Обычный Клиент", 4.0)
    
    # Загрузка грузов
    print("\nЗагрузка грузов:")
    result1 = vehicle.load_cargo(client1)
    print(f"Загрузка {client1.name}: {'Успешно' if result1 else 'Не удалось'}")
    
    result2 = vehicle.load_cargo(client2)
    print(f"Загрузка {client2.name}: {'Успешно' if result2 else 'Не удалось'}")
    
    print(f"\nПосле загрузки: {vehicle}")
    print(f"Клиенты в транспорте: {len(vehicle.clients_list)}")
    
    # Проверка перегрузки
    client3 = Client("Тяжелый Клиент", 5.0)
    result3 = vehicle.load_cargo(client3)
    print(f"\nПопытка загрузки {client3.name}: {'Успешно' if result3 else 'Не удалось (нет места)'}")
    
    print("\nЗадание 2 выполнено успешно!")
    
except Exception as e:
    print(f" Ошибка: {e}")

input("\nНажмите Enter для продолжения...\n")

# ========== ЗАДАНИЕ 3: Классы Airplane, Van, TransportCompany ==========
print("=" * 50)
print("ЗАДАНИЕ 3: Классы Airplane, Van, TransportCompany")
print("=" * 50)

class Airplane(Vehicle):
    """Класс самолета, наследующий от Vehicle"""
    
    def __init__(self, capacity: float, max_altitude: float):
        """
        Инициализация самолета
        
        Args:
            capacity: грузоподъемность в тоннах
            max_altitude: максимальная высота полета в метрах
        """
        super().__init__(capacity)
        
        self.validate_altitude(max_altitude)
        self.max_altitude = max_altitude
    
    def validate_altitude(self, altitude: float):
        """Валидация высоты полета"""
        if not isinstance(altitude, (int, float)) or altitude <= 0:
            raise ValueError("Максимальная высота полета должна быть положительным числом")
    
    def __str__(self):
        """Строковое представление самолета"""
        base_info = super().__str__()
        return f"{base_info} | Тип: Самолет | Макс. высота: {self.max_altitude} м"
    
    def __repr__(self):
        return (f"Airplane(id={self.vehicle_id}, capacity={self.capacity}, "
                f"load={self.current_load}, altitude={self.max_altitude})")


class Van(Vehicle):
    """Класс фургона, наследующий от Vehicle"""
    
    def __init__(self, capacity: float, is_refrigerated: bool = False):
        """
        Инициализация фургона
        
        Args:
            capacity: грузоподъемность в тоннах
            is_refrigerated: наличие холодильника
        """
        super().__init__(capacity)
        
        if not isinstance(is_refrigerated, bool):
            raise ValueError("Параметр is_refrigerated должен быть булевым значением")
        
        self.is_refrigerated = is_refrigerated
    
    def __str__(self):
        """Строковое представление фургона"""
        base_info = super().__str__()
        fridge = "с холодильником" if self.is_refrigerated else "без холодильника"
        return f"{base_info} | Тип: Фургон ({fridge})"
    
    def __repr__(self):
        return (f"Van(id={self.vehicle_id}, capacity={self.capacity}, "
                f"load={self.current_load}, refrigerated={self.is_refrigerated})")


class TransportCompany:
    """Класс транспортной компании"""
    
    def __init__(self, name: str):
        """
        Инициализация транспортной компании
        
        Args:
            name: название компании
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название компании должно быть непустой строкой")
        
        self.name = name
        self.vehicles = []
        self.clients = []
    
    def add_vehicle(self, vehicle):
        """Добавление транспортного средства"""
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Аргумент должен быть объектом класса Vehicle или его наследником")
        
        self.vehicles.append(vehicle)
    
    def list_vehicles(self):
        """Получение списка всех транспортных средств"""
        return self.vehicles.copy()
    
    def add_client(self, client):
        """Добавление клиента"""
        if not isinstance(client, Client):
            raise TypeError("Аргумент должен быть объектом класса Client")
        
        self.clients.append(client)
    
    def optimize_cargo_distribution(self):
        """
        Оптимизация распределения грузов
        
        Returns:
            dict: информация о распределении
        """
        # Разделяем клиентов на VIP и обычных
        vip_clients = [c for c in self.clients if c.is_vip]
        regular_clients = [c for c in self.clients if not c.is_vip]
        
        # Сортируем транспорт по убыванию грузоподъемности
        sorted_vehicles = sorted(self.vehicles, key=lambda v: v.capacity, reverse=True)
        
        # Сначала загружаем VIP клиентов
        unloaded_vip = []
        for client in vip_clients:
            loaded = False
            for vehicle in sorted_vehicles:
                if vehicle.load_cargo(client):
                    loaded = True
                    break
            if not loaded:
                unloaded_vip.append(client)
        
        # Затем загружаем обычных клиентов
        unloaded_regular = []
        for client in regular_clients:
            loaded = False
            for vehicle in sorted_vehicles:
                if vehicle.load_cargo(client):
                    loaded = True
                    break
            if not loaded:
                unloaded_regular.append(client)
        
        # Собираем статистику
        used_vehicles = [v for v in sorted_vehicles if v.current_load > 0]
        
        return {
            'total_clients': len(self.clients),
            'vip_clients': len(vip_clients),
            'regular_clients': len(regular_clients),
            'used_vehicles': len(used_vehicles),
            'total_vehicles': len(self.vehicles),
            'unloaded_vip': unloaded_vip,
            'unloaded_regular': unloaded_regular,
            'utilization': sum(v.current_load for v in used_vehicles) / sum(v.capacity for v in used_vehicles) * 100 if used_vehicles else 0
        }
    
    def clear_all_loads(self):
        """Очистка всех загрузок транспорта"""
        for vehicle in self.vehicles:
            vehicle.unload_cargo()
    
    def __str__(self):
        """Строковое представление компании"""
        return (f"Компания: {self.name} | "
                f"Транспорт: {len(self.vehicles)} ед. | "
                f"Клиенты: {len(self.clients)} чел.")


# Демонстрация работы задания 3
try:
    # Создание компании
    company = TransportCompany("Быстрая Доставка")
    print(f"Создана компания: {company}")
    
    # Добавление транспорта
    airplane = Airplane(20.0, 10000)
    van1 = Van(5.0, True)
    van2 = Van(3.0)
    
    company.add_vehicle(airplane)
    company.add_vehicle(van1)
    company.add_vehicle(van2)
    
    print(f"\nДобавлен транспорт:")
    for i, v in enumerate(company.vehicles, 1):
        print(f"{i}. {v}")
    
    # Добавление клиентов
    clients = [
        Client("VIP Клиент 1", 8.0, True),
        Client("VIP Клиент 2", 5.0, True),
        Client("Клиент 3", 6.0),
        Client("Клиент 4", 4.0),
        Client("Клиент 5", 7.0)
    ]
    
    for client in clients:
        company.add_client(client)
    
    print(f"\nДобавлено клиентов: {len(company.clients)}")
    
    # Оптимизация распределения
    print("\nОптимизация распределения грузов...")
    result = company.optimize_cargo_distribution()
    
    print("\nРезультаты распределения:")
    print(f"Всего клиентов: {result['total_clients']}")
    print(f"VIP клиентов: {result['vip_clients']}")
    print(f"Обычных клиентов: {result['regular_clients']}")
    print(f"Использовано транспорта: {result['used_vehicles']} из {result['total_vehicles']}")
    print(f"Загрузка транспорта: {result['utilization']:.1f}%")
    
    if result['unloaded_vip']:
        print(f"\n  Не загружено VIP клиентов: {len(result['unloaded_vip'])}")
    if result['unloaded_regular']:
        print(f"  Не загружено обычных клиентов: {len(result['unloaded_regular'])}")
    
    print("\nЗадание 3 выполнено успешно!")
    
except Exception as e:
    print(f" Ошибка: {e}")

input("\nНажмите Enter для продолжения к заданию 4...\n")

# ========== ЗАДАНИЕ 4: Система управления ==========
print("=" * 50)
print("ЗАДАНИЕ 4: Транспортная компания - система управления")
print("=" * 50)

def print_header():
    """Вывод заголовка программы"""
    print("=" * 60)
    print("ТРАНСПОРТНАЯ КОМПАНИЯ - СИСТЕМА УПРАВЛЕНИЯ")
    print("=" * 60)

def print_menu():
    """Вывод главного меню"""
    print("\nГЛАВНОЕ МЕНЮ:")
    print("1. Управление клиентами")
    print("2. Управление транспортом")
    print("3. Распределение грузов")
    print("4. Показать статистику")
    print("5. Тестовый запуск")
    print("0. Выход")

def get_float_input(prompt: str, min_val: float = 0) -> float:
    """Получение числа с плавающей точкой от пользователя"""
    while True:
        try:
            value = float(input(prompt))
            if value < min_val:
                print(f" Значение должно быть не меньше {min_val}")
                continue
            return value
        except ValueError:
            print(" Пожалуйста, введите число")

def get_bool_input(prompt: str) -> bool:
    """Получение булевого значения от пользователя"""
    while True:
        value = input(prompt + " (да/нет): ").strip().lower()
        if value in ['да', 'д', 'yes', 'y']:
            return True
        elif value in ['нет', 'н', 'no', 'n']:
            return False
        else:
            print(" Пожалуйста, введите 'да' или 'нет'")

def manage_clients_menu(company):
    """Меню управления клиентами"""
    while True:
        print("\n" + "-" * 40)
        print("УПРАВЛЕНИЕ КЛИЕНТАМИ")
        print("-" * 40)
        print("1. Добавить клиента")
        print("2. Показать всех клиентов")
        print("3. Удалить всех клиентов")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            print("\nДОБАВЛЕНИЕ НОВОГО КЛИЕНТА:")
            try:
                name = input("Введите имя клиента: ").strip()
                if not name:
                    print(" Имя не может быть пустым")
                    continue
                
                cargo_weight = get_float_input("Введите вес груза (т): ", 0.1)
                is_vip = get_bool_input("Это VIP клиент?")
                
                client = Client(name, cargo_weight, is_vip)
                company.add_client(client)
                print(f" Клиент {name} успешно добавлен!")
                
            except Exception as e:
                print(f" Ошибка: {e}")
        
        elif choice == "2":
            print("\nСПИСОК КЛИЕНТОВ:")
            if not company.clients:
                print("Клиентов нет")
            else:
                for i, client in enumerate(company.clients, 1):
                    print(f"{i}. {client}")
        
        elif choice == "3":
            if get_bool_input("Вы уверены что хотите удалить всех клиентов?"):
                company.clients.clear()
                print(" Все клиенты удалены")
        
        elif choice == "0":
            break
        
        else:
            print(" Неверный выбор")

def manage_vehicles_menu(company):
    """Меню управления транспортом"""
    while True:
        print("\n" + "-" * 40)
        print("УПРАВЛЕНИЕ ТРАНСПОРТОМ")
        print("-" * 40)
        print("1. Добавить самолет")
        print("2. Добавить фургон")
        print("3. Показать весь транспорт")
        print("4. Очистить все загрузки")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            print("\nДОБАВЛЕНИЕ САМОЛЕТА:")
            try:
                capacity = get_float_input("Введите грузоподъемность (т): ", 1)
                max_altitude = get_float_input("Введите максимальную высоту полета (м): ", 100)
                
                airplane = Airplane(capacity, max_altitude)
                company.add_vehicle(airplane)
                print(f" Самолет {airplane.vehicle_id} успешно добавлен!")
                
            except Exception as e:
                print(f" Ошибка: {e}")
        
        elif choice == "2":
            print("\nДОБАВЛЕНИЕ ФУРГОНА:")
            try:
                capacity = get_float_input("Введите грузоподъемность (т): ", 0.5)
                is_refrigerated = get_bool_input("Фургон с холодильником?")
                
                van = Van(capacity, is_refrigerated)
                company.add_vehicle(van)
                print(f" Фургон {van.vehicle_id} успешно добавлен!")
                
            except Exception as e:
                print(f" Ошибка: {e}")
        
        elif choice == "3":
            print("\nВЕСЬ ТРАНСПОРТ:")
            if not company.vehicles:
                print("Транспорта нет")
            else:
                for i, vehicle in enumerate(company.vehicles, 1):
                    print(f"{i}. {vehicle}")
        
        elif choice == "4":
            if get_bool_input("Очистить все загрузки транспорта?"):
                company.clear_all_loads()
                print(" Все загрузки очищены")
        
        elif choice == "0":
            break
        
        else:
            print(" Неверный выбор")

def optimize_cargo_menu(company):
    """Меню распределения грузов"""
    print("\n" + "-" * 40)
    print("РАСПРЕДЕЛЕНИЕ ГРУЗОВ")
    print("-" * 40)
    
    if not company.clients:
        print(" Нет клиентов для распределения")
        return
    
    if not company.vehicles:
        print(" Нет транспорта для распределения")
        return
    
    print("Оптимизация распределения грузов...")
    result = company.optimize_cargo_distribution()
    
    print("\n РЕЗУЛЬТАТЫ РАСПРЕДЕЛЕНИЯ:")
    print("-" * 40)
    print(f"Всего клиентов: {result['total_clients']}")
    print(f"  • VIP клиентов: {result['vip_clients']}")
    print(f"  • Обычных клиентов: {result['regular_clients']}")
    print(f"\nТранспорт:")
    print(f"  • Всего: {result['total_vehicles']} ед.")
    print(f"  • Использовано: {result['used_vehicles']} ед.")
    print(f"  • Загрузка: {result['utilization']:.1f}%")
    
    if result['unloaded_vip']:
        print(f"\n  Не загружено VIP клиентов: {len(result['unloaded_vip'])}")
        for client in result['unloaded_vip']:
            print(f"   • {client.name} (груз: {client.cargo_weight} т)")
    
    if result['unloaded_regular']:
        print(f"\n  Не загружено обычных клиентов: {len(result['unloaded_regular'])}")
        for client in result['unloaded_regular']:
            print(f"   • {client.name} (груз: {client.cargo_weight} т)")
    
    print("\nТранспорт после распределения:")
    for i, vehicle in enumerate(company.vehicles, 1):
        if vehicle.current_load > 0:
            print(f"{i}. {vehicle}")
            if vehicle.clients_list:
                print(f"   Клиенты: {', '.join([c.name for c in vehicle.clients_list])}")

def show_statistics_menu(company):
    """Меню статистики"""
    print("\n" + "-" * 40)
    print("СТАТИСТИКА КОМПАНИИ")
    print("-" * 40)
    
    print(f"Название: {company.name}")
    print(f"Клиенты: {len(company.clients)}")
    print(f"Транспорт: {len(company.vehicles)} ед.")
    
    if company.vehicles:
        total_capacity = sum(v.capacity for v in company.vehicles)
        total_load = sum(v.current_load for v in company.vehicles)
        print(f"\nОбщая грузоподъемность: {total_capacity:.1f} т")
        print(f"Общая загрузка: {total_load:.1f} т")
        print(f"Общая загрузка: {(total_load/total_capacity*100 if total_capacity > 0 else 0):.1f}%")
        
        # Статистика по типам транспорта
        airplanes = [v for v in company.vehicles if isinstance(v, Airplane)]
        vans = [v for v in company.vehicles if isinstance(v, Van)]
        
        print(f"\nСамолеты: {len(airplanes)} ед.")
        print(f"Фургоны: {len(vans)} ед.")
        print(f"  • С холодильником: {len([v for v in vans if v.is_refrigerated])}")
        print(f"  • Без холодильника: {len([v for v in vans if not v.is_refrigerated])}")
    
    if company.clients:
        vip_clients = [c for c in company.clients if c.is_vip]
        total_cargo = sum(c.cargo_weight for c in company.clients)
        print(f"\nVIP клиенты: {len(vip_clients)}")
        print(f"Общий вес грузов: {total_cargo:.1f} т")
        print(f"Средний вес груза: {total_cargo/len(company.clients):.1f} т")

def run_test_scenario():
    """Тестовый сценарий"""
    print("\n" + "=" * 40)
    print("ТЕСТОВЫЙ СЦЕНАРИЙ")
    print("=" * 40)
    
    try:
        # Создание компании
        company = TransportCompany("Тестовая Компания")
        
        # Добавление транспорта
        company.add_vehicle(Airplane(15.0, 8000))
        company.add_vehicle(Van(4.0, True))
        company.add_vehicle(Van(3.0))
        
        # Добавление клиентов
        company.add_client(Client("VIP Тест 1", 6.0, True))
        company.add_client(Client("VIP Тест 2", 4.0, True))
        company.add_client(Client("Тест 3", 5.0))
        company.add_client(Client("Тест 4", 3.0))
        company.add_client(Client("Тест 5", 8.0))
        
        print(" Создана тестовая компания с 3 единицами транспорта и 5 клиентами")
        
        # Распределение грузов
        print("\nЗапуск оптимизации...")
        result = company.optimize_cargo_distribution()
        
        print(f"\nРезультаты:")
        print(f"Использовано транспорта: {result['used_vehicles']}/{result['total_vehicles']}")
        print(f"Загрузка: {result['utilization']:.1f}%")
        
        if result['unloaded_vip'] or result['unloaded_regular']:
            print("  Не все клиенты были загружены")
        
        print("\nТестовый сценарий выполнен успешно!")
    
    except Exception as e:
        print(f" Ошибка в тестовом сценарии: {e}")

def main():
    """Основная функция программы"""
    print_header()
    
    # Создание компании
    company_name = input("Введите название транспортной компании: ").strip()
    if not company_name:
        company_name = "Моя Транспортная Компания"
    
    try:
        company = TransportCompany(company_name)
        print(f" Компания '{company_name}' создана!")
        
    except Exception as e:
        print(f" Ошибка при создании компании: {e}")
        return
    
    # Главный цикл меню
    while True:
        print_menu()
        choice = input("Выберите действие: ")
        
        if choice == "1":
            manage_clients_menu(company)
        elif choice == "2":
            manage_vehicles_menu(company)
        elif choice == "3":
            optimize_cargo_menu(company)
        elif choice == "4":
            show_statistics_menu(company)
        elif choice == "5":
            run_test_scenario()
        elif choice == "0":
            print("\nСпасибо за использование системы! До свидания!")
            break
        else:
            print(" Неверный выбор. Пожалуйста, выберите от 0 до 5.")

# Запуск основной программы
if __name__ == "__main__":
    main()