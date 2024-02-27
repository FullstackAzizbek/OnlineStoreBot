from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router
from utils.database import Database
from keyboards.cat_keyboard import make_category
from aiogram.fsm.context import FSMContext
from states.all_states import CategoryState
from all_commands import make_confirm_kb

category_router = Router()
db = Database()


@category_router.message(Command('categories'))
async def get_categories(message: Message):
    await message.answer(text="Select Categories above:\n",
                         reply_markup=make_category())


@category_router.message(Command("add_category"))
async def add_category(message: Message, state: FSMContext):
    await state.set_state(CategoryState.add_state)
    await message.answer(text="Please, Enter the new category name....")


@category_router.message(CategoryState.add_state)
async def insert_category_handler(message: Message, state: FSMContext):
    status = db.check_category_exists(message.text)
    if status == True:
        db.add_category(new_category=message.text)
        await state.clear()
        await message.answer(f"New category by name '{message.text}' added successfully 👍👍👍")
    else:
        await message.answer("Something went wrong. Please send other name or click /cancel.")
        await state.set_state(CategoryState.add_state)


@category_router.message(Command("delete_category"))
async def del_category(message: Message, state: FSMContext):
    await state.set_state(CategoryState.del_state)
    await message.answer(
        text="O'chirmoqchi bo'lgan kategoriyani tanlang: ",
        reply_markup=make_category()
    )


@category_router.callback_query(CategoryState.del_state)
async def del_state_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CategoryState.finish_delete)
    await state.update_data(cat_name=callback.data)
    await callback.message.edit_text(
        text=f"{callback.data} ni o'chirmoqchimisiz? ",
        reply_markup=make_confirm_kb()
    )


@category_router.callback_query(CategoryState.finish_delete)
async def remove_state_handler(callback: CallbackQuery, state: FSMContext):
    if callback.data == "Yes":
        all_data = await state.get_data()
        delete_result = db.del_category(all_data.get('cat_name'))

        if delete_result:
            await callback.message.answer("Kategoriya muvaffaqiyatli o'chirildi 👍👍👍")
            await callback.message.delete()
            await state.clear()
        else:
            await callback.message.answer(
                "Nimadir noto'g'ri ketdi. Iltimos, boshqa nom yuboring yoki /cancel tugmasini bosing.")
    else:
        await state.clear()
        await callback.message.answer("Jarayon bekor qilindi.")
        await callback.message.delete()


@category_router.message(Command("edit_category"))
async def edit_handler(message: Message, state: FSMContext):
    await state.set_state(CategoryState.edit_state)
    await message.answer("Select category for change name...", reply_markup=make_category())


@category_router.callback_query(CategoryState.edit_state)
async def edit_category_state_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_name=callback.data)
    await state.set_state(CategoryState.finishEditState)
    await callback.message.edit_text(
        text="Yangi nom kiriting..."
    )


@category_router.message(CategoryState.finishEditState)
async def finish_edit_handler(message: Message, state: FSMContext):
    all_data = await state.get_data()
    status = db.check_category_exists(message.text)
    if status == True and all_data.get('edit_name') != '':
        db.update_category(message.text, all_data.get('edit_name'))
        await message.answer("Edit name successfully 👍👍👍")
        await message.delete()
        await state.clear()
    else:
        await message.answer("Something went wrong. Please send other name or click /cancel.")
        await state.set_state(CategoryState.finishEditState)
