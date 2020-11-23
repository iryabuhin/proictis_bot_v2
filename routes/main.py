from vkbottle.bot import Blueprint, Message
from vkbottle.branch import ClsBranch, rule_disposal, Branch, ExitBranch
from vkbottle.keyboard import Keyboard, Text, OpenLink, keyboard_gen
from vkbottle.rule import PayloadRule, VBMLRule, EventRule, Pattern, CommandRule, Any
from keyboards import MAIN_MENU_KEYBOARD, EXIT_BUTTON, RESET_DIALOG_KEYBOARD, NEWS_WELCOME_KEYBOARD
from models.user_state import DBStoredBranch, UserState
from routes.faq import FaqDialogflowBranch
from routes.mentors import MentorInfoBranch
from routes.news import NewsBranch
from routes.schedule import ScheduleBranch

bp = Blueprint(name='main')
bp.branch = DBStoredBranch()


@bp.on.message(PayloadRule({'command': 'start'}))
async def wrapper(ans: Message):
    await ans('Здравствуйте! В этом чат-боте вы сможете найти '
              'информацию о наставниках, проектах, различных мероприятих '
              'и многом другом.\n'
              'Если у вас возникнут какие-либо вопросы, нажмите кнопку "Помощь"',
              keyboard=keyboard_gen(MAIN_MENU_KEYBOARD)
              )
    await bp.branch.add(uid=ans.from_id, branch='main')


@bp.on.message(CommandRule('reset_user'))
async def reset_branch(ans: Message):
    await ans(
        'Это сбросит состояние вашего диалога с ботом.'
        'Нажмите кнопку "Сбросить состояние диалога" чтобы подтвердить действие '
        'и "Отмена" для отмены действия.',
        keyboard=keyboard_gen(RESET_DIALOG_KEYBOARD, one_time=True),
        payload="{}"
    )

@bp.on.message(CommandRule('empty_keyboard'))
async def empty_keyboard(ans: Message):
    await ans('test', keyboard=keyboard_gen([]))

class MainBranch(ClsBranch):

    async def branch(self, ans: Message, *args):
        await ans(
            message='Главное меню',
            keyboard=keyboard_gen(MAIN_MENU_KEYBOARD, one_time=False)
        )

    # DRY? never heard of that
    @rule_disposal(PayloadRule({'command': 'start'}))
    async def start_command_wrapper(ans: Message):
        await ans('Здравствуйте! В этом чат-боте вы сможете найти '
                  'информацию о наставниках, проектах, различных мероприятих '
                  'и многом другом.\n'
                  'Если у вас возникнут какие-либо вопросы, нажмите кнопку "Помощь"',
                  keyboard=keyboard_gen(MAIN_MENU_KEYBOARD)
                  )
        await bp.branch.add(uid=ans.from_id, branch='main')

    @rule_disposal(PayloadRule({'selection': 'faq'}))
    async def faq_wrapper(self, ans: Message):
        await ans('Задавайте свои вопросы словно спрашиваете человека'
                  'и я попытаюсь найти на них ответ!',
                  keyboard=keyboard_gen([[EXIT_BUTTON]])
                  )
        await bp.branch.add(ans.from_id, 'faq')

    @rule_disposal(VBMLRule('test', lower=True))
    async def test(self, ans: Message):
        await ans(
            message='Выберите одну из опций:',
            keyboard=keyboard_gen(MAIN_MENU_KEYBOARD)
        )

    @rule_disposal(PayloadRule({'selection': 'schedule'}))
    async def schedule_enter(self, ans: Message):
        await ans('Введите ваш запрос - это может быть номер группы, аудитории или фамилия преподователя')
        await bp.branch.add(ans.from_id, 'schedule')

    @rule_disposal(PayloadRule({'selection': 'mentors'}))
    async def mentors_enter(self, ans: Message):
        await bp.branch.add(ans.from_id, 'mentors')
        await ans(
            'Вы можете узнать о наставнике отправив мне его/её фамилию.\n'
            'Если я смогу найти наставника с такой фамилией, я покажу вам информацию о нем'
            'и его контактные данные.',
            keyboard=keyboard_gen([[EXIT_BUTTON]], one_time=True)
        )

    @rule_disposal(VBMLRule('новости', lower=True))
    async def news_enter(self, ans: Message):
        await bp.branch.add(ans.from_id, 'news')
        await ans(
            'Нажмите "Далее", чтобы увидеть последние новости с сайта Проектного офиса или '
            '"Поиск" для интерактивного поиска по новостям Проектного офиса и группы ИКТИБ ВКонтакте',
            keyboard=keyboard_gen(NEWS_WELCOME_KEYBOARD, one_time=True)
        )

    @rule_disposal(PayloadRule({'selection': 'projects'}))
    async def projects(self, ans: Message):
        await bp.branch.add(ans.peer_id, 'projects')

    
    @rule_disposal(PayloadRule({'selection': 'help'}))
    async def help_message(self, ans: Message):
        await ans(
            message='''
            Управление чат-ботом осуществляется с помощью кнопок клавиатуры. В случае если клавиатура по какой-то причине не отображается, отправьте сообщение "выйти", чтобы вернуться в главное меню.

            Каждая кнопка в главном меню ведет в ветвь с соответствующим названию функционалом, управление в каждой ветви осуществляется также с помощью кнопок. 

            Ветвь "Наставники" позволяет узнать информацию о наставниках Проектного офиса,
            ветвь "Расписание" позволяет узнать расписание аудиторий, учебных групп и преподователей,
            ветвь "Новости" отображает последние новости Проектного офиса,
            а в ветви "ЧаВо" можно найти ответы на самые часто задаваемые вопросы о проектной деятельности. 
            ''',
            keyboard=keyboard_gen(MAIN_MENU_KEYBOARD)
        )


@bp.on.message(CommandRule('test_bp_branches'))
async def wrapper(ans: Message):
    await bp.branch.add(
        uid=ans.from_id,
        branch='main'
    )


bp.branch.add_branch(MainBranch, 'main')
bp.branch.add_branch(NewsBranch, 'news')
bp.branch.add_branch(MentorInfoBranch, 'mentors')
bp.branch.add_branch(FaqDialogflowBranch, 'faq')
bp.branch.add_branch(ScheduleBranch, 'schedule')

