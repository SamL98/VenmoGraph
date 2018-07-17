from flask import Flask, jsonify, request
from db import *

app = Flask(__name__, static_url_path='/static')
conn, cur = create_conn()

@app.route('/', methods=['GET'])
def graph():
    return app.send_static_file('graph.html')

@app.route('/users', methods=['GET'])
def get_users():
    query = 'select id, name from Person order by lower(name)'

    limit = request.args.get('limit')
    if not limit is None:
        offset = request.args.get('offset')
        if offset is None:
            offset = 0
        query += ' limit %d, %d' % (int(offset), int(limit))

    cur.execute(query)
    return jsonify(result=cur.fetchall())

@app.route('/search', methods=['GET'])
def search():
    qtext = request.args.get('q')
    if qtext is None:
        return None, 400

    cur.execute('select id, name from Person where lower(name) like \'%{}%\''.format(qtext.lower()))
    targets = cur.fetchall()
    max_name = max([t['name'].lower() for t in targets])

    if len(targets) == 0:
        return jsonify(result={})

    prev_name = request.args.get('pname')
    if prev_name is None:
        return jsonify(result=target_ids)

    cur.execute('select id, name from Person where name>\'%s\' and name<=\'%s\' order by lower(name)' % (prev_name.lower(), max_name))
    return jsonify(result=cur.fetchall())

@app.route('/pmts/<vid>', methods=['GET'])
def get_pmts(vid):
    if ':' in vid:
        vids = [int(v) for v in vid.split(':')]
    else:
        vids = [int(vid)]

    query ='select \
        P1.name as sender, P2.name as receiver, Payment.caption from Payment \
        inner join Person P1 on P1.id=Payment.sender \
        inner join Person P2 on P2.id=Payment.receiver where'

    for i, v in enumerate(vids):
        query += ' sender={0} or receiver={0}'.format(v)
        if i < len(vids)-1:
            query += ' or'
    
    cur.execute(query)
    return jsonify(result=cur.fetchall())

if __name__ == '__main__':
    app.run(port=8080)
    close_conn(conn, cur)