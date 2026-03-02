from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from DB.repositories.program_repository import ProgramRepository
from bot.filters.admin import MessageAdminFilter, CallbackAdminFilter
from bot.keyboards.AdminKeyboard import admin_keyboard
from bot.keyboards.InlineProgramList import get_inline_active_program_list
from bot.states.ProgramFSM import ProgramState

router = Router()
router.message.filter(MessageAdminFilter())
router.callback_query.filter(CallbackAdminFilter())


@router.callback_query(F.data.startswith('deactivate:'))
async def deactivate_program(callback: CallbackQuery, session: AsyncSession):
    program_id = int(callback.data.split(":")[1])
    program_repo = ProgramRepository(session)
    await program_repo.deactivate(program_id)
    await callback.message.answer('Программа успешно деактивирована!')


@router.message(Command('admin'))
async def admin(message: types.Message):
    await message.answer(
        'Добро пожаловать в админ-панель!',
        reply_markup=admin_keyboard
    )


@router.message(F.text == 'Список активных программ')
async def active_program_list(message: types.Message, session: AsyncSession):
    program_repo = ProgramRepository(session)
    programs = await program_repo.get_active_list()
    keyboard = await get_inline_active_program_list(programs)
    await message.answer(
        'Вот список активных программ:',
        reply_markup=keyboard
    )


@router.message(F.text == 'Создать новую программу')
async def create_program(message: types.Message, state: FSMContext):
    await message.answer('Введите название программы')
    await state.set_state(ProgramState.name)


@router.message(F.text, ProgramState.name)
async def add_program_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите описание программы')
    await state.set_state(ProgramState.description)


@router.message(F.text, ProgramState.description)
async def add_program_description(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(description=message.text)
    program = await state.get_data()
    program_repo = ProgramRepository(session)
    await program_repo.create(**program)
    await message.answer('Программа успешно создана!')
