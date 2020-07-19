#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils
import logging

from telethon.tl.types import ChannelParticipantsBots

logger = logging.getLogger(__name__)


@loader.tds
class BotsMod(loader.Module):
    """Get all bots in chat"""
    strings = {"name": "bots"}

    async def botscmd(self, m):
        client = self.client
        answer = ''
        quant = 0
        async for bot in client.iter_participants(m.chat, filter=ChannelParticipantsBots):
            answer += f'{bot.first_name} (@{bot.username})\n'
            quant += 1
        answer += f'\n{quant}'
        await client.edit_message(m, answer)

    async def client_ready(self, client, db):
        self.client = client
