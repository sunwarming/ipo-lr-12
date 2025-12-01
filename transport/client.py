class Client:
    """Класс для представления клиента компании"""
    
    def __init__(self, name: str, cargo_weight: float, is_vip: bool = False):
        self.validate_data(name, cargo_weight, is_vip)
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip
    
    def validate_data(self, name: str, cargo_weight: float, is_vip: bool):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя клиента должно быть непустой строкой")
        if len(name.strip()) < 2:
            raise ValueError("Имя должно содержать минимум 2 символа")
        if not name.replace(" ", "").isalpha():
            raise ValueError("Имя должно содержать только буквы")
        
        if not isinstance(cargo_weight, (int, float)) or cargo_weight <= 0:
            raise ValueError("Вес груза должен быть положительным числом")
        if cargo_weight > 10000:
            raise ValueError("Вес груза не может превышать 10000 кг")
        
        if not isinstance(is_vip, bool):
            raise ValueError("VIP статус должен быть булевым значением")
    
    def __str__(self):
        vip_status = "VIP" if self.is_vip else "Обычный"
        return f"{self.name} | {self.cargo_weight} кг | {vip_status}"
    
    def to_dict(self):
        return {
            'name': self.name,
            'cargo_weight': self.cargo_weight,
            'is_vip': self.is_vip
        }