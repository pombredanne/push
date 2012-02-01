import redis

from push.storage.base import StorageBase


class Storage(StorageBase):
    q = 'push:q:1:'  # Queues.
    u = 'push:u:1:'  # Users.
    d = 'push:d:1:'  # Domains.
    a = 'push:a:1:'  # Android tokens.

    def __init__(self, **kw):
        self.redis = redis.Redis(**kw)

    def new_queue(self, queue, user, domain):
        self.redis.hmset(self.q + queue, {'user': user, 'domain': domain})
        self.redis.sadd(self.u + user, queue)
        self.redis.sadd(self.d + domain, queue)

    def user_owns_queue(self, user, queue):
        return self.redis.sismember(self.u + user, queue)

    def domain_owns_queue(self, domain, queue):
        return self.redis.sismember(self.d + domain, queue)

    def get_user_for_queue(self, queue):
        return self.redis.hget(self.q + queue, 'user')

    def set_queue_timestamp(self, queue, timestamp):
        current = self.get_queue_timestamp(queue)
        self.redis.hset(self.q + queue, 'timestamp', max(current, timestamp))

    def get_queue_timestamp(self, queue):
        return float(self.redis.hget(self.q + queue, 'timestamp') or 0)

    def set_android_id(self, user, droid_id):
        return self.redis.set(self.a + user, droid_id)

    def get_android_id(self, user):
        return self.redis.get(self.a + user)
