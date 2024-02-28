from aiogram.fsm.state import State, StatesGroup


class CategoryState(StatesGroup):
    edit_state = State()
    finishEditState = State()
    del_state = State()
    finish_delete = State()
    add_state = State()

class ProductsState(StatesGroup):
    add_product_state = State()
    finish_add_product_state = State()
    edit_product_state = State()
    finish_edit_product_state = State()
    delete_product_state = State()
    finish_delete_product_state = State()
    get_product_state = State()
    search_state = State()

class AddProduct(StatesGroup):
    title_state = State()
    text_state = State()
    price_state = State()
    image_state = State()
    category_state = State()
    phone_state = State()


class ProductEditState(StatesGroup):
    title_edit_state = State()
    text_edit_state = State()
    price_edit_state = State()
    image_edit_state = State()
    category_edit_state = State()
    phone_edit_state = State()