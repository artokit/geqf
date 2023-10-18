from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = '6488041628:AAEh-fVs7vnR1g0GhfWSH-dlm8tEqmFjzzM'
bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())
