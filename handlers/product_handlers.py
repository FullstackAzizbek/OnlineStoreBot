from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from utils.database import Database
from states.all_states import AddProduct, ProductsState, ProductEditState
from keyboards.cat_keyboard import make_confirm, make_select
product_router = Router()
edit_product_router = Router()
db = Database()

@product_router.message(Command('add_product'))
async def product_add_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Okey, send me your product name please..."
    )
    await state.set_state(AddProduct.title_state)


@product_router.message(AddProduct.title_state, F.text)
async def product_text_handler(message: Message, state: FSMContext):
    if message.text != "":
        await state.update_data(title = message.text)
        await state.set_state(AddProduct.text_state)
        await message.answer(
            "Ok, send me your product description..."
        )
    else:
        await message.answer(
            "Please enter your product name..."
        )
        await state.set_state(AddProduct.title_state)

@product_router.message(AddProduct.text_state)
async def product_price_handler(message: Message, state: FSMContext):
    if message.text != "":
        await state.update_data(text = message.text)
        await state.set_state(AddProduct.price_state)
        await message.answer(
            "Ok, send me your product price..."
        )
    else:
        await message.answer(
            "Please enter your product description..."
        )
        await state.set_state(AddProduct.text_state)

@product_router.message(AddProduct.price_state, F.text)
async def product_category_handler(message: Message, state: FSMContext):
    if message.text != "":
        await state.update_data(price = message.text)
        await state.set_state(AddProduct.category_state)
        await message.answer(
            "Ok, send me your product category..."
        )
    else:
        await message.answer(
            "Please enter your product price..."
        )
        await state.set_state(AddProduct.price_state)

@product_router.message(AddProduct.category_state, F.text)
async def product_phone_handler(message: Message, state: FSMContext):
    if message.text != "":
        await state.update_data(category = message.text)
        await state.set_state(AddProduct.phone_state)
        await message.answer(
            "Ok, send me your phone number or contact..."
        )
    else:
        await message.answer(
            "Please enter your product category..."
        )
        await state.set_state(AddProduct.category_state)

@product_router.message(AddProduct.phone_state)
async def product_image_handler(message: Message, state: FSMContext):
    if message.text != "":
        await state.update_data(phone = message.text)
        await state.set_state(AddProduct.image_state)
        await message.answer(
            "Ok, send me your product image..."
        )
    else:
        await message.answer(
            "Please enter your phone number or contact..."
        )
        await state.set_state(AddProduct.phone_state)


@product_router.message(AddProduct.image_state)
async def image_handler(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(image=message.photo[-1].file_id)
        all_data = await state.get_data()
        await message.answer_photo(
            photo=all_data.get('image'),
            caption=f"Name: <b>{all_data.get('title')}</b>\nDescription: {all_data.get('text')}\nPrice: <i>{all_data.get('price')}$</i>\nCategory: <b>{all_data.get('category')}</b>\nPhone: <a>{all_data.get('phone')}</a>"
        )
        await message.answer(
            text="Ok, your product will be published like this, are you sure?",
            reply_markup=make_confirm()
        )
        await state.set_state(ProductsState.finish_add_product_state)

@product_router.callback_query(ProductsState.finish_add_product_state)
async def finish_add_product(callback: CallbackQuery, state: FSMContext):
    global finish_adding
    if callback.data == "Yes":
        await callback.message.delete()
        all_data = await state.get_data()
        db.add_product(
            pro_name=all_data.get('title'),
            pro_desc=all_data.get('text'),
            pro_price=all_data.get('price'),
            pro_cat=all_data.get('category'),
            pro_image=all_data.get('image'),
            pro_phone=all_data.get('phone'),
            pro_owner=callback.from_user.id  
        )
        await callback.message.answer(
            text="Your product was successfully added! 🥳🥳🥳"
        )
    else:
        await callback.message.answer(
            text="Ok, maybe next time."
        )

@product_router.message(Command("products"))
async def get_product_handler(message: Message):
    product = db.get_products(message.from_user.id)
    await message.answer(
        text="These are your products..."
    )
    for pro in product:
        await message.answer_photo(
            photo=pro[4],
            caption=f"Name: <b>{pro[0]}</b>\nDescription: {pro[1]}\nPrice: <i>{pro[2]}$</i>\nCategory: <b>{pro[3]}</b>\nPhone: <a>{pro[5]}</a>"
        )

    
@edit_product_router.message(Command("edit_product"))
async def edit_product_handler(message: Message):
    await message.answer(
        text="Please select product which you want and click 'Edit this' button for edit..."
    )

    product = db.get_products(message.from_user.id)

    for pro in product:
        await message.answer_photo(
            photo=pro[4],
            caption=f"Name: <b>{pro[0]}</b>\nDescription: {pro[1]}\nPrice: <i>{pro[2]}$</i>\nCategory: <b>{pro[3]}</b>\nPhone: <a>{pro[5]}</a>",
            reply_markup=make_select(pro[6])
        )
        
    
@edit_product_router.callback_query(CallbackQuery)
async def edit_select_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProductEditState.title_edit_state)
    await callback.message.answer(
        text="Please enter new name..."
    )

@edit_product_router.message(ProductEditState.title_edit_state)
async def edit_title_handler(message: Message, state: FSMContext):
    await state.update_data(edit_title = message.text)
    await state.set_state(ProductEditState.text_edit_state)
    await message.answer(
        text="Please enter new description..."
    )

@edit_product_router.message(ProductEditState.text_edit_state)
async def edit_text_handler(message: Message, state: FSMContext):
    await state.update_data(edit_text = message.text)
    await state.set_state(ProductEditState.price_edit_state)
    await message.answer(
        text="Please enter new price..."
    )

@edit_product_router.message(ProductEditState.price_edit_state)
async def edit_price_handler(message: Message, state: FSMContext):
    await state.update_data(edit_price = message.text)
    await state.set_state(ProductEditState.category_edit_state)
    await message.answer(
        text="Please enter new category name..."
    )

@edit_product_router.message(ProductEditState.category_edit_state)
async def edit_category_handler(message: Message, state: FSMContext):
    await state.update_data(edit_category = message.text)
    await state.set_state(ProductEditState.image_edit_state)
    await message.answer(
        text="Please enter new image..."
    )

@edit_product_router.message(ProductEditState.image_edit_state)
async def edit_image_handler(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(edit_image = message.photo[-1].file_id)
        await state.set_state(ProductEditState.phone_edit_state)
        await message.answer(
            text="Please enter new phone number..."
        )
    else:
        await message.answer(
            text="Please send only image..."
        )
        await state.set_state(ProductEditState.image_edit_state)

@edit_product_router.message(ProductEditState.phone_edit_state)
async def phone_edit_handler(message: Message, state: FSMContext):
    await state.update_data(edit_phone = message.text)
    all_data = await state.get_data()
    await db.get_edit_product(
        product_name=all_data.get('edit_title'),
        product_desc=all_data.get('edit_text'),
        product_price=all_data.get('edit_price'),
        product_category=all_data.get('edit_category'),
        product_image=all_data.get('edit_image'),
        phone=all_data.get('edit_phone'),
        id=message.from_user.id
    )
