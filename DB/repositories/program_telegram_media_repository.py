from DB.models.program_telegram_media import ProgramTelegramMedia
from DB.repositories.base_repository import BaseRepository


class ProgramTelegramMediaRepository(BaseRepository):
    async def create(self, **kwargs) -> ProgramTelegramMedia:
        associations = ProgramTelegramMedia(**kwargs)
        self.session.add(associations)
        await self.session.commit()
        await self.session.refresh(associations)
        return associations
