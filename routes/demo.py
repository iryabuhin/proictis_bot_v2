from datetime import datetime
from vkbottle import Message
from vkbottle.bot import Blueprint
from vkbottle.types import GroupJoin, WallPostNew

bp = Blueprint(name='Тестируем работу с ивентами группы',
               description='Приветствует пользователя при вступлении в группу')

@bp.on.event.group_join()
async def group_join_handler(event: GroupJoin):
    uid = event.user_id
    fist_name = await bp.api.users.get(user_ids=uid).first_name
    await Message('Привет, {}. Спасибо за подписку!'
                  .format(fist_name),
                  )


@bp.on.message(text='тест', lower=True)
async def wrapper(ans: Message):
    return "лонгполл работает"

@bp.on.event.wall_post_new()
async def wrapper(event: WallPostNew):
    uid = event.from_id
    first_name = (await bp.api.users.get(uid))[0].first_name

    print('New post by {}: {}'
          .format(first_name, event.text)
        )

    msg = '[{}] Пост "{}"'.format(
        datetime.utcfromtimestamp(int(event.date)).strftime('%Y-%m-%d %H:%M:%S'),
        event.text
    )
    await bp.api.messages.send(
        peer_id=uid,
        message=msg,
        random_id=bp.extension.random_id()
    )
