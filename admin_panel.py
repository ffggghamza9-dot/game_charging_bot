from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config import config
from database import db
from keyboards import keyboards

class AdminPanel:
    async def admin_login(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id not in config.ADMIN_IDS:
            await update.message.reply_text("ليس لديك صلاحية الدخول إلى لوحة التحكم.")
            return
        
        await update.message.reply_text(
            "أدخل كلمة مرور المشرف:",
            reply_markup=keyboards.cancel_keyboard()
        )
        return "WAIT_PASSWORD"

    async def verify_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == config.ADMIN_PASSWORD:
            await update.message.reply_text(
                "تم الدخول بنجاح إلى لوحة التحكم.",
                reply_markup=keyboards.admin_menu()
            )
            return ConversationHandler.END
        else:
            await update.message.reply_text("كلمة المرور خاطئة، حاول مرة أخرى.")
            return "WAIT_PASSWORD"

    async def manage_services(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.edit_message_text(
            "إدارة الخدمات والأقسام:",
            reply_markup=keyboards.manage_services_menu()
        )

    # ... باقي وظائف لوحة التحكم

admin_panel = AdminPanel()
