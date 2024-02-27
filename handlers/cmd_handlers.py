from config import admins
from all_commands import admin_commands, user_commands
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router
from utils.database import Database
from aiogram.fsm.context import FSMContext

command_router = Router()
db = Database()


@command_router.message(CommandStart())
async def start_handler(message: Message):
    if message.from_user.id in admins:
        await message.bot.set_my_commands(commands=admin_commands)
        await message.answer(text="Dear admin, Welcome!")
    else:
        await message.bot.set_my_commands(commands=user_commands)
        await message.answer(text="Welcome.")


@command_router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("All actions canceled")
