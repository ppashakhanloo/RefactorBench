import json, sys, os

dataset = dict()

with open('refactorbench_dataset.json', 'r') as f:
  obj = json.loads(f.read())
  for item in obj:
    dataset[item['instance_id']] = item

# artifacts_dir = sys.argv[1]

artifacts_dir = '/Users/ppardis/kiro-benchmarking/src/KiroScienceEvaluation/eval/kiro_0.5.0_refactorbench_baseline'
workspaces_dir = '/Users/ppardis/kiro-benchmarking/src/KiroBenchmarkingTestRunner/results/workspaces'

all_samples = 0
passed = 0

for sample in os.listdir(artifacts_dir):
  if sample == '.DS_Store': continue
  print('EXECUTION ENV FOR', sample)
  id = sample.strip().replace('polybench_', '')
  repo = dataset[id]['repo']
  commit = dataset[id]['base_commit']
  diff_path = f'{artifacts_dir}/{sample}/run-1/agent-diff'
  local_repo = f"{workspaces_dir}/{repo}/commit-{commit}"
  os.system(f'cd {local_repo} && git reset --quiet && git clean --quiet -fdx && git reset --quiet --hard "{commit}"')
  os.system(f'cd {local_repo} && git apply --whitespace=nowarn --quiet --ignore-whitespace {diff_path}')
  with open(f'{local_repo}/hidden-test-patch.diff', 'w') as f:
    f.write(dataset[id]['test_patch']+'\n')
  os.system(f'cd {local_repo} && git apply --quiet --whitespace=nowarn --ignore-whitespace hidden-test-patch.diff')
  os.system(f'cd {local_repo} && python3 -m pip install -q . 2> /dev/null')

  test_command = dataset[id]['test_command']
  status = os.system(f'cd {local_repo} && {test_command} -q 2> /dev/null')

  all_samples += 1
  if status == 0:
    passed += 1
  print('=========================')

print('passed:', passed)
print(' total:', all_samples)
print('      =', passed/all_samples*100, '%')
