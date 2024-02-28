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

def make_category_2():
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

def make_pagination():
    pagination = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data="prev"
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data="next"
                )
            ]
        ]
    )
    return pagination