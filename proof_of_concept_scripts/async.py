from redis import Redis
import rq
import time

queue = rq.Queue('microblog-tasks', connection=Redis.from_url('redis://'))
job = queue.enqueue('app.tasks.example', 23)

job.get_id()

job.refresh()
print(job.meta)

time.sleep(1)

job.refresh()
print(job.meta)

