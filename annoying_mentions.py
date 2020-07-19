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
import random

from telethon import types

logger = logging.getLogger(__name__)

CHATS_WITH_ANNOYING_MENTIONS = [1240221895, ]
ANSWERS_TO_ANNOYING_PIECES_OF_SHIT = ['<s>FUCK OFF</s> Пожалуйста, не беспокойте меня по мелочам типа игры, которая '
                                      'меня бесит и т.п., если у вас есть сказать что-то важное, напишите мне в личку.'
                                      '\nP.S.: если у вас бан за спам, попросите кого-нибудь рядом', ]
MARK_ANNOYING_MENTIONS_READ = True


@loader.tds
class AnnoyingMentionsMod(loader.Module):
    """Fuck off"""
    strings = {"name": "Annoying Mentions"}

    async def watcher(self, m):
        if not isinstance(m, types.Message):
            return
        if not self.__is_annoying_mention(m):
            return
        answer = random.choice(ANSWERS_TO_ANNOYING_PIECES_OF_SHIT)
        await m.reply(answer, parse_mode='html')
        if MARK_ANNOYING_MENTIONS_READ:
            await m.mark_read()

    @staticmethod
    def __is_annoying_mention(m):
        if m.chat.id in CHATS_WITH_ANNOYING_MENTIONS:
            return m.mentioned
        if m.chat.username not in CHATS_WITH_ANNOYING_MENTIONS:
            return False
        return m.mentioned

    async def client_ready(self, client, db):
        self.client = client
