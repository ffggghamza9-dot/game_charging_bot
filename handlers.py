from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config import config
from database import db
from keyboards import keyboards
import pytz
from datetime import datetime

class Handlers:
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id
        
        # تسجيل المستخدم الجديد
        if not db.get_user(user_id):
            db.save_user(user_id, {
                "name": user.full_name,
                "username": user.username,
                "balance": 0.0,
                "joined_at": datetime.now().isoformat(),
                "is_banned": False
            })
        
        # إرسال رسالة الترحيب
        welcome_msg = self._get_welcome_message()
        await update.message.reply_text(
            welcome_msg,
            reply_markup=keyboards.main_menu(),
            parse_mode="HTML"
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        user_id = update.effective_user.id
        
        if text == "🎮 الألعاب":
            await update.message.reply_text(
                "اختر لعبة من القائمة:",
                reply_markup=keyboards.games_menu()
            )
        elif text == "📱 التطبيقات":
            await update.message.reply_text(
                "اختر تطبيق من القائمة:",
                reply_markup=keyboards.apps_menu()
            )
        elif text == "💳 رصيدي":
            user = db.get_user(user_id)
            await update.message.reply_text(
                f"رصيدك الحالي: {user.get('balance', 0)} دولار"
            )
        # ... باقي معالجات النصوص

    async def button_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        data = query.data
        
        if data.startswith("game_"):
            game_id = data.split("_")[1]
            game = db.get_services()["games"].get(game_id)
            await query.edit_message_text(
                f"<b>{game['name']}</b>\n\n"
                f"{game['description']}\n\n"
                f"السعر: {game['price']} دولار",
                reply_markup=keyboards.service_options(game_id, "game"),
                parse_mode="HTML"
            )
        # ... باقي معالجات الأزرار

    def _get_welcome_message(self) -> str:
        settings = db.get_settings()
        return settings.get("welcome_message", "مرحباً بك في بوت شحن الألعاب والتطبيقات!")

handlers = Handlers()
