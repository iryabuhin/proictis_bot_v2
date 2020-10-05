import ujson

EXIT_BUTTON = {
    'text': 'Выйти',
    'color': 'negative',
    'payload': ujson.dumps({'command': 'exit'})
}
