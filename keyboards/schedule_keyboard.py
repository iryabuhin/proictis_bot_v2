import ujson
from keyboards import EXIT_BUTTON

SCHEDULE_KEYBOARD = [
    [
        {
            'text': 'Пред. день',
            'color': 'primary',
            'payload': ujson.dumps({'day': 'prev'})
        },
        {
            'text': 'След. день',
            'color': 'primary',
            'payload': ujson.dumps({'day': 'next'})
        }
    ],
    [
        {
            'text': 'Дни недели',
            'color': 'primary',
            'payload': ujson.dumps({'week': 'show_weekdays'})
        }
    ],
    [
        {
            'text': 'Пред. неделя',
            'color': 'positive',
            'payload': ujson.dumps({'week': 'prev'})
        },
        {
            'text': 'След. неделя',
            'color': 'positive',
            'payload': ujson.dumps({'week': 'next'})
        }
    ],
    [
        EXIT_BUTTON
    ]
]