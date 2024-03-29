import io
import logging

from .. import loader, utils

from telethon.tl.types import ChannelParticipantsBots, Message, DocumentAttributeFilename

logger = logging.getLogger(__name__)


@loader.tds
class ExpiringMediaMod(loader.Module):
    """Send all expiring media (not from secret chats) to Saved Messages"""
    strings = {"name": "Expiring Media"}

    async def watcher(self, m):
        if not isinstance(m, Message):
            return
        if not self.__is_expiring_photo(m):
            return
        sender_s = (f'{m.sender.first_name or ""} {m.sender.last_name or ""} '
                    f'{m.sender.username or ""} ({m.sender_id})')
        bytesio = io.BytesIO()
        await m.download_media(bytesio)
        bytesio.seek(0)
        await self.client.send_file(
            'me', file=bytesio, caption=f'Expiring media from: {sender_s}',
            parse_mode='HTML', attributes=[DocumentAttributeFilename(m.file.name)])
        bytesio.close()

    async def client_ready(self, client, db):
        self.client = client

    @staticmethod
    def __is_expiring_photo(m):
        if not m.media:
            return False
        if not m.media.ttl_seconds:
            return False
        return True
