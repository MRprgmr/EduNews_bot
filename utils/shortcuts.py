from aiogram.types import Message
import re

from core.config import settings
from db.models import User
from keyboards.inline_markup import required_channels_tm
from keyboards.reply_markup import main_menu_tm


async def check_channels(user: User) -> bool:
    from core.misc import bot
    for chat_id in settings.REQUIRED_CHANNELS_IDS:
        try:
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user.tg_id)
            if member.status in ["restricted", "left", 'kicked']:
                return False
        except Exception:
            return False
    return True


async def phone_number_validator(message: Message) -> str | None:
    if message.content_type == 'contact':
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text
    if phone_number[0] != '+':
        phone_number = '+' + phone_number

    if re.match(r"\+998(?:33|93|94|97|90|91|98|99|95|88)\d\d\d\d\d\d\d", phone_number) is not None:
        return phone_number
    else:
        return None


async def send_main_menu(message: Message, user: User) -> None:
    data = await main_menu_tm(user=user)
    await message.answer(**data)


async def send_membership_alert(message: Message, user: User) -> None:
    data = await required_channels_tm(user)
    await message.answer(**data)


def post_text_maker(data: dict) -> str:
    post_text = "\n".join([
        "<b>{title}</b>\n",
        "<i>{description}</i>",
        "\nš <b>{district_name},  {school_name}</b>",
        "\nš  @{bot_username}"
    ]).format(**data, bot_username=settings.BOT_USERNAME)
    return post_text
