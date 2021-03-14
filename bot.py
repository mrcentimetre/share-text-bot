from urllib.parse import quote

from pyrogram import Client, filters
from pyrogram.types import (
    InputTextMessageContent,
    InlineQueryResultArticle,
    Message,
    InlineQuery,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

api_id = api id
api_hash = 'api hash'
token = "bot token"

app = Client(":memory:", api_id, api_hash, bot_token=token)

##Start Message & Buttons
@bot.on_message(filters.command("start") & filters.private)
async def welcomemsg(bot, msg):
    await msg.reply(f"Welcome {msg.from_user.mention}, I'm Share Text Bot \n\nJust Forward me any message and I will create a share link for it.\n\nEnjoy! 😉",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🆘 Help",  callback_data="help"),
                    InlineKeyboardButton("💚 Credits",  callback_data=b"Credits")
                ],
                [
                    InlineKeyboardButton("📣 Channel",  url="https://t.me/TDICProjects"),
                    InlineKeyboardButton("👥 Group",  url="https://t.me/TDICSupport"),
                ]
            ]
        )
    )

#Back Button
@bot.on_callback_query(filters.regex(r"^back"))
async def backtostart(bot, query: CallbackQuery):
	await query.message.delete(revoke=True)
	await msg.reply(f"Welcome {msg.from_user.mention}, I'm Share Text Bot \n\nJust Forward me any message and I will create a share link for it.\n\nEnjoy! 😉",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🆘 Help",  callback_data="help"),
                    InlineKeyboardButton("💚 Credits",  callback_data=b"Credits")
                ],
                [
                    InlineKeyboardButton("📣 Channel",  url="https://t.me/TDICProjects"),
                    InlineKeyboardButton("👥 Group",  url="https://t.me/TDICSupport"),
                ]
            ]
        )
    )
    
#Setup Help Message with buttons    
@bot.on_callback_query(filters.regex(r"^help"))
async def helpbutton(bot: Client, query: CallbackQuery):
	await query.message.delete(revoke=True)
	await query.message.reply_sticker("CAACAgUAAxkBAAEJZtZgSPs_fV8OmqAu3fBsbfc9WwJdBgACtAEAAuvwSVYLyVS6tQ2Yyh4E",
    reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔙 Back", callback_data="back")],
        ]
    )
)

#Popup Credits    
@bot.on_callback_query(filters.regex(r"^Credits"))
async def credits(bot: Client, query: CallbackQuery):
    await query.answer("Developer 🧑‍💻\n\n • @itayki", show_alert=True)

#Share Command in groups
@app.on_message(filters.group & filters.text & filters.command("share"))
async def groupmsg(client: app, message: Message):
    reply = message.reply_to_message
    input_split = message.text.split(None, 1)
    if len(input_split) == 2:
        input_text = input_split[1]
    elif reply and (reply.text or reply.caption):
        input_text = reply.text or reply.caption
    else:
        await message.reply_text(
            "**ERROR** : `No Input found !`",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("delete this message", "deleterrormessage")]]
            ),
        )
        return
    await message.reply_text(share_link(input_text))


@app.on_callback_query(filters.regex("^deleterrormessage"))
async def delerrmsg(client: app, cquery: CallbackQuery):
    await cquery.message.delete()

#Private Message
@app.on_message(filters.private)
async def privatensg(client: app, message: Message):
    await message.reply_text(share_link(message.text))


@app.on_inline_query()
async def inlineshare(client: app, query: InlineQuery):
    if query.query:
        await query.answer(
            [
                InlineQueryResultArticle(
                    "click to share", InputTextMessageContent(share_link(query.query))
                )
            ]
        )


def share_link(text: str) -> str:
    return "https://t.me/share/url?url=" + quote(text)


app.run()
