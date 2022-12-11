from loader import bot
import loader
import handlers
import admin
import reserve




bot.polling(non_stop=True, interval=0, skip_pending=True)