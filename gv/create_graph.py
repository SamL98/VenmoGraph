from graphviz import Graph

dot = Graph(comment='Venmo Transactions')
with open('payments.txt') as f:
	text = f.read()

pairs = text.split(',')
pairs[-1] = pairs[-1][:-1]

people = []
for pair in pairs:
	ps = pair.split(':')
	if ps[0] in people:
		ix1 = people.index(ps[0])
	else:
		people.append(ps[0])
		ix1 = len(people)-1
		dot.node(str(ix1), ps[0])

	if ps[1] in people:
		ix2 = people.index(ps[1])
	else:
		people.append(ps[1])
		ix2 = len(people)-1
		dot.node(str(ix2), ps[1])

	dot.edge(str(ix1), str(ix2))

dot.render('test.gv', view=True)
