from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER  # make sure LOGGER points to your logging util


class PURVI(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="PURVIMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        # Start Pyrogram client
        await super().start()

        # Store bot info
        self.id = self.me.id
        self.name = f"{self.me.first_name} {self.me.last_name or ''}".strip()
        self.username = self.me.username
        self.mention = self.me.mention

        # Try to access logger chat safely
        try:
            # Force Pyrogram to cache the logger chat
            await self.get_chat(config.LOGGER_ID)

            # Send start message to logger
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                    f"ɪᴅ : <code>{self.id}</code>\n"
                    f"ɴᴀᴍᴇ : {self.name}\n"
                    f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
                ),
                parse_mode=ParseMode.HTML,
            )

            # Check if bot is admin
            member = await self.get_chat_member(config.LOGGER_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).warning(
                    "Bot is not admin in logger chat. Some features may not work."
                )

        except Exception as e:
            # Logger is unavailable, but bot continues to run
            LOGGER(__name__).warning(
                f"Logger chat unavailable or inaccessible. Continuing without logger. Details: {e}"
            )

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
        LOGGER(__name__).info("Bot stopped successfully.")
