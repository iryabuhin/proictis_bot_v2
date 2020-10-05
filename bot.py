from vkbottle import Bot
from vkbottle import PhotoUploader
from dotenv import load_dotenv

from config import Config
from routes import main, mentors, demo, news, faq
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
bot = Bot(tokens=[token])
bot.branch = DBStoredBranch()
photo_uploader = PhotoUploader(bot.api, generate_attachment_strings=True)


if __name__ == '__main__':
    bot.set_blueprints(mentors.bp, main.bp, news.bp, faq.bp)

    bot.run_polling(
        on_startup=init_db
    )
