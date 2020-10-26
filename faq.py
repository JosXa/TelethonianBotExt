import json
import re
import os
from pathlib import Path

from telethon import events

# TODO Make this better
template = "The cause of this error is most likely {cause}. To fix it you need to {solution}"
faq_json = Path(__file__).parent / "faq.json"
errors = json.loads(faq_json.read_text(encoding="utf-8"))

FAQ_URL = 'https://docs.telethon.dev/en/latest/quick-references/faq.html'

async def init(bot):
    @bot.on(events.NewMessage)
    async def handler(event):
        for error in errors:
            if re.search(error["pattern"], event.raw_text, flags=re.IGNORECASE):
                await event.reply(template.format(cause=error["cause"], solution=error["solution"]))
                break

    @bot.on(events.NewMessage(pattern='#faq'))
    async def handler(event):
        """#faq: Tell the user that their problem is in the faq."""
        await event.delete()
        await event.respond(
            f"You can find a solution to your problem in [Telethon's FAQ]({FAQ_URL})",
            reply_to=event.reply_to_msg_id
        )
