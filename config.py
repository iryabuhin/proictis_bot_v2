from utils import envget
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASEDIR = os.path.abspath(__file__)
    TOKEN = envget('TOKEN') or  None
    DATABASE_URL = envget('DATABASE_URL') or "sqlite://users.db"
    BASE_API_URL = 'https://proictis.sfedu.ru'
    PORT = int(envget('PORT') or 5555)

    URL_PATH = {
        'mentors': '/api/mentors',
        'projects': '/api/projects',
        'news': '/api/news',
        'sheets': '/api/projects/sheets',
        'chats': '/api/chats',
        'me': '/api/me',
        'competitions': '/api/competitions',
        'contacts': '/about',
        'achievements': '/api/achievements',
        'login': '/api/login',
        'archive': '/api/chat/archive',
        'requests': '/api/me/requests',
        'update': '/api/update'
    }

    NEWS_PER_MSG = 4
    NEWS_TITLE_MAX_LENGTH = 40
    
    GOOGLE_APPLICATION_CREDENTIALS = envget('GOOGLE_APPLICATION_CREDENTIALS')
    PROJECT_ID = envget('PROJECT_ID')
