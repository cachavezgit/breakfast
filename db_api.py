from flask import Flask, request, jsonify
import oracledb

WALLET_DIRECTORY = "/opt/oracle"
DB_USER          = "admin"
DB_PASSWORD      = "Pa$$w0rd5678"
DB_DSN           = "glxs3dqea9h0rmo0_high"

app = Flask(__name__)

def get_conn():
    return oracledb.connect(
        user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN,
        config_dir=WALLET_DIRECTORY,
        wallet_location=WALLET_DIRECTORY,
        wallet_password=DB_PASSWORD
    )

def rows_as_dicts(cursor):
    cols = [d[0].lower() for d in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

@app.route('/evaluations')
def evaluations():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT o.id, o.name,
                   COUNT(r.id)            AS count_ratings,
                   ROUND(AVG(r.score), 1) AS average
            FROM meal_options o
            LEFT JOIN meal_ratings r ON r.option_id = o.id
            WHERE o.week_start = (SELECT MAX(week_start) FROM meal_options)
            GROUP BY o.id, o.name
            ORDER BY o.id
        """)
        return jsonify(rows_as_dicts(cur))

@app.route('/rate', methods=['POST'])
def rate():
    data = request.json
    id_, score = data.get('id'), data.get('score')
    if id_ is None or score is None or not (0 <= float(score) <= 10):
        return jsonify({'error': 'Invalid rating'}), 400
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO meal_ratings (option_id, score) VALUES (:id, :score)",
            {'id': id_, 'score': score}
        )
        conn.commit()
    return jsonify({'success': True})

@app.route('/options', methods=['POST'])
def add_options():
    data     = request.json
    options  = data.get('options', [])
    ws, we   = data.get('week_start'), data.get('week_end')
    if not options or not ws or not we:
        return jsonify({'error': 'options, week_start y week_end son requeridos'}), 400
    with get_conn() as conn, conn.cursor() as cur:
        for opt in options:
            cur.execute(
                """INSERT INTO meal_options (name, week_start, week_end)
                   VALUES (:name,
                           TO_DATE(:ws, 'YYYY-MM-DD'),
                           TO_DATE(:we, 'YYYY-MM-DD'))""",
                {'name': opt['name'], 'ws': ws, 'we': we}
            )
        conn.commit()
    return jsonify({'success': True, 'inserted': len(options)})

@app.route('/history')
def history():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT o.name,
                   TO_CHAR(o.week_start, 'YYYY-MM-DD') AS week_start,
                   TO_CHAR(o.week_end,   'YYYY-MM-DD') AS week_end,
                   COUNT(r.id)                          AS count_ratings,
                   ROUND(AVG(r.score), 1)               AS average
            FROM meal_options o
            LEFT JOIN meal_ratings r ON r.option_id = o.id
            GROUP BY o.name, o.week_start, o.week_end
            ORDER BY o.week_start DESC, o.name
        """)
        return jsonify(rows_as_dicts(cur))

if __name__ == '__main__':
    app.run(port=5001)
