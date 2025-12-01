from transport.vehicle import Vehicle

class Van(Vehicle):
    """Класс фургона, наследующий от Vehicle"""
    
    def __init__(self, capacity: float, is_refrigerated: bool = False):
        super().__init__(capacity, "Фургон")
        self.is_refrigerated = is_refrigerated
    
    def __str__(self):
        base = super().__str__()
        fridge = "с холодильником" if self.is_refrigerated else "без холодильника"
        return f"{base} | {fridge}"
    
    def to_dict(self):
        data = super().to_dict()
        data['is_refrigerated'] = self.is_refrigerated
        return data