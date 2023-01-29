from flask import Flask, request
from getpass import getpass
from mysql.connector import connect, Error
 
connection = None
 
def init_db():
    global connection
    try:
        print('Connection to db:', end='')
        connection = connect(host='db', user='root', password='123')
        print('ОК')
 
        print('Create db:', end='')
        create_db_query = "CREATE DATABASE IF NOT EXISTS vars"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
        print('ОК')
 
        print('Change db:', end='')
        use_db_query = "USE vars"
        with connection.cursor() as cursor:
            cursor.execute(use_db_query)
        print('ОК')
 
        print('Create table:', end='')
        create_table_query = """
        CREATE TABLE IF NOT EXISTS vars(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            value VARCHAR(100),
            UNIQUE (name)
            )
            """
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()  
        print('ОК')     
    except Error as e:
        print('Failure', e)
 
 
app = Flask(__name__)
 
@app.route('/var/<var_name>', methods=['GET'])
def get(var_name):
    select_query = f"""
    SELECT value FROM vars
    WHERE name = '{var_name}'
    """
 
    print("Select query:", select_query)
    with connection.cursor() as cursor:
        cursor.execute(select_query)
        return cursor.fetchall()[0][0]
 
 
@app.route('/var/<var_name>', methods=['POST'])
def set(var_name):
    value = request.form.get("value")
    insert_query = f"""
    INSERT INTO vars (name, value)
    VALUES ('{var_name}', '{value}')
    ON DUPLICATE KEY UPDATE value='{value}'
    """
 
    print("Insert query:", insert_query)
    with connection.cursor() as cursor:
        cursor.execute(insert_query)
        connection.commit()
 
    return 'OK'
 
 
if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0')
