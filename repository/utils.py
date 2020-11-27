import io
from collections import Counter
import string
import random

from rq import get_current_job

from github import Github

import matplotlib.pyplot as plt

from config.settings import image_bucket, BUCKET_NAME

import scipy.stats as ss

from reliability.Fitters import Fit_Weibull_2P
from reliability.Utils import generate_X_array

import django_rq

from .models import Repository, Issue, Label, AsyncTask
from django.core.management.utils import get_random_secret_key


def get_filted_issues(repository, must_not_have_labels):
    return repository.issues.exclude(
        labels__in=Label.objects.filter(
            name__in=must_not_have_labels
        )
    )

def get_months(issues):
    dates = []

    for issue in issues:
        date = issue.created_at.replace(day=1, hour=0, minute=0, second=0)
        dates.append(date)

    dates = sorted(dates)

    months = []
    prev_date = None
    years_counter = 0

    for date in dates:
        if prev_date != None:
            years_counter += (date.year - prev_date.year)

        prev_date = date
        month = years_counter * 12 + date.month
        months.append(month)

    return[month-months[0]+1 for month in months]


def get_random_slug(size=10, chars=string.ascii_uppercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def process(repository, must_not_have_labels):
    img_bytes = get_image(repository, must_not_have_labels)
    image_hash_name = get_random_slug() + '.png'

    # TODO: WHEN DEGUG==TRUE SAVE ON ANOTHER PLACE
    image_bucket.put_object(
        Body=img_bytes, 
        ContentType='image/png', 
        Key=image_hash_name,
        ACL='public-read'
    )

    img_url = f'https://{BUCKET_NAME}.s3-sa-east-1.amazonaws.com/{image_hash_name}'

    return img_url


def process_async(github_token, url, must_have_labels, must_not_have_labels):
    job = get_current_job()
    job.meta['ERRORS_MSG'] = []
    job.meta['ERRORS'] = False
    job.save_meta()

    task = AsyncTask.objects.create(
        id=job.get_id(),
        url=url,
        must_have_labels=must_have_labels,
        must_not_have_labels=must_not_have_labels,
        failed=False,
        finished=False
    )

    try:
        repository = import_filtered_issues(
            github_token, 
            url, 
            must_have_labels, 
            must_not_have_labels
        )
    except Exception as e:
        # print('here ' * 10)
        # print('e', e)
        task.failed = task.finished = True
        task.save()
        return

    # print('\n'*3)
    # print('BEFORE process')
    # print('\n'*3)
    img_url = process(repository, must_not_have_labels)
    # print('\n'*3)
    # print('AFTER process')
    # print('\n'*3)
    
    task.image = img_url
    task.finished = True
    task.save()

    job.meta['progress'] = '100%'
    job.save_meta()


def get_image(repository, must_not_have_labels):
    issues = get_filted_issues(repository, must_not_have_labels)

    months = get_months(issues)
    
    hist = Counter(months)
    axis_y = [hist[month] for month in months]

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Meses')
    ax1.set_ylabel('Bugs reportados', color='tab:red')
    ax1.plot(months, axis_y, color='tab:red')

    repository_name = repository.url.replace('https://github.com/', '')

    plt.suptitle('Padrão de chegada de issues de\nBug do Repositório %s' % (repository_name))

    wb = Fit_Weibull_2P(
        failures=months,
        show_probability_plot=False,
        print_results=False
    )

    weibull = wb.distribution

    X = generate_X_array(dist=weibull, xvals=None, xmin=None, xmax=None)
    Y = ss.weibull_min.pdf(X, weibull.beta, scale=weibull.alpha, loc=weibull.gamma)

    count = len([i for i in X if i < months[-1]+1])

    X = X[:count]
    Y = Y[:count]

    ax2 = ax1.twinx()
    ax2.set_ylabel('Função de densidade de probabilidade de Weibull', color='tab:blue')
    ax2.plot(X, Y, color='tab:blue')

    fig.tight_layout()

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    return img_bytes


        
"""
    This function get all valid issues and saves on database
"""
def import_filtered_issues(github_token, url, must_have_labels, must_not_have_labels):
    g = Github(login_or_token=github_token)

    repo_name = url.replace('https://github.com/', '')
    repo_name = repo_name[:-1] if repo_name[-1] == '/' else repo_name

    job = get_current_job()

    try:
        conn = g.get_repo(full_name_or_id=repo_name)
    except Exception as e:
        job.meta['ERRORS'] = True
        job.meta['ERRORS_MSG'].append(
            'The defined url does not belong to a public github repository.'
        )
        job.save_meta()
        raise
        
    all_issues = conn.get_issues(state='all', labels=must_have_labels, direction='asc')
    # print('\n'*3)
    # print('all_issues.totalCount', all_issues.totalCount)
    # print('\n'*3)

    r = Repository.objects.get(
        url=url,
        must_have_labels=str(sorted(list(set(must_have_labels))))
    )

    if all_issues.totalCount < 100:
        # print('inside 100 validation'*4)
        job.meta['ERRORS'] = True
        job.meta['ERRORS_MSG'].append(
            f'With the issue filters defined, it was possible to select only {all_issues.totalCount} issues, with the minimum required being 100.'
        )
        job.save_meta()
        r.delete()
        raise Exception

    # print('after 100 validation'*4)
    total = job.meta['total_of_issues'] = all_issues.totalCount
    job.save_meta()

    for i, issue in enumerate(all_issues):
        if(issue.pull_request):
            continue

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

        job.meta['progress'] = str(int(((i/total)*10000))/100) + '%'
        job.meta['issues_processed'] = i
        job.save_meta()

    return r