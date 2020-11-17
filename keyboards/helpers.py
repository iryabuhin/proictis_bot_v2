import ujson

EXIT_BUTTON = {
    'text': 'Выйти',
    'color': 'negative',
    'payload': ujson.dumps({'command': 'exit'})
}

RESET_DIALOG_KEYBOARD = [
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

EMPTY_KEYBOARD = []
