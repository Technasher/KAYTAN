from sqlalchemy import select

from DB.models.telegram_media import TelegramMedia, MediaType
from DB.repositories.base_repository import BaseRepository


class TelegramMediaRepository(BaseRepository):
    async def check_file(self, file_id) -> TelegramMedia | None:
        stmt = select(TelegramMedia).filter_by(file_id=file_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> TelegramMedia:
        file = await self.check_file(kwargs['file_id'])
        if file:
            return file
        else:
            media = TelegramMedia(
                file_id=kwargs['file_id'],
                file_unique_id=kwargs['file_unique_id'],
                file_type=MediaType(kwargs['file_type'])
            )
            self.session.add(media)
            await self.session.commit()
            await self.session.refresh(media)
            return media
