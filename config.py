from utils import envget
from dotenv import load_dotenv
from urllib.parse import urlparse
import os

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

    SCHEDULE_URL = 'http://165.22.28.187/schedule-api/'

    REDIS_URL = envget('REDIS_URL') or '127.0.0.1:6379'

    REDIS_ENDPOINT = urlparse(REDIS_URL).hostname
    REDIS_PORT = urlparse(REDIS_URL).port
    
    GOOGLE_APPLICATION_CREDENTIALS = envget('GOOGLE_APPLICATION_CREDENTIALS')
    PROJECT_ID = envget('PROJECT_ID')
