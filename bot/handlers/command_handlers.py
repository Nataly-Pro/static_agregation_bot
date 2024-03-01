from datetime import timedelta
from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram3_calendar import DialogCalendar
from aiogram3_calendar.calendar_types import DialogCalendarCallback

from bot.keyboards import inline_keyboard
from bot.lexicon import LEXICON
from bot.services import get_report

command_router = Router()


# Cоздан класс для группы состояний FSM и экземпляры класса State,
# обозначающие возможные состояния, в которых будет находиться
# бот в разные моменты взаимодействия с пользователем."""
class Query(StatesGroup):
    dt_from = State()
    dt_upto = State()
    group_type = State()


@command_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    """Этот хэндлер срабатывает на команду /start и очищает контекст"""
    await state.clear()
    await message.answer(text=LEXICON['/start'])


@command_router.message(StateFilter(None), Command(commands=['date_from']))
async def command_date_from(message: Message, state: FSMContext) -> Message:
    """Этот хэндлер срабатывает на команду /date_from,
    предлагает определить дату начала периода выборки.
    """
    await state.set_state(Query.dt_from)
    return await message.answer(
        text='Выберите дату начала периода:',
        reply_markup=await DialogCalendar().start_calendar()
    )


@command_router.message(Command(commands=['date_to']))
async def command_date_to(message: Message, state: FSMContext) -> Message:
    """Этот хэндлер срабатывает на команду /date_to,
    предлагает определить дату конца периода выборки.
    """
    await state.set_state(Query.dt_upto)
    return await message.answer(
        text='Выберите дату окончания периода:',
        reply_markup=await DialogCalendar().start_calendar()
    )


@command_router.callback_query(Query.dt_from, DialogCalendarCallback.filter())
async def process_dialog_calendar_from(callback_query: CallbackQuery,
                                       callback_data: CallbackData,
                                       state: FSMContext) -> Message:
    """Этот хэндлер обрабатывает CallbackQuery и показывает начальную дату.
    """
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(dt_from=date)
        return await callback_query.message.answer(text=f'Вы выбрали дату начала периода: '
                                                        f'{date.strftime("%Y-%m-%d")}.')


@command_router.callback_query(Query.dt_upto, DialogCalendarCallback.filter())
async def process_dialog_calendar_to(callback_query: CallbackQuery,
                                     callback_data: CallbackData,
                                     state: FSMContext) -> None:
    """Этот хэндлер обрабатывает CallbackQuery и показывает конечную дату.
    """
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(dt_upto=date + timedelta(hours=23, minutes=59))
        await callback_query.message.answer(text=f'Вы выбрали дату окончания периода: '
                                                 f'{date.strftime("%Y-%m-%d")}.')


@command_router.message(Command(commands=['group_type']))
async def command_type(message: Message, state: FSMContext) -> Message:
    """Этот хэндлер срабатывает на команду /group_type,
    предлагает определить тип агрегирования.
    """
    await state.set_state(Query.group_type)
    return await message.answer(
        text='Выберите тип группировки данных: ',
        reply_markup=inline_keyboard
    )


@command_router.callback_query(Query.group_type, F.data.in_({'hour', 'day', 'month'}))
async def process_group_type(callback: CallbackQuery, state: FSMContext) -> None:
    """Этот хэндлер обрабатывает CallbackQuery, отфильтрованный по
    значению Callbackdata, и записывает тип агрегирования в Query.
    """
    await state.update_data(group_type=callback.data)
    await callback.message.answer(text=f'Тип агрегирования выбран "{callback.data}".')


@command_router.message(Command(commands=['report']))
async def command_report(message: Message, state: FSMContext) -> Message:
    """Этот хэндлер срабатывает на команду /report и возвращает
    агрегированные данные из БД в виде словаря.
    """
    data = await state.get_data()
    report = await get_report(data)
    if report['dataset']:
        return await message.answer(text=f'Отчёт:\n{report}')
    else:
        return await message.answer(text='За выбранный период нет данных.')

