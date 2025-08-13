from telegram import Update
from telegram.ext import ContextTypes
from config import config
from database import db
from keyboards import keyboards
import pytz

class PaymentSystem:
    async def handle_payment_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        photo = update.message.photo[-1]  # أعلى دقة
        
        # حفظ صورة التحويل
        file = await photo.get_file()
        file_path = f"payments/{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        await file.download_to_drive(file_path)
        
        # إرسال إشعار للمستخدم
        damascus_time = datetime.now(pytz.timezone(config.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")
        await update.message.reply_text(
            f"تم تثبيت طلب شحن البوت بنجاح في الساعة {damascus_time} ✅\n"
            "الرجاء الانتظار حوالي 5 دقائق وحتى ساعتين ليتم التحقق من عملية التحويل "
            "وإضافة الرصيد لحسابك ⏱️"
        )
        
        # إعلام المشرفين
        for admin_id in config.ADMIN_IDS:
            await context.bot.send_photo(
                chat_id=admin_id,
                photo=photo.file_id,
                caption=f"طلب دفع جديد من المستخدم {user_id}"
            )

    async def confirm_payment(self, update: Update, context: ContextTypes.DEFAULT_TYPE, order_id: str):
        db.update_order(order_id, {"status": "completed"})
        user_id = db.get_order(order_id)["user_id"]
        amount = db.get_order(order_id)["amount"]
        
        # تحديث رصيد المستخدم
        user = db.get_user(user_id)
        user["balance"] = user.get("balance", 0) + amount
        db.save_user(user_id, user)
        
        # إرسال إشعار للمستخدم
        await context.bot.send_message(
            chat_id=user_id,
            text=f"تم تأكيد دفعتك وتم إضافة {amount} دولار إلى رصيدك."
        )

payment_system = PaymentSystem()
