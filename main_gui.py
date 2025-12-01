import dearpygui.dearpygui as dpg
import json
import os
from transport.client import Client
from transport.vehicle import Vehicle
from transport.airplane import Airplane
from transport.van import Van
from transport.company import TransportCompany


class TransportGUI:
    def __init__(self):
        self.company = None
        self.vehicles_data = []
        self.clients_data = []
        
    def run(self):
        dpg.create_context()
        dpg.create_viewport(title='Transport Company Management', width=1200, height=800)
        self.setup_gui()
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
    
    def setup_gui(self):
        # Создание окон и элементов интерфейса
        self.setup_main_window()
        self.setup_vehicles_window()
        self.setup_clients_window()
        self.setup_modals()
    
    def setup_main_window(self):
        with dpg.window(label="Main Window", tag="main_window", width=1200, height=800):
            dpg.add_text("Transport Company Management System", color=[255, 255, 0])
            dpg.add_separator()
            
            dpg.add_button(label="Manage Vehicles", callback=lambda: dpg.show_item("vehicles_window"))
            dpg.add_button(label="Manage Clients", callback=lambda: dpg.show_item("clients_window"))
            dpg.add_button(label="Optimize Distribution", callback=self.optimize_distribution)
            dpg.add_button(label="Show Statistics", callback=self.show_statistics)
            dpg.add_button(label="Save Data", callback=self.save_data)
            dpg.add_button(label="Load Data", callback=self.load_data)
    
    def setup_vehicles_window(self):
        with dpg.window(label="Vehicles Management", tag="vehicles_window", width=600, height=400, show=False):
            dpg.add_text("Vehicles Management")
            dpg.add_separator()
            
            # Форма добавления транспорта
            with dpg.group(horizontal=True):
                dpg.add_text("Vehicle Type:")
                dpg.add_combo(["Airplane", "Van"], tag="vehicle_type", default_value="Airplane")
            
            with dpg.group(horizontal=True):
                dpg.add_text("Capacity (kg):")
                dpg.add_input_float(tag="vehicle_capacity", default_value=1000.0, step=100.0)
            
            with dpg.group(horizontal=True):
                dpg.add_text("Additional:")
                dpg.add_input_float(tag="max_altitude", default_value=10000.0, show=True)
                dpg.add_checkbox(label="Refrigerated", tag="is_refrigerated", show=False)
            
            dpg.add_button(label="Add Vehicle", callback=self.add_vehicle)
            dpg.add_separator()
            
            # Список транспорта
            dpg.add_text("Vehicle List:")
            self.vehicle_list = dpg.add_listbox(tag="vehicle_list", items=[], num_items=10)
    
    def setup_clients_window(self):
        with dpg.window(label="Clients Management", tag="clients_window", width=600, height=400, show=False):
            dpg.add_text("Clients Management")
            dpg.add_separator()
            
            # Форма добавления клиента
            with dpg.group(horizontal=True):
                dpg.add_text("Name:")
                dpg.add_input_text(tag="client_name", width=200)
            
            with dpg.group(horizontal=True):
                dpg.add_text("Cargo Weight (kg):")
                dpg.add_input_float(tag="client_weight", default_value=100.0, step=10.0)
            
            dpg.add_checkbox(label="VIP Client", tag="client_vip")
            dpg.add_button(label="Add Client", callback=self.add_client)
            dpg.add_separator()
            
            # Список клиентов
            dpg.add_text("Client List:")
            self.client_list = dpg.add_listbox(tag="client_list", items=[], num_items=10)
    
    def setup_modals(self):
        # Модальные окна для редактирования
        with dpg.window(label="Edit Vehicle", tag="edit_vehicle_modal", width=400, height=300, show=False, modal=True):
            dpg.add_text("Edit Vehicle", color=[0, 255, 255])
            dpg.add_input_text(tag="edit_vehicle_id", label="Vehicle ID", readonly=True)
            dpg.add_input_float(tag="edit_vehicle_capacity", label="Capacity (kg)")
            dpg.add_button(label="Save Changes", callback=self.save_vehicle)  # Вот здесь используется save_vehicle
            dpg.add_button(label="Cancel", callback=lambda: dpg.hide_item("edit_vehicle_modal"))
    
    # ДОБАВЛЕННЫЙ МЕТОД - который отсутствовал
    def save_vehicle(self):
        """Сохранить изменения транспортного средства"""
        try:
            vehicle_id = dpg.get_value("edit_vehicle_id")
            new_capacity = dpg.get_value("edit_vehicle_capacity")
            
            # Найти и обновить транспорт
            for vehicle in self.vehicles_data:
                if vehicle.get('vehicle_id') == vehicle_id:
                    vehicle['capacity'] = new_capacity
                    break
            
            self.update_vehicle_list()
            dpg.hide_item("edit_vehicle_modal")
            
        except Exception as e:
            print(f"Error saving vehicle: {e}")
    
    def add_vehicle(self):
        vehicle_type = dpg.get_value("vehicle_type")
        capacity = dpg.get_value("vehicle_capacity")
        
        if vehicle_type == "Airplane":
            max_altitude = dpg.get_value("max_altitude")
            vehicle = Airplane(capacity, max_altitude)
        else:  # Van
            is_refrigerated = dpg.get_value("is_refrigerated")
            vehicle = Van(capacity, is_refrigerated)
        
        self.vehicles_data.append({
            'vehicle_id': vehicle.vehicle_id,
            'type': vehicle_type,
            'capacity': capacity,
            'max_altitude': max_altitude if vehicle_type == "Airplane" else None,
            'is_refrigerated': is_refrigerated if vehicle_type == "Van" else None,
            'object': vehicle
        })
        
        self.update_vehicle_list()
    
    def add_client(self):
        name = dpg.get_value("client_name")
        weight = dpg.get_value("client_weight")
        is_vip = dpg.get_value("client_vip")
        
        if not name:
            print("Please enter client name")
            return
        
        client = Client(name, weight, is_vip)
        self.clients_data.append({
            'name': name,
            'weight': weight,
            'vip': is_vip,
            'object': client
        })
        
        self.update_client_list()
        dpg.set_value("client_name", "")
    
    def update_vehicle_list(self):
        items = []
        for v in self.vehicles_data:
            if v['type'] == "Airplane":
                items.append(f"Airplane {v['vehicle_id']} - {v['capacity']} kg, Alt: {v['max_altitude']} m")
            else:
                fridge = "Refrigerated" if v['is_refrigerated'] else "Non-refrigerated"
                items.append(f"Van {v['vehicle_id']} - {v['capacity']} kg, {fridge}")
        
        dpg.configure_item("vehicle_list", items=items)
    
    def update_client_list(self):
        items = []
        for c in self.clients_data:
            vip_status = "VIP" if c['vip'] else "Regular"
            items.append(f"{c['name']} - {c['weight']} kg ({vip_status})")
        
        dpg.configure_item("client_list", items=items)
    
    def optimize_distribution(self):
        # Создаем компанию и добавляем данные
        if not self.company:
            self.company = TransportCompany("GUI Company")
        
        # Добавляем транспорт
        for v in self.vehicles_data:
            self.company.add_vehicle(v['object'])
        
        # Добавляем клиентов
        for c in self.clients_data:
            self.company.add_client(c['object'])
        
        # Оптимизируем
        result = self.company.optimize_cargo_distribution()
        
        # Показываем результаты
        with dpg.window(label="Optimization Results", width=500, height=400, modal=True):
            dpg.add_text(f"Total Clients: {result['total_clients']}")
            dpg.add_text(f"VIP Clients: {result['vip_clients']}")
            dpg.add_text(f"Regular Clients: {result['regular_clients']}")
            dpg.add_text(f"Used Vehicles: {result['used_vehicles']}/{result['total_vehicles']}")
            dpg.add_text(f"Utilization: {result['utilization']:.1f}%")
            
            if result['unloaded_vip']:
                dpg.add_text("Unloaded VIP Clients:")
                for client in result['unloaded_vip']:
                    dpg.add_text(f"  • {client.name} ({client.cargo_weight} kg)")
            
            if result['unloaded_regular']:
                dpg.add_text("Unloaded Regular Clients:")
                for client in result['unloaded_regular']:
                    dpg.add_text(f"  • {client.name} ({client.cargo_weight} kg)")
    
    def show_statistics(self):
        if not self.company:
            self.company = TransportCompany("GUI Company")
        
        total_vehicles = len(self.vehicles_data)
        total_clients = len(self.clients_data)
        
        with dpg.window(label="Statistics", width=400, height=300, modal=True):
            dpg.add_text(f"Total Vehicles: {total_vehicles}")
            dpg.add_text(f"Total Clients: {total_clients}")
            
            if total_vehicles > 0:
                airplanes = len([v for v in self.vehicles_data if v['type'] == "Airplane"])
                vans = len([v for v in self.vehicles_data if v['type'] == "Van"])
                dpg.add_text(f"Airplanes: {airplanes}")
                dpg.add_text(f"Vans: {vans}")
    
    def save_data(self):
        """Сохранить все данные в файл"""
        data = {
            'vehicles': self.vehicles_data,
            'clients': self.clients_data
        }
        
        with open('transport_data.json', 'w') as f:
            # Убираем объекты перед сохранением
            save_data = {
                'vehicles': [],
                'clients': []
            }
            
            for v in self.vehicles_data:
                vehicle_dict = {k: v for k, v in v.items() if k != 'object'}
                save_data['vehicles'].append(vehicle_dict)
            
            for c in self.clients_data:
                client_dict = {k: v for k, v in c.items() if k != 'object'}
                save_data['clients'].append(client_dict)
            
            json.dump(save_data, f, indent=2)
        
        print("Data saved to transport_data.json")
    
    def load_data(self):
        """Загрузить данные из файла"""
        if not os.path.exists('transport_data.json'):
            print("No data file found")
            return
        
        with open('transport_data.json', 'r') as f:
            data = json.load(f)
        
        # Загружаем транспорт
        self.vehicles_data = []
        for v in data['vehicles']:
            if v['type'] == "Airplane":
                vehicle = Airplane(v['capacity'], v['max_altitude'])
                vehicle.vehicle_id = v['vehicle_id']
            else:
                vehicle = Van(v['capacity'], v['is_refrigerated'])
                vehicle.vehicle_id = v['vehicle_id']
            
            self.vehicles_data.append({
                'vehicle_id': vehicle.vehicle_id,
                'type': v['type'],
                'capacity': v['capacity'],
                'max_altitude': v.get('max_altitude'),
                'is_refrigerated': v.get('is_refrigerated'),
                'object': vehicle
            })
        
        # Загружаем клиентов
        self.clients_data = []
        for c in data['clients']:
            client = Client(c['name'], c['weight'], c['vip'])
            self.clients_data.append({
                'name': c['name'],
                'weight': c['weight'],
                'vip': c['vip'],
                'object': client
            })
        
        self.update_vehicle_list()
        self.update_client_list()
        print("Data loaded from transport_data.json")


if __name__ == "__main__":
    app = TransportGUI()
    app.run()