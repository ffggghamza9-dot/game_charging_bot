import os
from typing import Dict, Any

class Config:
    # إعدادات البوت الأساسية
    TOKEN = os.getenv("8168891066:AAEO5G1AGN2YNg1Hz_z4iG_iVdfm5bfgiwo")
    ADMIN_IDS = [7944027261]  # قائمة بأيدي المشرفين
    PAYMENT_METHODS = {
        "paypal": {"fee": 0.05, "active": True},
        "credit_card": {"fee": 0.03, "active": True},
        "bank_transfer": {"fee": 0.02, "active": True}
    }
    EXCHANGE_RATE = 50.0  # سعر الصرف الافتراضي
    TIMEZONE = "Asia/Damascus"  # توقيت سوريا
    
    # إعدادات لوحة التحكم
    ADMIN_PASSWORD = "secure_password_123"
    
    # مسارات الملفات
    DATA_PATH = "data/"
    USERS_FILE = DATA_PATH + "users.json"
    SERVICES_FILE = DATA_PATH + "services.json"
    ORDERS_FILE = DATA_PATH + "orders.json"
    SETTINGS_FILE = DATA_PATH + "settings.json"

config = Config()
