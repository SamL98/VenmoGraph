from db import *
import sys

conn, c = create_conn()
f = open('payments_expanded_fr.txt', 'r')

count = 0
buffer = ''

upto = 0
if len(sys.argv) > 1:
    upto = int(sys.argv[1])

for line in f:
    if count < upto:
        count += 1
        continue

    if len(line) < 2 or not line[-2] == '"':
        buffer += line
        continue
    elif len(buffer) > 0:
        buffer += line
        line = buffer
        buffer = ''

    if count > 0 and count % 10000 == 0:
        conn.commit()
        print('%d: committed' % count)
    elif count > 0 and count % 1000 == 0:
        print(count)

    if not ',' in line:
        print(count, line)
        break
    i = line.index(',')
    n1 = line[:i]

    c.execute('select * from Person where name="%s"' % n1)
    ps = c.fetchone()
    if ps is None:
        c.execute('insert into Person (name) values ("%s")' % n1)
        c.execute('select LAST_INSERT_ID()')
        p1 = c.fetchone()[0]
    else:
        p1 = ps[1]

    line = line[i+1:]
    i = line.index(',')
    n2 = line[:i]

    c.execute('select * from Person where name="%s"' % n2)
    ps = c.fetchone()
    if ps is None:
        c.execute('insert into Person (name) values ("%s")' % n2)
        c.execute('select LAST_INSERT_ID()')
        p2 = c.fetchone()[0]
    else:
        p2 = ps[1]

    line = line[i+1:]
    i = line.index(',')
    d = line[:i]

    if d == 'charged':
        p1, p2 = p2, p1

    line = line[i+1:]
    i = line.index(',')
    cap = line[i+2:-2]

    c.execute('insert into Payment (caption, sender, receiver) values (%s, %s, %s)', (cap, p1, p2))
    count += 1

f.close()

conn.commit()
close_conn(conn, c)