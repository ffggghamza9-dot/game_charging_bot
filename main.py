import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from config import config
from handlers import handlers
from admin_panel import admin_panel
from payment_system import payment_system

# إعدادات التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    # إنشاء تطبيق البوت
    application = Application.builder().token(config.TOKEN).build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_message))
    application.add_handler(CallbackQueryHandler(handlers.button_click))
    
    # معالجات الدفع
    application.add_handler(MessageHandler(filters.PHOTO, payment_system.handle_payment_photo))
    
    # لوحة التحكم الإدارية
    admin_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("admin", admin_panel.admin_login)],
        states={
            "WAIT_PASSWORD": [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_panel.verify_password)]
        },
        fallbacks=[CommandHandler("cancel", admin_panel.cancel)]
    )
    application.add_handler(admin_conv_handler)
    
    # تشغيل البوت
    application.run_polling()

if __name__ == "__main__":
    main()
