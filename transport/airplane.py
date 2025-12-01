from transport.vehicle import Vehicle

class Airplane(Vehicle):
    """Класс самолета, наследующий от Vehicle"""
    
    def __init__(self, capacity: float, max_altitude: float):
        super().__init__(capacity, "Самолет")
        self.max_altitude = max_altitude
    
    def __str__(self):
        base = super().__str__()
        return f"{base} | Макс. высота: {self.max_altitude} м"
    
    def to_dict(self):
        data = super().to_dict()
        data['max_altitude'] = self.max_altitude
        return data