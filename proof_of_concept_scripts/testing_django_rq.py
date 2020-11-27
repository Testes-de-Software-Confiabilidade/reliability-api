from repository.models import Repository
from rq import get_current_job

def create(url, must):
    Repository.objects.create(
        url=url,
        must_have_labels = must,
    )
    job = get_current_job()
    job.meta['status'] = 'to aqui'
    job.save_meta()

