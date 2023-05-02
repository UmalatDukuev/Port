from functools import wraps
from cache.connection import RedisCache


def fetch_from_cache(cache_name: str, cache_config: dict):
    cache_conn = RedisCache(cache_config['redis']) #подключились к Redis
    ttl = cache_config['ttl']

    def wrapper_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cached_value = cache_conn.get_value(cache_name) #извлекаем из кэша
            if cached_value:
                return cached_value
            response = f(*args, **kwargs)#если в кэше пусто, то берем из базы данных, в качестве f будем передавать select_dict
            cache_conn.set_value(cache_name, response, ttl=ttl)
            return response
        return wrapper
    return wrapper_func #возвращает декоратор