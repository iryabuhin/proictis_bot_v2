from vkbottle import Bot
from vkbottle import PhotoUploader
from dotenv import load_dotenv
from routes import main, mentors, demo, news
from models import PostgresStoredBranch
from utils import envget
from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url=envget('DATABASE_URL') or 'postgres://test:test@127.0.0.1:5432/test',
        modules={
            'models': ['models.user_state']
        }
    )
    await Tortoise.generate_schemas()


load_dotenv()
token = envget('TOKEN')
bot = Bot(tokens=[token])
bot.branch = PostgresStoredBranch()
photo_uploader = PhotoUploader(bot.api, generate_attachment_strings=True)


if __name__ == '__main__':
    bot.set_blueprints(demo.bp, mentors.bp, main.bp, news.bp)

    for branch in bot.branch.branches:
        print(branch)

    bot.run_polling(
        on_startup=init_db
    )
