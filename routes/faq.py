from vkbottle import keyboard_gen
from vkbottle.bot import Blueprint, Message
from vkbottle.rule import PayloadRule, VBMLRule
from vkbottle.branch import ClsBranch, rule_disposal
from proictis_api.faq.handler_tools import detect_intent_texts
from google.api_core.exceptions import GoogleAPIError
from keyboards import MAIN_MENU_KEYBOARD, EXIT_BUTTON
from rules import ExitButtonPressed
from models import DBStoredBranch
from config import Config

bp = Blueprint(name='faq')
bp.branch = DBStoredBranch()


@bp.on.message(PayloadRule({'selection': 'faq'}))
async def faq_wrapper(ans: Message):
    await ans('Задавайте свои вопросы как будто спрашиваете человека'
              'и я попытаюсь найти на них ответ!',
              keyboard=keyboard_gen([[EXIT_BUTTON]])
              )
    await bp.branch.add(ans.from_id, 'faq')


class FaqDialogflowBranch(ClsBranch):
    async def branch(self, ans: Message, *args):
        try:
            query_result = detect_intent_texts(
                Config.PROJECT_ID,
                ans.from_id,
                ans.text,
                'ru-RU'
            )
        # TODO add logging
        except GoogleAPIError as e:
            raise GoogleAPIError(e)
        except ValueError as e:
            raise ValueError(e)
        else:
            msg = query_result.get('fulfillmentText')
            await ans(msg)

    @rule_disposal(ExitButtonPressed())
    async def exit_branch(self, ans: Message):
        await ans(
            message=f'[DEBUG] Exiting branch {self.__class__.__name__}',
            keyboard=keyboard_gen(MAIN_MENU_KEYBOARD, inline=True)
        )
        await bp.branch.exit(ans.from_id)


bp.branch.add_branch(FaqDialogflowBranch, 'faq')
