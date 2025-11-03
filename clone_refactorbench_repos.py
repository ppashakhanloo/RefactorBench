import json, sys, os

dataset_file = sys.argv[1]

repositories = {
  'ansible/ansible': 'ansible_refactor',
  'celery/celery': 'celery_refactor',
  'django/django': 'django_refactor',
  'tiangolo/fastapi': 'fastapi_refactor',
  'pallets/flask': 'flask_refactor',
  'psf/requests': 'requests_refactor',
  'saltstack/salt': 'salt_refactor',
  'scrapy/scrapy': 'scrapy_refactor',
  'tornadoweb/tornado': 'tornado_refactor'
}

with open(dataset_file, 'r') as f:
  dataset = json.loads(f.read())

if not os.path.exists('repositories'):
  os.system('git clone https://github.com/ppashakhanloo/RefactorBench')
  os.system('cp -r RefactorBench/repositories . && rm -rf RefactorBench')

  print('>>> CLONED THE MOTHER REPOSITORY! <<<')

  for rep in repositories.values():
    os.system(f'cd repositories/{rep} && git init')
    os.system(f'cd repositories/{rep} && git add . && git commit -m "initial"')

  for item in dataset:
    os.system(f'cd repositories/{repositories[item['repo']]} && git checkout -b {item['instance_id']} && git checkout main')

print('>>> FINISHED SETTING UP THE GIT REPOS! <<<')

from tqdm import tqdm

for item in tqdm(dataset):
  os.system(f'mkdir -p results/workspaces/{item['repo']}')
  os.system(f'rm -rf results/workspaces/{item['repo']}/commit-{item['base_commit']} && cp -r repositories/{repositories[item['repo']]} results/workspaces/{item['repo']}/commit-{item['base_commit']}')
