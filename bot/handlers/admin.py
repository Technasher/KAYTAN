from typing import List

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from DB.repositories.program_repository import ProgramRepository
from DB.repositories.program_telegram_media_repository import ProgramTelegramMediaRepository
from DB.repositories.telegram_media_repository import TelegramMediaRepository
from bot.filters.admin import MessageAdminFilter, CallbackAdminFilter
from bot.keyboards.AdminKeyboard import admin_keyboard, cancel_add_program_keyboard
from bot.keyboards.InlineProgramList import get_inline_active_program_list
from bot.media_goup_manager import MediaGroupManager
from bot.states.ProgramFSM import ProgramState

router = Router()
router.message.filter(MessageAdminFilter())
router.callback_query.filter(CallbackAdminFilter())


async def create_program(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession,
        media_id_list: List[int]
):
    program_data = await state.get_data()
    program_repo = ProgramRepository(session)
    program = await program_repo.create(**program_data)
    program_telegram_media_repo = ProgramTelegramMediaRepository(session)
    program_id = program.id
    for media_id in media_id_list:
        await program_telegram_media_repo.create(
            program_id=program_id,
            telegram_media_id=media_id
        )
    await message.answer('Программа успешно создана!')
    await state.clear()


async def save_media_group(messages: List[types.Message], state: FSMContext, session: AsyncSession):
    await state.update_data(description=messages[0].caption)
    telegram_media_repo = TelegramMediaRepository(session)
    media_id_list = []
    for message in messages:
        if message.photo:
            media = await telegram_media_repo.create(
                file_id=message.photo[-1].file_id,
                file_unique_id=message.photo[-1].file_unique_id,
                file_type='photo'
            )
        elif message.video:
            media = await telegram_media_repo.create(
                file_id=message.video.file_id,
                file_unique_id=message.video.file_unique_id,
                file_type='video'
            )
        else:
            continue
        media_id_list.append(media.id)
    await create_program(messages[0], state, session, media_id_list)


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
async def create_program_handler(message: types.Message, state: FSMContext, session: AsyncSession):
    global media_group_manager
    media_group_manager = MediaGroupManager(
        callback=lambda l: save_media_group(l, state, session)
    )
    await message.answer('Введите название программы', reply_markup=cancel_add_program_keyboard)
    await state.set_state(ProgramState.name)


@router.message(F.text, ProgramState.name)
async def add_program_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите описание программы', reply_markup=cancel_add_program_keyboard)
    await state.set_state(ProgramState.description)


@router.message(lambda message: message.media_group_id is not None, ProgramState.description)
async def add_program_media_group(message: types.Message):
    await media_group_manager.handle_message(message)


@router.message(F.photo, ProgramState.description)
async def add_program_photo(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(description=message.caption)
    telegram_media_repo = TelegramMediaRepository(session)
    media = await telegram_media_repo.create(
        file_id=message.photo[-1].file_id,
        file_unique_id=message.photo[-1].file_unique_id,
        file_type='photo'
    )
    await create_program(message, state, session, [media.id])


@router.message(F.video, ProgramState.description)
async def add_program_video(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(description=message.caption)
    telegram_media_repo = TelegramMediaRepository(session)
    media = await telegram_media_repo.create(
        file_id=message.video.file_id,
        file_unique_id=message.video.file_unique_id,
        file_type='video'
    )
    await create_program(message, state, session, [media.id])


@router.message(F.text, ProgramState.description)
async def add_program_description(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(description=message.text)
    await create_program(message, state, session, [])


@router.callback_query(F.data == 'cancel_add_program')
async def cancel_add_program(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Отмена создания программы')
