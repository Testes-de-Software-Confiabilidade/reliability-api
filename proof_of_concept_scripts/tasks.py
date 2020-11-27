import time
from rq import get_current_job

def example(seconds):
    job = get_current_job()
    print('Starting task')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')


def testing(a, b, c, d):
    job =get_current_job()
    job.meta['a'] = a
    job.meta['b'] = b
    job.meta['c'] = c
    job.meta['d'] = d
    job.save_meta()
    time.sleep(2)