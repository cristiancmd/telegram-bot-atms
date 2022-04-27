import datetime
import logging
import os
import pytz
from cajero_handler import CajeroHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from map_generator import MapGenerator as Maps
from dotenv import load_dotenv

load_dotenv()
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


logger = logging.getLogger(__name__)
cajeros = CajeroHandler()


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hola {user.mention_markdown_v2()}\! Te ofrezco las ubicaciones de las cajeros Red Link y Banelco que se encuentran en CABA y a un rango de 500m\. Escribí uno de los comandos disponibles\.\.',
        reply_markup=ForceReply(selective=True),
    )


def echo(update: Update, context: CallbackContext) -> None:
    start(update,context)


def link(update: Update, context: CallbackContext) -> None:
    sendButton(update, context, 'LINK')


def banelco(update: Update, context: CallbackContext) -> None:
    sendButton(update, context, 'BANELCO')


def sendButton(update: Update, context: CallbackContext, type: str):
    location_keyboard = KeyboardButton(
        text="Enviar ubicación", request_location=True)
    my_keyboard = ReplyKeyboardMarkup(
        [[location_keyboard]], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(
        f'ℹ️  Presiona "Enviar ubicación" para ver los cajeros {type} cercanos.', reply_markup=my_keyboard)
    context.user_data['tipo'] = type


def location_data_handler(update: Update, context: CallbackContext):

    type = context.user_data['tipo']
    removeKw = ReplyKeyboardRemove(True)
    long = update.message.location.longitude
    lat = update.message.location.latitude

    if(type == 'LINK'):
        points, data = cajeros.get_link((long, lat))
    if(type == 'BANELCO'):
        points, data = cajeros.get_banelco((long, lat))

    text_res = string_res_build(data, points, type)
    update.message.reply_text(text_res, reply_markup=removeKw)
    map = Maps(long, lat, points)
    image = map.get_image_url()
    update.message.reply_photo(image)


def string_res_build(data, points, tipo):
    text_res = f"✅ Cajeros {tipo} encontrados: \n \n"
    letras = ['A', 'B', 'C', 'D', 'E']
    for val in data:
        text_res += ("{3}{2}{0} - {1}\n\n".format(
            val['banco'], val['ubicacion'], '📍: ', letras[data.index(val)]))
    if(len(points) < 1):
        text_res = "ℹ️ No se encontraron cajeros en tu zona. Probá buscando cajeros de otra red!"
    return text_res


def reset_cajeros(context: CallbackContext):
    cajeros.reset_cronjob()


def main() -> None:
    """Start the bot."""

    # Create the Updater and pass it your bot's token.
    updater = Updater( os.getenv("BOT_KEY"), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("link", link))
    dispatcher.add_handler(CommandHandler("banelco", banelco))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(
        Filters.location, location_data_handler))

    # cronjob cajeros
    job = updater.job_queue
    dt = datetime.datetime.now()
    timezone = pytz.timezone("America/Argentina/Buenos_Aires")
    d_aware = timezone.localize(dt)
    time = datetime.time(hour=8, minute=00, second=00, tzinfo=d_aware.tzinfo)
    job.run_daily(reset_cajeros, days=(1, 2, 3, 4, 5), time=time)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
