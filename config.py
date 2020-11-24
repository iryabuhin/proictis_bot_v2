from dotenv import load_dotenv
from urllib.parse import urlparse
import os.path

load_dotenv()


class Config:
    DEBUG = os.environ.get('DEBUG') or True

    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    API_BACKUP_LOCATION = os.path.join(BASEDIR, os.path.join('content', 'proictis_api'))
    TOKEN = os.environ.get('TOKEN') or  None
    DATABASE_URL = os.environ.get('DATABASE_URL') or "sqlite://users.db"
    BASE_API_URL = 'https://proictis.sfedu.ru'
    PORT = int(os.environ.get('PORT') or 5555)

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
        'requests': '/api/me/requests'
    }

    NEWS_PER_MSG = 4
    NEWS_TITLE_MAX_LENGTH = 40

    SCHEDULE_URL = 'http://165.22.28.187/schedule-api/'

    REDIS_URL = os.environ.get('REDIS_URL') or '127.0.0.1:6379'

    REDIS_ENDPOINT = urlparse(REDIS_URL).hostname
    REDIS_PORT = urlparse(REDIS_URL).port
    REDIS_USERNAME = urlparse(REDIS_URL).username
    REDIS_PASSWORD = urlparse(REDIS_URL).password
    
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    PROJECT_ID = os.environ.get('PROJECT_ID')

    PROICTIS_LOGIN = os.environ.get('PROICTIS_LOGIN')
    PROICTIS_PASSWORD = os.environ.get('PROICTIS_LOGIN')

    USE_MIDDLEWARE = os.environ.get('USE_MIDDLEWARE') or False
