from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import BotCommand

admin_commands = [
    BotCommand(command="start", description="start/restart bot"),
    BotCommand(command="edit_category", description="Edit Category"),
    BotCommand(command="delete_category", description="Delete Category"),
    BotCommand(command="add_category", description="Add new category"),
    BotCommand(command="edit_product", description="Edit Category"),
    BotCommand(command="delete_product", description="Delete Category"),
    BotCommand(command="add_product", description="Add new category"),
    BotCommand(command="categories", description="All categories"),
    BotCommand(command="products", description="All products"),
]

user_commands = [
    BotCommand(command="start", description="start/restart bot"),
    BotCommand(command="help", description="Manual for this bot"),
    BotCommand(command="categories", description="All categories"),
    BotCommand(command="products", description="All products"),
]


def make_confirm_kb():
    rows = [
        InlineKeyboardButton(text="Yes", callback_data="Yes"),
        InlineKeyboardButton(text="No", callback_data="No")
    ]
    in_kb = InlineKeyboardMarkup(
        inline_keyboard=[rows]
    )
    return in_kb
