from repository.models import Repository, Issue, Label

model_list = [
    {
        'issue_data': {
            'closed_at':  '2020-11-30 10:39:10.587518',
            'created_at': '2020-10-30 10:39:10.587518',
            'html_url':   'https://www.w3schools.com/python/python_datetime.asp',
            'api_url':    'https://www.w3schools.com/python/python_datetime.asp',
            'is_closed':  True,
        },
        'related_labels': set()
    },
    {
        'issue_data': {
            'closed_at':  '2019-11-30 10:39:10.587518',
            'created_at': '2019-10-30 10:39:10.587518',
            'html_url':   'https://www.w3schools.com/',
            'api_url':    'https://www.w3schools.com/python',
            'is_closed':  False,
        },
        'related_labels': set()
    },
]

for l in ['naruto', 'sasuke']:
    model_list[0]['related_labels'].add(l)

for l in ['comp: ngcc', 'windows']:
    model_list[1]['related_labels'].add(l)

r = Repository.objects.get(
    url='https://stackoverflow.com/questions/24388297/how-to-save-list-of-objects-in-django-models',
    must_have_labels='["nice", "work"]'
)

labels_rel = []

rtn = Issue.objects.bulk_create(
    [Issue(repository=r, **d['issue_data']) for d in model_list]
)

for issue in rtn:
    issue.labels.bulk_create(
        [Label(name=name, issue=issue) for d in model_list for name in d['related_labels']],
        ignore_conflicts=True,
    )
