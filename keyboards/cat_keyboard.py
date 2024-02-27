from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.database import Database


db = Database()


def make_category():
    categories = db.get_category()
    rows = []

    for cat in categories:
        rows.append(
            [InlineKeyboardButton(
                text=cat[1], callback_data=str(cat[1])
            )]
        )

    kb = InlineKeyboardMarkup(
        inline_keyboard=rows
    )

    return kb

def make_confirm():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes", callback_data="Yes"
                ),
                InlineKeyboardButton(
                    text="No", callback_data="No"
                )
            ]
        ]
    )
    return kb

def make_select(id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Edit this",
                    callback_data=f'{id}'
                )           
            ]
        ]
    )

    return kb