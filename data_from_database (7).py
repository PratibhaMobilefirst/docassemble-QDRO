from docassemble.base.util import variables_snapshot_connection,get_config, user_info, json
import psycopg2

__all__ = ['display_code','display_plan']

def get_conn():
    dbconfig = get_config('db')
    return psycopg2.connect(database=dbconfig.get('railway'),
                            user=dbconfig.get('postgres'),
                            password=dbconfig.get('zGXpi8KWdoNs6rthE7Eg'),
                            host=dbconfig.get('containers-us-west-179.railway.app'),
                            port=dbconfig.get('6763'))


def display_code():
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("select sf_sponsor_name from sponsor ORDER BY id ASC LIMIT 100")
    results = [record[0] for record in cur.fetchall()]
    conn.close()
    return results

def display_plan(code):
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("SELECT sf_plan_name from plan n JOIN sponsor s ON n.sponsor_id = s.id where s.sf_sponsor_name = '" + code + "'")
    results = [record[0] for record in cur.fetchall()]
    conn.close()
    return results