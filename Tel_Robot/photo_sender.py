
import logging
import telegram
from datetime import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "6268884938:AAEpODzegaSCnEipbwf4s0AGzcy9kakU6x0"
bot = telegram.Bot(token=TOKEN)
chat_id = "-1001944338560"


def photo():
    bot.send_photo(chat_id, photo=open('STRENGTH.png', "br"),
                   caption=f"{dt.now().strftime('Date: %Y-%m-%d  Time: %H:00:00')}")


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(photo, "cron", day_of_week="mon"    , hour="2-23" , minute="31", second=20)
    scheduler.add_job(photo, "cron", day_of_week="tue-fri",               minute="31", second=20)
    scheduler.start()
