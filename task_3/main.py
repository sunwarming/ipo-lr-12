# Николай Козик
# Вариант: 4

import uuid
from task_1.main import Client
from task_2.main import Vehicle

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


# Демонстрация работы
if __name__ == "__main__":
    print("=" * 50)
    print("ЗАДАНИЕ 3: Классы Airplane, Van, TransportCompany")
    print("=" * 50)
    
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
        
        print("\n Задание 3 выполнено успешно!")
        
    except Exception as e:
        print(f" Ошибка: {e}")