import json
import os
from typing import Dict, List, Any
from config import config
from datetime import datetime

class Database:
    @staticmethod
    def load_data(file_path: str) -> Dict:
        """تحميل البيانات من ملف JSON"""
        if not os.path.exists(file_path):
            return {}
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_data(file_path: str, data: Dict) -> None:
        """حفظ البيانات إلى ملف JSON"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # مستخدمون
    def get_user(self, user_id: int) -> Dict:
        users = self.load_data(config.USERS_FILE)
        return users.get(str(user_id), {}

    def save_user(self, user_id: int, user_data: Dict) -> None:
        users = self.load_data(config.USERS_FILE)
        users[str(user_id)] = user_data
        self.save_data(config.USERS_FILE, users)

    # خدمات
    def get_services(self) -> Dict:
        return self.load_data(config.SERVICES_FILE)

    def save_services(self, services: Dict) -> None:
        self.save_data(config.SERVICES_FILE, services)

    # طلبات
    def create_order(self, order_data: Dict) -> str:
        orders = self.load_data(config.ORDERS_FILE)
        order_id = str(int(datetime.now().timestamp()))
        orders[order_id] = order_data
        self.save_data(config.ORDERS_FILE, orders)
        return order_id

    def update_order(self, order_id: str, updates: Dict) -> None:
        orders = self.load_data(config.ORDERS_FILE)
        if order_id in orders:
            orders[order_id].update(updates)
            self.save_data(config.ORDERS_FILE, orders)

    # إعدادات
    def get_settings(self) -> Dict:
        return self.load_data(config.SETTINGS_FILE)

    def update_settings(self, updates: Dict) -> None:
        settings = self.load_data(config.SETTINGS_FILE)
        settings.update(updates)
        self.save_data(config.SETTINGS_FILE, settings)

db = Database()
