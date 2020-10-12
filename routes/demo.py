from vkbottle import Message
from vkbottle.bot import Blueprint

from models.user_state import DBStoredBranch

bp = Blueprint()
bp.branch = DBStoredBranch()

@bp.on.message(text='тест', lower=True)
async def wrapper(ans: Message):
    return "лонгполл работает"
