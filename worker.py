from redis import Redis
from rq import Queue, Worker

redis = Redis('redis', 6379)
queue = Queue('', connection=redis)
worker = Worker([queue], connection=redis, name='foo')
worker.work()