from config.settings import queue

job = queue.enqueue('_app.tasks.testing', 1, 'abc', ['a', 'b'], 'd')

print(job.get_id())
print(job.is_finished)

job.refresh()
print(job.meta)

job.refresh()
print(job.meta)