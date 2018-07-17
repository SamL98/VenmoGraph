import json
import sys

pfile = open('payments_expanded.txt', 'r')
jfile = open('payments.json', 'w')

people = []
nodes = []
links = []

def idxs(t):
    prev = 0
    ixs = []
    while ',' in t[prev:]:
        ixs.append(t.index(',', prev))
        prev = ixs[-1]+1
    return ixs

for payment in pfile:
    ixs = idxs(payment)
    frm, to = payment[:ixs[0]], payment[ixs[0]+1:ixs[1]]
    d = payment[ixs[1]+1:ixs[2]]
    if d == 'charged':
        frm, to = to, frm
    cap = payment[ixs[-1]+2:-2]

    for name in [to, frm]:
        if not name in people:
            people.append(name)
            nodes.append({'name': name})

    links.append({
        'source': people.index(frm),
        'target': people.index(to),
        'weight': 1
    })

data = {
    'nodes': nodes,
    'links': links
}
jfile.write(json.dumps(data))

pfile.close()
jfile.close()