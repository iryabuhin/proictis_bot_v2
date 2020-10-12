from config import Config

CACHE_CONFIG = {
    'default': {
        'cache': 'aiocache.RedisCache',
        'endpoint': '127.0.0.1',
        'port': 6379,
        'timeout': 1,
        'serializer': {
            'class': 'aiocache.serializers.PickleSerializer'
        },
        'plugins': [
            {'class': 'aiocache.plugins.HitMissRatioPlugin'},
            {'class': 'aiocache.plugins.TimingPlugin'}
        ]
    },
    'redis': {
        'cache': 'aiocache.RedisCache',
        'endpoint': Config.REDIS_ENDPOINT,
        'port': Config.REDIS_PORT,
        'timeout': 1,
        'serializer': {
            'class': 'aiocache.serializers.PickleSerializer'
        },
        'plugins': [
            {'class': 'aiocache.plugins.HitMissRatioPlugin'},
            {'class': 'aiocache.plugins.TimingPlugin'}
        ]
    }
}
