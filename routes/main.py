from vkbottle.bot import Blueprint, Message
from vkbottle.branch import ClsBranch, rule_disposal, Branch, ExitBranch
from vkbottle.keyboard import Keyboard, Text, OpenLink, keyboard_gen
from vkbottle.rule import LevenshteinDisRule, PayloadRule, VBMLRule, EventRule, Pattern, CommandRule, Any
from models.user_state import PostgresStoredBranch
import ujson

MAIN_LOOP_KEYBOARD = [
    [
        {
            "type": "text",
            "label": "Наставники",
            "payload": "{\"selection\": \"mentors\"}",
            "color": "primary"
        }
    ],
    [
        {
            "type": "text",
            "label": "Проекты",
            "payload": "{\"selection\": \"projects\"}"
        }
    ]
]

bp = Blueprint(name='main')
bp.branch = PostgresStoredBranch()

# def make_main_keyboard():
#     k = Keyboard(one_time=True)
#     k.add_row()
#     k.add(
#         Text(
#             label='Наставники',
#             payload=ujson.dumps({'selection': 'mentors'})
#         ),
#         color='primary',
#     )
#     k.add_row()
#     k.add(
#         Text(
#             label='Проекты',
#             payload=ujson.dumps({'selection': 'projects'})
#         ),
#         color='primary'
#     )
#     return k.generate()


@bp.on.message(PayloadRule({'command': 'start'}))
async def wrapper(ans: Message):
    await ans('Здравствуйте! Я - чат-бот Проектного офиса ИКТИБ '
              'и я здесь чтобы предоставить вам информацию о наставниках, '
              'доступных проектах и многом другом.\n'
              'Помимо этого, я могу напоминать вам о предстоящих дедлайнах,'
              'связанных с проектной деятельностью, а также уведомлять вас о новостях'
              'из жизни Проектного офиса. \n'
              'Если у вас возникнут какие-либо вопросы, нажмите кнопку "Помощь"',
              keyboard=keyboard_gen(MAIN_LOOP_KEYBOARD)
              )
    await bp.branch.add(uid=ans.from_id, branch='main')


@bp.on.message(CommandRule('reset_user'))
async def reset_branch(ans: Message):
    kbrd = [
        [
            {
                'text': 'Сбросить состояние диалога',
                'payload': "{\"command\": \"start\"}",
                'color': 'primary'
            }
        ],
        [
            {
                'text': 'Отмена',
                'payload': "{\"command\": \"cancel_reset\"}"
            }
        ]
    ]
    await ans(
        'Это сбросит состояние вашего диалога с ботом.'
        'Нажмите кнопку "Сбросить состояние диалога" чтобы подтвердить действие '
        'и "Отмена" для отмены действия.',
        keyboard=keyboard_gen(kbrd, one_time=True),
        payload="{}"
    )


class MainBranch(ClsBranch):

    async def branch(self, ans: Message, *args):
        await ans(
            message='Ты сейчас в основном бранче',
            payload=ujson.dumps({'selection': 'mentors'})
        )

    @rule_disposal(
        PayloadRule({"selection": "mentors"}),
        VBMLRule('наставники', lower=True)
    )
    async def mentors(self, ans: Message):
        await bp.branch.add(ans.peer_id, 'mentors')

    @rule_disposal(
        VBMLRule('test', lower=True)
    )
    async def wrapper(self, ans: Message, **kwargs):
        await ans(
            'Выберите одну из опций:',
            keyboard=make_main_keyboard()
        )


    @rule_disposal(
        PayloadRule(
            {
                "selection": "projects"
            }
        ),
        VBMLRule('проекты', lower=True)
    )
    async def projects(self, ans: Message):
        await bp.branch.add(ans.peer_id, 'projects')


@bp.on.message(CommandRule('test_bp_branches'))
async def wrapper(ans: Message):
    await bp.branch.add(
        uid=ans.from_id,
        branch='main'
    )


class ProjectInfoStubBranch(ClsBranch):
    async def branch(self, ans: Message, *args):
        await ans('[DEBUG] Branch ProjectInfoStubBranch, reply "exit" to exit (duh)')

    @rule_disposal(
        VBMLRule('exit', lower=True)
    )
    async def exit_branch(self, ans: Message):
        await ans('[DEBUG] Exiting branch...')
        await bp.branch.exit(ans.peer_id)


bp.branch.add_branch(
    MainBranch,
    'main'
)
bp.branch.add_branch(
    ProjectInfoStubBranch,
    'projects'

)


bp.branch.add_branch(MainBranch, 'main')
bp.branch.add_branch(ProjectInfoStubBranch, 'projects')
