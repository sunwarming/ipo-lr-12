# Николай Козик

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


# Демонстрация работы
if __name__ == "__main__":
    print("=" * 50)
    print("ЗАДАНИЕ 1: Класс Client")
    print("=" * 50)
    
    # Создание клиентов
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
        
        print("\n Задание 1 выполнено успешно!")
        
    except Exception as e:
        print(f" Ошибка: {e}")