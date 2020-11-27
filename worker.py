import redis
import os
from dotenv import load_dotenv
from rq import Worker, Queue, Connection

load_dotenv()

conn = redis.Redis(
    host=os.environ.get('REDIS_HOST', None),
    port=os.environ.get('REDIS_PORT', None),
    password=os.environ.get('REDIS_PASSWORD', None),
)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, ['default']))
        worker.work()