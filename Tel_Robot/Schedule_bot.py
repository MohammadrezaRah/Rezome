import logging
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler,Filters , MessageHandler, ConversationHandler
import datetime
from datetime import datetime as dt
import time
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
SECONDS,MINUTES, HOURS, DAYS = range(4)

reply_keyboard = [["Stop", "Schedule"]]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

TOKEN = "6193405666:AAGsy-JjXRmzwbiNAVYL8ZDeoDYiTNGLApQ"
bot = telegram.Bot(token=TOKEN)
chat_id = "-1001876323749"


def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f"HI {user.first_name} \n"
                              f"Your ID is {user.id}",
                              reply_markup=markup)
    bot.send_message(chat_id=chat_id, text=f"{user.first_name} Started the bot\nAt {dt.now().strftime('%A')}"
                                           f"\n{dt.now().strftime('%Y-%m-%d  %H:%M:%S')}")
    print(user.first_name, "Started the bot")
    print(user)

def stop(update, context):
    user = update.message.from_user
    update.message.reply_text(f"GoodBye {user.first_name}",
                              reply_markup=ReplyKeyboardMarkup([["Start"]], resize_keyboard=True))
    bot.send_message(chat_id=chat_id, text=f"{user.first_name} Stopped the bot\nAt {dt.now().strftime('%A')}"
                                           f"\n{dt.now().strftime('%Y-%m-%d  %H:%M:%S')}")
    print(f"{user.first_name} Stopped the bot")

def echo(update, context):
    update.message.reply_text(f"'{update.message.text}' Is Not a Command")
    user = update
    print("echo")

def error(update, context):
    logger.warning("Update '{}' caused error '{}'".format(update, context.error))

def entry(update, context):
    update.message.reply_text("SECONDS?",
                              reply_markup=ReplyKeyboardMarkup([["Done"]], resize_keyboard=True))
    return SECONDS

def seconds(update, context):
    global s
    update.message.reply_text("MINUTES?")
    s = int(update.message.text)
    print("SECONDS", s)
    return MINUTES

def minutes(update, context):
    global m
    update.message.reply_text("HOURS?")
    m = int(update.message.text)
    print("MINUTES", m)
    return HOURS

def hours(update, context):
    global h
    update.message.reply_text("DAYS?")
    h = int(update.message.text)
    print("HOURS", h)
    return DAYS

def days(update, context):
    global d
    d = int(update.message.text)
    print("DAYS", d)
    global done
    from_now = datetime.timedelta(days=d, hours=h, minutes=m, seconds=s)
    now = dt.now()
    done = from_now + now
    update.message.reply_text(f"Schedule set: {done.strftime('%Y-%m-%d  %H:%M:%S')}"
                              f"\nTIME now is : {now.strftime('%Y-%m-%d  %H:%M:%S')}")
    print(now)
    print(done)
    scheduler()

def task():         # do what you want here
    bot.send_message(chat_id=chat_id, text="Done")

def scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(task, "date", next_run_time= done)
    scheduler.start()



def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))

    dp.add_handler(MessageHandler(Filters.text("Start"), start))
    dp.add_handler(MessageHandler(Filters.text("Stop"), stop))
    dp.add_handler(MessageHandler(Filters.text("Done"), start))

    conv_handler = ConversationHandler(
        entry_points= [MessageHandler(Filters.text("Schedule"), entry)],

        states={
            SECONDS:[MessageHandler(Filters.text("Schedule"), entry),
                     MessageHandler(Filters.text("Done"), start), MessageHandler(Filters.text, seconds)],
            MINUTES:[MessageHandler(Filters.text("Schedule"), entry),
                     MessageHandler(Filters.text("Done"), start), MessageHandler(Filters.text, minutes)],
            HOURS:[MessageHandler(Filters.text("Schedule"), entry),
                   MessageHandler(Filters.text("Done"), start), MessageHandler(Filters.text, hours)],
            DAYS:[MessageHandler(Filters.text("Schedule"), entry),
                  MessageHandler(Filters.text("Done"), start), MessageHandler(Filters.text, days)]
        },
        fallbacks="cancell")

    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()