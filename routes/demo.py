from vkbottle import Message
from vkbottle.bot import Blueprint

from models.user_state import PostgresStoredBranch

bp = Blueprint()
bp.branch = PostgresStoredBranch()

@bp.on.message(text='тест', lower=True)
async def wrapper(ans: Message):
    return "лонгполл работает"
