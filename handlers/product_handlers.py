from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command
from utils.database import Database
from states.all_states import AddProduct, ProductsState
from unidecode import unidecode

from keyboards.cat_keyboard import make_confirm, make_pagination, make_category_2
product_router = Router()
edit_product_router = Router()
db = Database()

@product_router.message(Command('add_product'))
async def product_add_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Okey, choose the category...",
        reply_markup=make_category_2()
    )
    await state.set_state(AddProduct.category_state)

@product_router.callback_query(AddProduct.category_state)
async def product_category_handler(query: CallbackQuery, state: FSMContext):
    category = query.data
    if category:
        await query.message.delete()
        await state.update_data(category=category)
        await state.set_state(AddProduct.title_state)
        await query.message.answer(text="Ok, send me your product name please...")
    else:
        await query.message.answer("Please enter your product category...")
        await state.set_state(AddProduct.category_state)

@product_router.message(AddProduct.title_state)
async def product_title_handler(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await state.set_state(AddProduct.text_state)
    await message.answer(
        text="Ok, send me your product description..."
    )


@product_router.message(AddProduct.text_state)
async def product_desc_handler(message: Message, state: FSMContext):
    await state.update_data(text = message.text)
    await state.set_state(AddProduct.price_state)
    await message.answer(
        text="Ok, send me your product price..."
    )

@product_router.message(AddProduct.price_state, F.text)
async def product_price_handler(message: Message, state: FSMContext):
    if message.text != "":
        await state.update_data(price = message.text)
        await state.set_state(AddProduct.phone_state)
        await message.answer(
            "Ok, send me your phone number or contact please..."
        )
    else:
        await message.answer(
            "Please enter your product price..."
        )
        await state.set_state(AddProduct.price_state)

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
async def get_product_handler(message: Message, state: FSMContext):
    products = db.get_products(message.from_user.id)
    
    await message.answer(
        text="These are your products..."
    )
    if len(products) == 1:
        product = products[0]
        await message.answer_photo(
            photo=product[4],
            caption=f"Name: <b>{product[0]}</b>\nDescription: {product[1]}\nPrice: <i>{product[2]}$</i>\nCategory: <b>{product[3]}</b>\nPhone: <a>{product[5]}</a>",
            reply_markup=make_pagination()
        ) 
    else:
        product = products[0]
        await state.update_data(index = 0)
        await state.update_data(products=products)
        await state.update_data()
        await message.answer_photo(
            photo=product[4],
            caption=f"Name: <b>{product[0]}</b>\nDescription: {product[1]}\nPrice: <i>{product[2]}$</i>\nCategory: <b>{product[3]}</b>\nPhone: <a>{product[5]}</a>",
            reply_markup=make_pagination()
        )
        await state.set_state(ProductsState.get_product_state)

@product_router.callback_query(ProductsState.get_product_state)
async def get_product_page(query: CallbackQuery, state: FSMContext):
    all_data = await state.get_data()

    index = all_data.get('index')
    products = all_data.get('products')
    count = len(products)

    if query.data == "next":
        if index == count - 1:
            index = 0
        else:
            index += 1
    else:
        if index == 0:
            index = count - 1
        else:
            index -= 1

    await state.update_data(index=index)
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=products[index][4],
            caption=f"Name: <b>{products[index][0]}</b>\nDescription: {products[index][1]}\nPrice: <i>{products[index][2]}$</i>\nCategory: <b>{products[index][3]}</b>\nPhone: <a>{products[index][5]}</a>",
        ),
        reply_markup=make_pagination()
    )
    state.clear()

@product_router.message(F.text)
async def search_handler(message: Message, state: FSMContext):
    text = message.text
    products = db.search_product(unidecode(text))
    await state.update_data(products=products)
    all_data = await state.get_data()
    count = len(all_data.get('products'))
    await state.update_data(index = 0)
    

    if count > 0 and count is not None:
        if count == 1:
            await message.answer_photo(
                photo=products[0][4],
                caption=f"Name: <b>{products[0][0]}</b>\nDescription: {products[0][1]}\nPrice: <i>{products[0][2]}$</i>\nCategory: <b>{products[0][3]}</b>\nPhone: <a>{products[0][5]}</a>",
            )
        elif count > 1:
            await state.set_state(ProductsState.search_state)
            await message.answer_photo(
                photo=products[0][4],
                caption=f"Name: <b>{products[0][0]}</b>\nDescription: {products[0][1]}\nPrice: <i>{products[0][2]}$</i>\nCategory: <b>{products[0][3]}</b>\nPhone: <a>{products[0][5]}</a>",
                reply_markup=make_pagination()
            )
    else:
        await message.answer("No products found.")

@product_router.callback_query(ProductsState.search_state)
async def search_products_handler(query: CallbackQuery, state: FSMContext):
    
    all_data = await state.get_data()

    index = all_data.get('index')
    products = all_data.get('products')
    count = len(products)

    if query.data == "next":
        if index == count - 1:
            index = 0
        else:
            index += 1
    elif query.data == "prev":  
        if index == 0:
            index = count - 1
        else:
            index -= 1

    await state.update_data(index=index)
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=products[index][4],
            caption=f"Name: <b>{products[index][0]}</b>\nDescription: {products[index][1]}\nPrice: <i>{products[index][2]}$</i>\nCategory: <b>{products[index][3]}</b>\nPhone: <a>{products[index][5]}</a>",
        ),
        reply_markup=make_pagination()
    )
