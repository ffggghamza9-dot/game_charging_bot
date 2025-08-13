from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from config import config
from database import db

class Keyboards:
    def __init__(self):
        self.services = db.get_services()
        self.settings = db.get_settings()

    def main_menu(self) -> ReplyKeyboardMarkup:
        """لوحة المفاتيح الرئيسية أسفل الشات"""
        buttons = [
            [KeyboardButton("🎮 الألعاب")],
            [KeyboardButton("📱 التطبيقات")],
            [KeyboardButton("💳 رصيدي"), KeyboardButton("🛒 طلباتي")],
            [KeyboardButton("ℹ️ المساعدة"), KeyboardButton("📞 التواصل")]
        ]
        return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    def games_menu(self) -> InlineKeyboardMarkup:
        """قائمة الألعاب"""
        games = self.services.get("games", {})
        buttons = []
        for game_id, game in games.items():
            buttons.append([InlineKeyboardButton(game["name"], callback_data=f"game_{game_id}")])
        buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
        return InlineKeyboardMarkup(buttons)

    def apps_menu(self) -> InlineKeyboardMarkup:
        """قائمة التطبيقات"""
        apps = self.services.get("apps", {})
        buttons = []
        for app_id, app in apps.items():
            buttons.append([InlineKeyboardButton(app["name"], callback_data=f"app_{app_id}")])
        buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
        return InlineKeyboardMarkup(buttons)

    def service_options(self, service_id: str, service_type: str) -> InlineKeyboardMarkup:
        """خيارات الخدمة"""
        buttons = [
            [InlineKeyboardButton("🛒 طلب الآن", callback_data=f"order_{service_type}_{service_id}")],
            [InlineKeyboardButton("🔙 رجوع", callback_data=f"{service_type}_menu")]
        ]
        return InlineKeyboardMarkup(buttons)

    def payment_methods(self) -> InlineKeyboardMarkup:
        """وسائل الدفع"""
        buttons = []
        for method, details in config.PAYMENT_METHODS.items():
            if details["active"]:
                buttons.append([InlineKeyboardButton(
                    f"{method.upper()} (+{details['fee']*100}%)", 
                    callback_data=f"pay_{method}"
                )])
        buttons.append([InlineKeyboardButton("🔙 إلغاء", callback_data="cancel_payment")])
        return InlineKeyboardMarkup(buttons)

    def admin_menu(self) -> InlineKeyboardMarkup:
        """لوحة التحكم الإدارية"""
        buttons = [
            [InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")],
            [InlineKeyboardButton("📝 إدارة الخدمات", callback_data="admin_services")],
            [InlineKeyboardButton("💳 إدارة المدفوعات", callback_data="admin_payments")],
            [InlineKeyboardButton("👤 إدارة المستخدمين", callback_data="admin_users")],
            [InlineKeyboardButton("⚙️ الإعدادات", callback_data="admin_settings")]
        ]
        return InlineKeyboardMarkup(buttons)

keyboards = Keyboards()
