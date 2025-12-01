class TransportCompany:
    """Класс транспортной компании"""
    
    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название компании должно быть непустой строкой")
        self.name = name
        self.clients = []
        self.vehicles = []
    
    def add_client(self, client):
        self.clients.append(client)
    
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
    
    def optimize_cargo_distribution(self):
        """Упрощенная оптимизация распределения грузов"""
        # Сначала разгружаем весь транспорт
        for vehicle in self.vehicles:
            vehicle.unload_cargo()
        
        # Разделяем клиентов на VIP и обычных
        vip_clients = [c for c in self.clients if c.is_vip]
        regular_clients = [c for c in self.clients if not c.is_vip]
        
        # Сортируем транспорт по грузоподъемности (от большей к меньшей)
        sorted_vehicles = sorted(self.vehicles, key=lambda v: v.capacity, reverse=True)
        
        unloaded_vip = []
        unloaded_regular = []
        
        # Сначала загружаем VIP клиентов
        for client in vip_clients:
            loaded = False
            for vehicle in sorted_vehicles:
                if vehicle.load_cargo(client):
                    loaded = True
                    break
            if not loaded:
                unloaded_vip.append(client)
        
        # Затем загружаем обычных клиентов
        for client in regular_clients:
            loaded = False
            for vehicle in sorted_vehicles:
                if vehicle.load_cargo(client):
                    loaded = True
                    break
            if not loaded:
                unloaded_regular.append(client)
        
        # Собираем статистику
        used_vehicles = [v for v in self.vehicles if v.current_load > 0]
        total_utilization = sum(v.current_load for v in used_vehicles) / sum(v.capacity for v in used_vehicles) * 100 if used_vehicles else 0
        
        return {
            'total_clients': len(self.clients),
            'vip_clients': len(vip_clients),
            'regular_clients': len(regular_clients),
            'used_vehicles': len(used_vehicles),
            'total_vehicles': len(self.vehicles),
            'unloaded_vip': unloaded_vip,
            'unloaded_regular': unloaded_regular,
            'utilization': total_utilization
        }
    
    def clear_all_loads(self):
        for vehicle in self.vehicles:
            vehicle.unload_cargo()
    
    def __str__(self):
        return f"{self.name} | Клиенты: {len(self.clients)} | Транспорт: {len(self.vehicles)}"