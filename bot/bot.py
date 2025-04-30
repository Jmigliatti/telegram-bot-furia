from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from update_ngrok_url import get_ngrok_url


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ngrok_public_url = get_ngrok_url()
    if ngrok_public_url:
        print(f"URL pública do ngrok: {ngrok_public_url}")
    else:
        print("Não foi possível obter a URL do ngrok")

    keyboard = [
        [InlineKeyboardButton("Ver Produtos", callback_data='produtos')],
        [InlineKeyboardButton("Redes Sociais", callback_data='redes')],
        [InlineKeyboardButton("Loja da Furia", url="https://t.me/furi4bot/furiaApp")],
        [InlineKeyboardButton("Noticias da Furia", url=ngrok_public_url)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Olá! O que você gostaria de fazer?', reply_markup=reply_markup)

async def produto_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    index = int(query.data.split("_")[1])
    await enviar_produto(update, context, produtos, index)

produtos = [
    {
        "imagem": "https://furiagg.fbitsstatic.net/img/p/camiseta-furia-adidas-preta-150263/337479-1.jpg?w=1280&h=1280&v=202503281012",
        "titulo": "Camiseta FURIA Preta - R$129,00",
    },
    {
        "imagem": "https://furiagg.fbitsstatic.net/img/p/jaqueta-furia-x-zor-verde-militar-150246/337361-1.jpg?w=1280&h=1280&v=no-value",
        "titulo": "Moletom FURIA - R$249,00",
    }
]


async def enviar_produto(update: Update, context: ContextTypes.DEFAULT_TYPE, produtos, index: int):
    produto = produtos[index]

    buttons = []

    if index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"produto_{index-1}"))
    if index < len(produtos) - 1:
        buttons.append(InlineKeyboardButton("Próximo ➡️", callback_data=f"produto_{index+1}"))

    reply_markup = InlineKeyboardMarkup([buttons])

    if update.callback_query:
        await update.callback_query.edit_message_media(
            media=InputMediaPhoto(media=produto["imagem"], caption=produto["titulo"]),
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_photo(
            photo=produto["imagem"],
            caption=produto["titulo"],
            reply_markup=reply_markup
        )

async def produtos_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_produto(update, context, produtos, index=0)


async def redes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Instagram", url='https://www.instagram.com/furiagg/?hl=pt')],
        [InlineKeyboardButton("YouTube", url='https://www.youtube.com/@FURIAgg')],
        [InlineKeyboardButton("TikTok", url='https://www.tiktok.com/@furia')],
        [InlineKeyboardButton("X (Twitter)", url='https://twitter.com/FURIA')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text('Siga a FURIA em todas as redes sociais e fique por dentro de tudo que acontece!', reply_markup=reply_markup)


def main():
    app = ApplicationBuilder().token("7526898144:AAEimW92zjqbsZ1WJeUkfKUJVPrvONU42io").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(produtos_handler, pattern='^produtos$'))
    app.add_handler(CallbackQueryHandler(produto_callback, pattern='^produto_\\d+$'))
    app.add_handler(CallbackQueryHandler(redes, pattern='^redes$'))

    app.run_polling()


if __name__ == '__main__':
    main()
