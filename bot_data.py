from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

admin_chat = "" 	# "@name"
admin_id = 1  		# 1111111111
group_link = ""  	# "https://t.me/name"
token = ""  		# "4534536:dfsaastrastscfvcxzvxzearaev"
qiwi_token = ""  	# "7sazaa0sd7807adsg="
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)