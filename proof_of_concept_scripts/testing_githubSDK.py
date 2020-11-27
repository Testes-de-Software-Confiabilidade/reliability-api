from github import Github
from rq import get_current_job

from repository.models import Repository, Issue, Label


def is_valid(issue, block_list):
    for label in issue.labels:
        if label.name in block_list:
            return False
    return True



g = Github(login_or_token="")

conn = g.get_repo(
    full_name_or_id='vuejs/vue'
)

all_issues = conn.get_issues(
    state='all',
    labels=["bug", "has workaround", "has PR"],
    direction='asc'
)

# block_list = list(set([]))

filtered_issues = []
r = Repository.objects.get(
    url='https://github.com/vuejs/vue', must_have_labels='["bug", "has workaround"]'
)

total = all_issues.totalCount
job = get_current_job()

if job:
    job.meta['total_of_issues'] = total

for i, issue in enumerate(all_issues):
    if(issue.pull_request):
        continue
    # if(is_valid(issue, block_list) == False):
    #     continue
        
    created_issue = Issue.objects.create(
        repository=r,
        closed_at=issue.closed_at,
        created_at=issue.created_at,
        html_url=issue.html_url,
        api_url=issue.url,
        is_closed = True if issue.state=='closed' else False,
    )

    for label in issue.labels:
        query = Label.objects.filter(name=label.name)
        if not query.exists():
            db_label = Label.objects.create(name=label.name)
        else:
            db_label = query.first()

        created_issue.labels.add(db_label)

    perc = str(int(((i/total)*10000))/100) + '%'

    if job:
        job.meta['progress'] = perc
        job.meta['issues_processed'] = i
        job.save_meta()

if job:
    job.meta['valid_issues'] = len(filtered_issues)
    job.save_meta()
