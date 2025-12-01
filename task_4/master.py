# Николай Козик

import sys
import os

# Добавляем пути для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'task_1'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'task_2'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'task_3'))

from task_1.main import Client
from task_2.main import Vehicle
from task_3.main import Airplane, Van, TransportCompany

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
        
        print("\n Тестовый сценарий выполнен успешно!")
    
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

if __name__ == "__main__":
    main()