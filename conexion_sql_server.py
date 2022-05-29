import pyodbc
server = 'proyectofinal-server.database.windows.net'
database = 'DatosColegios'
username = 'administradorpf'
password = '{Proyectofinal!}'   
driver= '{ODBC Driver 17 for SQL Server}'

def info():
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Saber_11_2020_2")
            row = cursor.fetchone()
            while row:
                row = cursor.fetchone()
                return row