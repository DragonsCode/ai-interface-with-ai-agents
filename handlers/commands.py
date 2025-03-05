from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

commands_router = Router()

@commands_router.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!\nОтправляй любое сообщение – я сам определю, что тебе нужно!")