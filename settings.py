from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = '6546493942:AAHfCLtAxsHiNNDiurBlS_XDpKtKtx8Csd0'
bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())
