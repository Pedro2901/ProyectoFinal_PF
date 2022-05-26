from multiprocessing import connection
from colorama import Cursor
import pyodbc as odbc
'''





try:
    connection:pyodbc.connect('DRIVER={SQL Server};SERVER=proyectofinal-server.database.windows.net;DATABASE=DatosColegios;UID=administradorpf;PWD=Proyectofinal!')
    print("Conexion exitosa")
    
    Cursor = connection.cursor()
    Cursor.execute("SELECT * FROM Saber_11_2020_2")
    row=Cursor.fetchone()
    rows = Cursor.fetchall()
    for row in rows:
        print(row)

    
    
except Exception as ex:
    print(ex)

'''
'''

DRIVER_NAME='{SQL Server}'
SERVER_NAME='proyectofinal-server.database.windows.net'
DATABASE_NAME='DatosColegios'

Connection_String= f"""
DRIVER={{{DRIVER_NAME}}};
SERVER={SERVER_NAME};
DATABASE={DATABASE_NAME};
trust_connection=yes;
"""
conn=odbc.connect(Connection_String)
print(conn)
'''

import pyodbc
server = 'proyectofinal-server.database.windows.net'
database = 'DatosColegios'
username = 'administradorpf'
password = '{Proyectofinal!}'   
driver= '{ODBC Driver 17 for SQL Server}'

def connect():
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Saber_11_2020_2")
            row = cursor.fetchone()
            while row:
                #print (str(row[0]) + " " + str(row[1]))
                #row = cursor.fetchone()
                return row