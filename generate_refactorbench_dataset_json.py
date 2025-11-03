import json, sys, os

dataset = []


repositories = {
  'ansible_refactor': ('ansible/ansible','00'),
  'celery_refactor': ('celery/celery','00'),
  'django_refactor': ('django/django','00'),
  'fastapi_refactor': ('tiangolo/fastapi','00'),
  'flask_refactor': ('pallets/flask','00'),
  'requests_refactor': ('psf/requests','00'),
  'salt_refactor': ('saltstack/salt','00'),
  'scrapy_refactor': ('scrapy/scrapy','00'),
  'tornado_refactor': ('tornadoweb/tornado','00')
}



for repo_dir in os.listdir('RefactorBench/problems/base_problems'):
  if repo_dir == '.DS_Store': continue
  for problem_name in os.listdir(f'RefactorBench/problems/base_problems/{repo_dir}'):
    if problem_name == '.DS_Store': continue
    with open(f'RefactorBench/problems/base_problems/{repo_dir}/{problem_name}') as f:
      ps = f.read().strip()
    os.system('rm -rf temp && mkdir temp')
    os.system(f'cd temp && git init && touch testfile')
    os.system(f'cd temp && git add . && git commit -m "commit"')
    os.system(f'cp RefactorBench/tests/{repo_dir}/{problem_name.replace('-task.txt', '-test.py')} temp/ && cd temp && git add . && git diff HEAD > patch.diff')
    with open('temp/patch.diff') as g:
      test_patch = g.read().strip()
    os.system('rm -rf temp')
    item = {
      "repo": repositories[repo_dir][0],
      "url": 'https://github.com/' + repositories[repo_dir][0],
      "instance_id": problem_name.replace('-task.txt', ''),
      "base_commit": problem_name.replace('-task.txt', ''),
      "patch": "N/A",
      "test_patch": test_patch,
      "problem_statement": ps,
      "hints_text": "",
      "created_at": "2025-11-03 22:46:32+00:00",
      "language": "Python",
      "Dockerfile": "N/A",
      "test_command": "python3 -m unittest " + problem_name.replace('-task.txt', '-test.py'),
      "task_category": "Refactoring",
      "data_source": "microsoft/RefactorBench",
      "scenario": "brownfield"
    }
    dataset.append(item)

with open('refactorbench_dataset.json', 'w') as f:
  f.write(json.dumps(dataset, indent=2))