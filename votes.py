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
import traceback

logger = logging.getLogger(__name__)


@loader.tds
class VotesMod(loader.Module):
    """Get votes from @GlobalAdministratorBot in group with it"""
    strings = {"name": "votes"}

    @loader.unrestricted
    @loader.ratelimit
    async def votescmd(self, m):
        client = self.client

        last_admin_change_m = await client.get_messages(entity=m.chat.id,
                                                        search='Производится выбор нового администратора...',
                                                        from_user='GlobalAdministratorBot')
        last_admin_change_m = last_admin_change_m[0]
        votes = {}
        no_anon_votes = 0
        async for msg in client.iter_messages(entity=m.chat.id, min_id=last_admin_change_m.id,
                                              search='Вы успешно проголосовали!',
                                              from_user='GlobalAdministratorBot'):
            try:
                reply_message = await msg.get_reply_message()
                vote_for = reply_message.message.split()[1]
                vote_from = reply_message.from_id
                no_anon_votes += 1
                if vote_for in votes:
                    votes[vote_for].append(vote_from)
                    continue
                votes[vote_for] = [vote_from]
            except AttributeError:
                logging.warning(f'vote info not found\n{traceback.format_exc()}')
        all_votes = client.iter_messages(entity=m.chat.id, min_id=last_admin_change_m.id,
                                         search='проголосовал за одного из кандидатов!',
                                         from_user='GlobalAdministratorBot')
        all_votes = len([i async for i in all_votes])
        anonimous = all_votes - no_anon_votes
        text = ''
        for u in votes:
            user = await client.get_entity(entity=int(u))
            text += f'<b>{user.first_name}({len(votes[u])})</b>:\n'
            for vote in votes[u]:
                voted = await client.get_entity(entity=vote)
                text += f'ᅠ{voted.first_name}\n'
            text += '• ' * 25 + '\n'
        text += f'\nАнонимные голоса: {anonimous}\n\nP.S.: если есть анонимные голоса, то количество голосов неточное.' \
                f' Также счет может быть неточным за счёт удаления следов голосования из чата!'
        try:
            await client.edit_message(m, text, parse_mode='html')
        except:
            await client.send_message(m.chat, text, parse_mode='html')

    async def client_ready(self, client, db):
        self.client = client
