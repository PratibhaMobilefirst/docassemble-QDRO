from docassemble.base.util import variables_snapshot_connection,get_config, user_info, json
import psycopg2
from cryptography.fernet import Fernet

__all__ = ['add','display','encryptStr','decryptStr','dash','display_copy','delete_data','display_register_data']

def get_conn():
    dbconfig = get_config('db')
    return psycopg2.connect(database=dbconfig.get('railway'),
                            user=dbconfig.get('postgres'),
                            password=dbconfig.get('zGXpi8KWdoNs6rthE7Eg'),
                            host=dbconfig.get('containers-us-west-179.railway.app'),
                            port=dbconfig.get('6763'))

def encryptStr(textToConvert):
  key = 'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
  fernet = Fernet(key)
  message = bytes(str(textToConvert), 'utf-8')
  encrypted_message = fernet.encrypt(message)
  return encrypted_message.decode()

def decryptStr(textToDecrypt):
  key = 'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='

  # Create a Fernet object using the key
  fernet = Fernet(key)
  decrypted_message = fernet.decrypt(textToDecrypt)
  return decrypted_message.decode()

def add(da,mainid):
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    da1 = json.dumps(da)
    exists_data = display_copy(mainid)
    if len(exists_data) > 0:
      sql_update_query = """Update interview set data = %s where user_id = %s and id = %s"""
      cur.execute(sql_update_query, (da1, user_info().id,mainid))
      conn.commit()
      cur.close()
      return ""
    else:
      postgres_insert_query = """ INSERT INTO interview (data, user_id, filename) VALUES (%s,%s,%s)"""
      record_to_insert = (da1, user_info().id, 'docassemble.playground3QDRO:Copy_1.yml')
      cur.execute(postgres_insert_query, record_to_insert)
      
      last_id = cur.lastrowid
      postgres_insert_query_payment = """ INSERT INTO payment (interview_id, user_id, is_paid) VALUES (%s,%s,%s)"""
      record_to_insert_payment = (last_id, user_info().id, 'false')
      cur.execute(postgres_insert_query_payment, record_to_insert_payment)
      conn.commit()
      cur.close()
      return ""

def display():
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("select data from interview where user_id="+ str(user_info().id) +" and filename='" + user_info().filename + "'")
    results = [record[0] for record in cur.fetchall()]
    conn.close()
    return results
  
def dash():
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("select * from interview where user_id="+ str(user_info().id))
    rows = cur.fetchall()
    results = []
    for row in rows:
      results.append({
        "id": row[0],
        "user_id": row[1],
        "data": row[2],
        "filename": row[3],
        "creation_date": row[4],
        "modified_date": row[5]
      })
    conn.close()
    return results
  
def display_copy(mainid):
    if mainid == 'unknown':
      results = []
      return results
    else:
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("select data from interview where id=" + mainid + " and user_id="+ str(user_info().id)   +" and filename='" + user_info().filename + "'")
      results = [record[0] for record in cur.fetchall()]
      conn.close()
      return results
  
def display_register_data(mainid):
    if mainid == 'unknown':
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("select * from \"user\" where id = " + str(user_info().id))
      rows = cur.fetchall()
      results = []
      for row in rows:
        results.append({
          "email": row[3],
          "first_name": row[6],
          "last_name": row[7],
        })
      conn.close()
      return results
    else:
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("select data from interview where id=" + mainid + " and user_id="+ str(user_info().id)   +" and filename='" + user_info().filename + "'")
      results = [record[0] for record in cur.fetchall()]
      conn.close()
      return results
    
def delete_data(mainid):
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("delete from interview where id=" + mainid)
      msg = 'Record is deleted successfully'
      conn.commit()
      cur.close()
      conn.close()
      return msg

def display_payment(mainid):
    if mainid == 'unknown':
      results = []
      return results
    else:
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("select data from payment where interview_id=" + mainid + " and user_id="+ str(user_info().id))
      results = [record[0] for record in cur.fetchall()]
      conn.close()
      return results