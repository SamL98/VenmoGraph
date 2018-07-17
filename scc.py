import networkx as nx
import pymysql
from db import *

conn, cur = create_conn()

cur.execute('select id, sender, receiver from Payment')
pmts = cur.fetchall()

G = nx.MultiDiGraph()
for pmt in pmts:
    G.add_edge(pmt['sender'], pmt['receiver'])

for wcc in nx.weakly_connected_component_subgraphs(G):
    cur.execute('insert into Component (strong, count) values (false, %d)' % len(wcc.nodes()))
    cur.execute('select LAST_INSERT_ID()')
    comp_id = cur.fetchone()['LAST_INSERT_ID()']

    query = 'update Person set weak_comp=%d where' % comp_id
    for i, id in enumerate(wcc.nodes()):
        query += ' id=%d' % id
        if i < len(wcc.nodes())-1:
            query += ' or'
    cur.execute(query)

for scc in nx.strongly_connected_component_subgraphs(G):
    cur.execute('insert into Component (strong, count) values (true, %d)' % len(scc.nodes()))
    cur.execute('select LAST_INSERT_ID()')
    comp_id = cur.fetchone()['LAST_INSERT_ID()']

    query = 'update Person set strong_comp=%d where' % comp_id
    for i, id in enumerate(scc.nodes()):
        query += ' id=%d' % id
        if i < len(scc.nodes())-1:
            query += ' or'
    cur.execute(query)

conn.commit()
close_conn(conn, cur)