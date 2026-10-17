"""Record review input versions and Git checks; never change daily deliveries."""
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(argv, stdin=None):
    result = subprocess.run(argv, cwd=ROOT, input=stdin, text=True,
                            capture_output=True, encoding='utf8', errors='replace',
                            timeout=60)
    return {'argv': argv, 'exit_code': result.returncode,
            'stdout': result.stdout, 'stderr': result.stderr}


def main():
    sys.stdout.reconfigure(encoding='utf8')
    manifest = json.loads((ROOT / 'docs/tasks/manifest.json').read_text(encoding='utf8'))
    first = json.loads((HERE / 'command-01.json').read_text(encoding='utf8'))
    protected = {p: digest(Path(p)) for p in first['protected_before_sha256']}
    assert protected == first['protected_before_sha256'], 'Protected input changed since first review command'

    formal = set()
    for task in manifest['tasks'][5:25]:
        for relative in task['deliverables']:
            path = ROOT / relative
            formal.update([path] if path.is_file() else (p for p in path.rglob('*') if p.is_file()))
    review = {p for p in HERE.iterdir() if p.is_file()}
    # These evidence files are created after this check; probe their exact paths too.
    planned = {HERE / name for name in ('closeout.json', 'command-06.json', 'command-07.json')}
    relative_paths = sorted(p.relative_to(ROOT).as_posix() for p in formal | review | planned)
    ignore = command(['git', 'check-ignore', '--stdin'], '\n'.join(relative_paths) + '\n')
    assert ignore['exit_code'] == 1 and not ignore['stdout'], ignore

    status = command(['git', 'status', '--short', '--ignored', '--untracked-files=all', '--', '.'])
    worktree = command(['git', 'diff', '--check', '--', '.'])
    index = command(['git', 'diff', '--cached', '--check', '--', '.'])
    assert all(c['exit_code'] == 0 for c in (status, worktree, index))
    cache_paths = command(['rg', '--files', '--hidden', '--no-ignore',
                           '-g', '*.pyc', '-g', '*.pyo', '-g', '**/__pycache__/**',
                           '-g', '**/.pytest_cache/**', '-g', '**/.mypy_cache/**',
                           '-g', '**/.ruff_cache/**', '-g', '**/.venv/**',
                           '-g', '*.tmp', '-g', '*.log', '-g', '~$*', '.'])
    assert cache_paths['exit_code'] in (0, 1), cache_paths

    inputs = {ROOT / 'docs/tasks/manifest.json', ROOT / 'scripts/check_workspace.py'}
    for folder in ('algorithm/src', 'algorithm/schemas', 'algorithm/tests',
                   'algorithm/release/演示版/src', 'algorithm/release/演示版/schemas'):
        inputs.update(p for p in (ROOT / folder).iterdir() if p.is_file() and p.suffix in ('.py', '.json'))
    inputs.update(ROOT / f'docs/tasks/D{n:02}.md' for n in range(6, 26))
    inputs.update(review)
    review_prefix = HERE.relative_to(ROOT).as_posix() + '/'
    outside = [line for line in status['stdout'].splitlines()
               if not line.startswith('!! ') and not line[3:].startswith(review_prefix)]
    classification = {'.py': 'reproducible review tool or independent counterexample',
                      '.json': 'measured command, diagnostic, integrity, or Git evidence',
                      '.md': 'workspace maintenance review report'}
    retained = {p.relative_to(ROOT).as_posix(): classification[p.suffix] for p in review | planned}
    whitespace = {p.relative_to(ROOT).as_posix(): [n for n, line in enumerate(
                  p.read_text(encoding='utf8').splitlines(), 1) if line.rstrip(' \t') != line]
                  for p in review}
    assert not any(whitespace.values()), whitespace
    result = {'schema_version': 'review-closeout-1.0',
              'timestamp': datetime.now().astimezone().isoformat(),
              'scope': 'D06-D25 review evidence only; no implementation or progress update',
              'cwd': str(ROOT), 'python_executable': sys.executable,
              'python': sys.version, 'platform': platform.platform(),
              'protected_sha256': protected, 'protected_unchanged_since_command_01': True,
              'input_and_review_sha256': {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(inputs)},
              'git_status': status, 'git_diff_check': worktree, 'git_cached_diff_check': index,
              'git_check_ignore': {**ignore, 'stdin_paths': relative_paths},
              'outside_review_status_entries': outside,
              'ignored_status_entries': [s for s in status['stdout'].splitlines() if s.startswith('!! ')],
              'cache_temp_log_path_search': cache_paths,
              'workspace_gitignore_exists': (ROOT / '.gitignore').exists(),
              'new_file_classification': retained,
              'classification_counts': dict(Counter(retained.values())),
              'review_trailing_whitespace_lines': {k: v for k, v in whitespace.items() if v},
              'limitations': 'Hashes record the reviewed current versions. Planned evidence files are excluded from hashes to avoid circular content; their ignore paths are checked. Git checks do not prove behavioral acceptance.'}
    with (HERE / 'closeout.json').open('x', encoding='utf8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'protected_unchanged': True, 'git_diff_check': worktree['exit_code'],
                      'git_cached_diff_check': index['exit_code'], 'not_ignored_paths': len(relative_paths),
                      'outside_review_status_entries': outside,
                      'ignored_status_count': len(result['ignored_status_entries']),
                      'cache_temp_log_paths': cache_paths['stdout'].splitlines()}, ensure_ascii=False))


if __name__ == '__main__':
    main()
