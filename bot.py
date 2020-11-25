from vkbottle import Bot, Message
from vkbottle import PhotoUploader
from dotenv import load_dotenv
from config import Config
from routes import main, mentors, news, faq, schedule
from models import DBStoredBranch, UserState
from utils import init_db
from vkbottle.ext import Middleware
import os


load_dotenv()
token = os.environ.get('TOKEN')
bot = Bot(tokens=[token], debug=Config.DEBUG)
bot.branch = DBStoredBranch()
photo_uploader = PhotoUploader(bot.api, generate_attachment_strings=True)


@bot.middleware.middleware_handler()
class CheckUserStateMiddleware(Middleware):
    async def pre(self, msg: Message, *args):
        if not Config.USE_MIDDLEWARE:
            return

        u = await UserState.filter(uid=msg.from_id).get_or_none()

        if u is None:
            u = await UserState.create(
                uid=msg.from_id,
                branch='main',
                context={}
            )
            await u.save()


if __name__ == '__main__':
    bot.set_blueprints(mentors.bp, main.bp, news.bp, faq.bp, schedule.bp, main.bp)

    bot.run_polling(
        on_startup=init_db
    )
