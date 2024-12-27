# aiogram import
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

# kode import
from loader import dp, bot
from utils import texts, buttons
from utils.env import CHANNEL_ID

# add import
from asyncio import create_task


async def chat_handler_task(message: Message, state: FSMContext):
    """
    Guruhda foydalanuvchilar xabarlariga javob beruvchi funksiya
    """
    user_id = message.from_user.id
    username = message.from_user.username or "No username"
    text = message.text.lower().strip()

    print(user_id, text)

    keywords = ["pochta", "ketishim kerak", "yo‘lga chiqaman", "borishim kerak", "yetib olishim kerak"]

    if any(keyword in text for keyword in keywords):
        mail = text
        try:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=texts.text_to_send(
                    username=username,
                    mail=mail
                ),
                reply_markup=buttons.group_mail_success_admin(user_id)
            )
            await message.reply(texts.MAIL_SEND_MESSAGE.format(message.from_user.first_name))
        except Exception as e:
            print(f"Error sending mail message: {e}")
            return
        

@dp.message_handler(content_types=['text'], state='*')
async def chat_handler(message: Message, state: FSMContext):
    if message.chat.type in ['group', 'supergroup']:
        await create_task(chat_handler_task(message, state))
