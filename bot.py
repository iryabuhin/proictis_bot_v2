from vkbottle import Bot, Message
from vkbottle import PhotoUploader
from vkbottle.ext import Middleware
from models import UserState
from dotenv import load_dotenv
from config import Config
from routes import main, mentors, news, faq, schedule
from models import DBStoredBranch
from utils import envget
from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url=Config.DATABASE_URL or 'sqlite://users.db',
        modules={
            'models': ['models.user_state']
        }
    )
    await Tortoise.generate_schemas()


load_dotenv()
token = envget('TOKEN')
bot = Bot(tokens=[token], debug=Config.DEBUG)
bot.branch = DBStoredBranch()
photo_uploader = PhotoUploader(bot.api, generate_attachment_strings=True)

@bot.middleware.middleware_handler()
class UserStateMiddleware(Middleware):
    async def pre(self, msg: Message, *args):
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
