from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload
from DB.models.program import Program
from DB.repositories.base_repository import BaseRepository


class ProgramRepository(BaseRepository):
    async def create(self, **kwargs) -> Program:
        program = Program(**kwargs)
        self.session.add(program)
        await self.session.commit()
        await self.session.refresh(program)
        return program

    async def get_active_list(self):
        stmt = select(Program).filter_by(is_active=True)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_program_by_id(self, program_id) -> Program | None:
        stmt = select(Program).filter_by(id=program_id).options(selectinload(Program.telegram_media))
        result = await self.session.execute(stmt)
        return result.one_or_none()[0]

    async def deactivate(self, program_id):
        stmt = update(Program).filter_by(id=program_id).values(is_active=False)
        await self.session.execute(stmt)
        await self.session.commit()
