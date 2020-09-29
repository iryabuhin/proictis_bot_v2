from vkbottle import Bot
from vkbottle import PhotoUploader
from dotenv import load_dotenv
from routes import main, mentors, demo
from utils import envget

load_dotenv()
token = envget('TOKEN')

bot = Bot(tokens=[token])
photo_uploader = PhotoUploader(bot.api, generate_attachment_strings=True)


if __name__ == '__main__':
    bot.set_blueprints(demo.bp, mentors.bp, main.bp)

    for item in bot.branch.branches:
        print(item)

    print(bot.branch.names, 'mentors' in bot.branch.names)
    bot.branch.add_branch(
        mentors.MentorInfoBranch,
        'mentors'
    )

    # bot.branch = PostgresStoredBranch()

    bot.run_polling()
