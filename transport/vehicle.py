import uuid

class Vehicle:
    """Базовый класс транспортного средства"""
    
    def __init__(self, capacity: float, vehicle_type: str = "Грузовик"):
        self.validate_capacity(capacity)
        self.vehicle_id = str(uuid.uuid4())[:8]
        self.capacity = capacity
        self.vehicle_type = vehicle_type
        self.current_load = 0.0
        self.clients_list = []
    
    def validate_capacity(self, capacity: float):
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Грузоподъемность должна быть положительным числом")
    
    def load_cargo(self, client):
        if client.cargo_weight <= (self.capacity - self.current_load):
            self.current_load += client.cargo_weight
            self.clients_list.append(client)
            return True
        return False
    
    def unload_cargo(self):
        self.current_load = 0.0
        self.clients_list.clear()
    
    def get_available(self):
        return self.capacity - self.current_load
    
    def __str__(self):
        return f"{self.vehicle_type} {self.vehicle_id} | Груз: {self.current_load:.1f}/{self.capacity:.1f} кг"
    
    def to_dict(self):
        return {
            'vehicle_id': self.vehicle_id,
            'capacity': self.capacity,
            'vehicle_type': self.vehicle_type,
            'current_load': self.current_load,
            'available': self.get_available(),
            'clients': [c.name for c in self.clients_list]
        }