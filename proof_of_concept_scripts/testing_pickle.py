class Repository:
    def __init__(self, url, filters_rules):
        
        self.url = url

        labels_rules = filters_rules['labels']
        
        self.must_have_labels = set(labels_rules['must_have'])
        self.blocklist_labels = set(labels_rules['blocklist_labels'])

        self.name = url.split('/')[1].replace('.', '')
        self.dataset_file = 'datasets/' + self.name + '.csv'
        self.chart_name = 'graph/' + self.name + '.png'
        self.chart_name_linear = 'graph/' + self.name + 'linear_regression' + '.png'


filters_rules = {
        'labels': {
            'must_have': ['bug'],
            'blocklist_labels': []
        }
    }

GITHUB_TOKEN = ''
r = Repository('vuejs/vue', filters_rules)

import github
import pickle

g = github.Github(GITHUB_TOKEN)
conn = g.get_repo(r.url)

with open('testing.pickle', 'rb') as f:
    all_issues = pickle.load(f)

for i, issue in enumerate(all_issues):
    print(i, issue, remaining)

    for j, label in enumerate(issue.labels):
        print("  ", j, label, remaining)


# all_issues = conn.get_issues(
#     state='all',  # closed and open
#     # get only issues with must_have_labels
#     labels=list(r.must_have_labels),
#     direction='asc'  # oldest issue to newest
# )

# print(all_issues.totalCount)
# local_issues = []
# for i, issue in enumerate(all_issues):
#     local_issues.append(issue)
#     print(i, issue)
# print('\n\n\n')
with open('testing.pickle', 'wb') as f:
    pickle.dump(local_issues, f)
