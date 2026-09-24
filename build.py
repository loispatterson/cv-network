"""Rebuild graph.json from data.yaml and splice it into index.html.

    python3 build.py

Validates every id before writing: a typo in a link silently drops it otherwise.
"""
import yaml, json, sys
from datetime import date
from collections import defaultdict

d = yaml.safe_load(open('data.yaml'))
roles, nodes, links = d['roles'], d['nodes'], d['links']

ids = {n['id'] for n in nodes}
rids = {r['id'] for r in roles}
bad = [l for l in links if l['node'] not in ids or l['role'] not in rids]
seen, dup = set(), []
for l in links:
    k = (l['role'], l['node'])
    if k in seen: dup.append(k)
    seen.add(k)
if bad or dup:
    print("broken links:", bad); print("duplicates:", dup); sys.exit(1)

def years(r):
    """Whole years, rounded up. A three-month contract still needs a circle."""
    s = str(r['start']); e = r.get('end')
    sy, sm = int(s[:4]), int(s[5:7])
    if e is None: ey, em = date.today().year, date.today().month
    else: e = str(e); ey, em = int(e[:4]), int(e[5:7])
    m = (ey - sy) * 12 + (em - sm)
    return max(1, -(-m // 12))          # ceil

def mid(r):
    s = str(r['start']); a = int(s[:4]) + (int(s[5:7]) - 1) / 12
    e = r.get('end')
    b = (date.today().year + (date.today().month - 1) / 12) if e is None \
        else (int(str(e)[:4]) + (int(str(e)[5:7]) - 1) / 12)
    return round((a + b) / 2, 2)

byNode = defaultdict(set)
for l in links: byNode[l['node']].add(l['role'])
used = set(byNode)
orphans = [n['id'] for n in nodes if n['id'] not in used]

g = {"roles": [{**r, "years": r.get("years", years(r)), "mid": r.get("mid", mid(r))}
               for r in roles],
     "nodes": [{**n, "roles": len(byNode[n['id']])} for n in nodes if n['id'] in used],
     "links": [{k: v for k, v in l.items() if k != 'first'} for l in links]}
json.dump(g, open('graph.json', 'w'), indent=1, default=str)

s = open('index.html').read()
a = s.index("const DATA = "); b = s.index(";\n", a)
open('index.html', 'w').write(s[:a] + "const DATA = " + json.dumps(g) + s[b:])

print(f"{len(g['roles'])} roles, {len(g['nodes'])} nodes, {len(g['links'])} links")
if orphans: print("not drawn, no links:", ", ".join(orphans))
