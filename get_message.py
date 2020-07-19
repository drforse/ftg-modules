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
import pprint

from telethon import errors as terrors

logger = logging.getLogger(__name__)


@loader.tds
class GetMessageMod(loader.Module):
    """Get message info"""
    strings = {"name": "get_message"}

    async def get_messagecmd(self, m):
        reply = await m.get_reply_message()
        changed_reply_dict = reply.to_dict()

        elements = (('to_id', 'user_id'),)

        for key, value in reply.to_dict().items():
            if not value and value is not False:
                del changed_reply_dict[key]
            if type(value) == int:
                changed_reply_dict[key] = f"\'<code>{value}</code>\'"

        for element in elements:
            path_to_element = ''
            for i in range(0, len(element)):
                path_to_element += f'[element[{i}]]'
            try:
                exec(
                    f'changed_reply_dict{path_to_element} = ' + 'f"\'<code>{changed_reply_dict%s}</code>\'"' % path_to_element)
            except (KeyError, IndexError):
                pass

        s = pprint.pformat(changed_reply_dict)
        lines = s.splitlines()
        for num, line in enumerate(lines):
            nline = lines[num] = line.split(':')[0].replace('\'', '') + ':' + ':'.join(
                line.split(':')[1:]) if ':' in line else line
            if '{' in nline:
                elements = nline.split('{')
                for elnum, el in enumerate(elements[1:]):
                    elements[elnum + 1] = el.split(':')[0].replace('\'', '') + ':' + ':'.join(
                        el.split(':')[1:]) if ':' in el else el
                nline = '{'.join(elements)
            lines[num] = nline
        s = '\n'.join(lines).replace('"\'', '').replace('\'"', '')
        try:
            await m.edit(s, parse_mode='html')
        except terrors.MessageTooLongError:
            await m.edit('too long error :--)')

    async def client_ready(self, client, db):
        self.client = client
