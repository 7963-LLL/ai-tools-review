#!/usr/bin/env python3
"""Push HEAD tree via Git Data API (github.com:443 blocked from this host; api.github.com reachable)."""
import base64, json, os, subprocess, sys, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

TODAY = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')

REPO = '7963-LLL/ai-tools-review'
BRANCH = 'master'
UA = 'Mozilla/5.0'

line = open(os.path.expanduser('~/.git-credentials'), encoding='utf-8').read().splitlines()[0]
pw = line.split('//', 1)[1].split('@', 1)[0].split(':', 1)[1]
HDRS = {'Authorization': 'Bearer ' + pw, 'Accept': 'application/vnd.github+json',
        'Content-Type': 'application/json', 'User-Agent': UA}

def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request('https://api.github.com' + path, data=data, headers=HDRS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit('%s %s -> %s %s' % (method, path, e.code, e.read().decode()[:300]))

files = subprocess.run(['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
                       capture_output=True, text=True).stdout.split()
if not files:
    raise SystemExit('no changed files')
print('files:', files)

ref = api('GET', '/repos/%s/git/ref/heads/%s' % (REPO, BRANCH))
base_sha = ref['object']['sha']
base = api('GET', '/repos/%s/git/commits/%s' % (REPO, base_sha))
print('base commit', base_sha[:8])

tree, local = [], {}
for f in files:
    data = open(f, 'rb').read()
    local[f] = data
    blob = api('POST', '/repos/%s/git/blobs' % REPO,
               {'content': base64.b64encode(data).decode(), 'encoding': 'base64'})
    if 'sha' not in blob:
        raise SystemExit('blob failed for %s: %s' % (f, blob))
    tree.append({'path': f, 'mode': '100755' if f.endswith('.py') else '100644',
                 'type': 'blob', 'sha': blob['sha']})
    print('blob', f, len(data), blob['sha'][:8])

new_tree = api('POST', '/repos/%s/git/trees' % REPO,
               {'base_tree': base['tree']['sha'], 'tree': tree})
commit = api('POST', '/repos/%s/git/commits' % REPO,
             {'message': '每日更新 ' + TODAY, 'tree': new_tree['sha'], 'parents': [base_sha]})
if 'sha' not in commit:
    raise SystemExit('commit failed: %s' % commit)
upd = api('PATCH', '/repos/%s/git/refs/heads/%s' % (REPO, BRANCH),
          {'sha': commit['sha'], 'force': False})
print('new commit:', commit['sha'], 'ref now:', upd.get('object', {}).get('sha'))

head = api('GET', '/repos/%s/git/ref/heads/%s' % (REPO, BRANCH))['object']['sha']
ok = head == commit['sha']
for entry in tree:
    r = api('GET', '/repos/%s/git/blobs/%s' % (REPO, entry['sha']))
    same = base64.b64decode(r['content']) == local[entry['path']]
    ok = ok and same
    print('verify', entry['path'], 'OK' if same else 'MISMATCH')
print('REMOTE HEAD', head)
print('ALL VERIFIED' if ok else 'VERIFY FAILED')
sys.exit(0 if ok else 1)
