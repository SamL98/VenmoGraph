from graphviz import Graph
from db import *

dot = Graph(comment='Venmo Transactions')

conn, cur = create_conn()
cur.execute('select id, name from Person where strong_comp=4423')
people = cur.fetchall()
print('%d people' % len(people))

ids = [p['id'] for p in people]
names = [p['name'] for p in people]

for id, name in zip(ids, names):
	dot.node(str(id), name)

pmt_ids = []
for i, id in enumerate(ids):
	if i % 500 == 0:
		print('%d / %d' % (i, len(ids)))

	cur.execute('select id, sender, receiver, caption\
		from Payment where\
		sender={0} or receiver={0}'.format(id))
	pmts = cur.fetchall()

	for pmt in pmts:
		if pmt['id'] in pmt_ids:
			continue

		pmt_ids.append(pmt['id'])
		dot.edge(str(pmt['sender']), str(pmt['receiver']), label=pmt['caption'])

dot.render('venmo_scc.gv', view=True)
close_conn(conn, cur)