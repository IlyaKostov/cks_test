import logging

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from bot_app.utils import add_product_api, delete_product_api, get_products_list_api, get_price_history_api

logger = logging.getLogger(__name__)

router = Router()


class ProductStates(StatesGroup):
    waiting_for_url = State()
    waiting_for_product_id = State()


@router.message(CommandStart())
async def start(message: Message):
    """Обработчик команды /start."""
    await message.answer(
        '👋 <b>Бот мониторинга цен</b>\n\n'
        'Доступные команды:\n'
        '/add - Добавить продукт на мониторинг\n'
        '/list - Список продуктов на мониторинге\n'
        '/history - История цен на продукт\n'
        '/delete - Удалить продукт из мониторинга',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command('add'))
async def add_product(message: Message, state: FSMContext):
    await message.answer('🔗 Пожалуйста, отправьте ссылку на товар:')
    await state.set_state(ProductStates.waiting_for_url)


@router.message(ProductStates.waiting_for_url)
async def process_product_url(message: Message, state: FSMContext):
    url = message.text.strip()
    if not url.startswith(('http://', 'https://')):
        await message.answer('⚠️ Пожалуйста, введите корректную URL-ссылку')
        return

    try:
        result = await add_product_api(message.text)
        if result.get('id'):
            await message.answer(f'✅ Товар успешно добавлен! ID: {result['id']}\nName: {result['name']}')
        else:
            await message.answer('❌ Ошибка при добавлении товара. Проверьте ссылку.')
    except Exception as e:
        logger.error(f'Error adding product: {e}')
        await message.answer('⚠️ Произошла ошибка при обработке запроса')
    finally:
        await state.clear()


@router.message(Command('delete'))
async def cmd_delete_product(message: Message, state: FSMContext):
    await message.answer('❌ Введите ID товара для удаления:')
    await state.set_state(ProductStates.waiting_for_product_id)


@router.message(ProductStates.waiting_for_product_id)
async def process_delete_product(message: Message, state: FSMContext):
    try:
        product_id = int(message.text)
        success = await delete_product_api(product_id)
        if success:
            await message.answer(f'✅ Товар ID {product_id} успешно удален!')
        else:
            await message.answer('❌ Ошибка при удалении товара. Проверьте ID.')
    except ValueError:
        await message.answer('⚠️ Пожалуйста, введите числовой ID товара')
    except Exception as e:
        logger.exception('Error deleting product')
        await message.answer('⚠️ Произошла ошибка при обработке запроса')
    finally:
        await state.clear()


@router.message(Command('list'))
async def cmd_products_list(message: Message):
    try:
        products = await get_products_list_api()
        if not products:
            await message.answer('📭 Список товаров пуст')
            return

        response = ['📋 Список отслеживаемых товаров:\n\n']

        for product in products:
            response.append(f'🆔 ID: {product['id']}\n')
            response.append(f'🏷️ Название: {product['name']}\n')
            response.append(f'🔗 Ссылка: {product['url']}\n')
            response.append(f'🕒 Добавлен: {product['created_at']}\n\n')

        final_response = ''.join(response)

        await message.answer(final_response)
    except Exception as e:
        logger.exception('Error getting products list')
        await message.answer('⚠️ Не удалось получить список товаров')


@router.message(Command('history'))
async def cmd_price_history(message: Message, state: FSMContext):
    await message.answer('📈 Введите ID товара для просмотра истории цен:')
    await state.set_state(ProductStates.waiting_for_product_id)


@router.message(ProductStates.waiting_for_product_id)
async def process_price_history(message: Message, state: FSMContext):
    try:
        product_id = int(message.text)
        history = await get_price_history_api(product_id)

        if not history:
            await message.answer(f'📭 История цен для товара ID {product_id} отсутствует')
            return

        response = [f'📊 История цен для товара ID {product_id}:\n\n']
        for entry in history:
            response.append(f'💰 Цена: {entry['price']} руб.\n')
            response.append(f'🕒 Дата: {entry['created_at']}\n\n')

        final_response = ''.join(response)

        await message.answer(final_response)
    except ValueError:
        await message.answer('⚠️ Пожалуйста, введите числовой ID товара')
    except Exception as e:
        logger.exception('Error getting price history')
        await message.answer('⚠️ Произошла ошибка при получении истории цен')
    finally:
        await state.clear()
