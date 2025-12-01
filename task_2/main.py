# Николай Козик
# Вариант: 4
# Задание 2: Базовый класс Vehicle

import uuid
from task_1.main import Client

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


# Демонстрация работы
if __name__ == "__main__":
    print("=" * 50)
    print("ЗАДАНИЕ 2: Базовый класс Vehicle")
    print("=" * 50)
    
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
        print(f"Загрузка {client1.name}: {' Успешно' if result1 else ' Не удалось'}")
        
        result2 = vehicle.load_cargo(client2)
        print(f"Загрузка {client2.name}: {' Успешно' if result2 else ' Не удалось'}")
        
        print(f"\nПосле загрузки: {vehicle}")
        print(f"Клиенты в транспорте: {len(vehicle.clients_list)}")
        
        # Проверка перегрузки
        client3 = Client("Тяжелый Клиент", 5.0)
        result3 = vehicle.load_cargo(client3)
        print(f"\nПопытка загрузки {client3.name}: {' Успешно' if result3 else ' Не удалось (нет места)'}")
        
        print("\n Задание 2 выполнено успешно!")
        
    except Exception as e:
        print(f" Ошибка: {e}")