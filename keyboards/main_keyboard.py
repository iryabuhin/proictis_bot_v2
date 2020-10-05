import ujson

MAIN_MENU_KEYBOARD = [
    [
        {
            'text': 'Наставники Проектного офиса',
            'color': 'primary',
            'payload': ujson.dumps({'selection': 'mentors'})
        }
    ],
    [
        {
            'text': 'Новости',
            'color': 'primary',
            'payload': ujson.dumps({'selection': 'news'})
        },
        {
            'text': 'ЧаВо',
            'color': 'primary',
            'payload': ujson.dumps({'selection': 'faq'})
        }
    ],
    [
        {
            'text': 'Помощь',
            'color': 'positive',
            'payload': ujson.dumps({'selection': 'help'})
        }
    ]
]