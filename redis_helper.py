import os

import initial_data
import redis

#redis_url = os.environ.get('REDISTOGO_URL', 'redis://localhost:6379')
redis_url = "redis://redistogo:978270a2f8107277a484e05008366235@crestfish.redistogo.com:9240/"
redis_object = redis.from_url(redis_url, decode_responses=True)

def initialize_data():
    data = initial_data.data
    for key, value in data.items():
        success = redis_object.set(key, value)
        if not success:
            print("Was not able to set " + key)

def get_value(key):
    return redis_object.get(key)

def get_keys():
    return redis_object.keys()

def set_key_value(key, value):
    return redis_object.set(key, value)

def get_list(key):
    redis_list = []
    for i in range(0, redis_object.llen(key)):
        redis_list.append(redis_object.lindex(key, i))
    return redis_list

def append_to_list(key, value):
    return redis_object.lpush(key, value)

def delete_key(key):
    redis_object.delete(key)

def delete_all_keys():
    for key in redis_object.keys():
        redis_object.delete(key)
