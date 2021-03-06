from re import I
import pyodbc
import pandas as pd
server = 'proyectofinal-server.database.windows.net'
database = 'DatosColegios'
username = 'administradorpf'
password = '{Proyectofinal!}'
driver = '{ODBC Driver 17 for SQL Server}'


def info():
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD=' + password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM Saber_11_2020_2 WHERE COLE_DEPTO_UBICACION = 'ATLANTICO'")
            row = cursor.fetchone()
            df = pd.DataFrame(columns=['ESTU_TIPODOCUMENTO', 'ESTU_NACIONALIDAD', 'ESTU_GENERO',
                                       'ESTU_FECHANACIMIENTO', 'PERIODO', 'ESTU_CONSECUTIVO',
                                       'ESTU_ESTUDIANTE', 'ESTU_PAIS_RESIDE', 'ESTU_TIENEETNIA',
                                       'ESTU_DEPTO_RESIDE', 'ESTU_COD_RESIDE_DEPTO', 'ESTU_MCPIO_RESIDE',
                                       'ESTU_COD_RESIDE_MCPIO', 'FAMI_ESTRATOVIVIENDA', 'FAMI_PERSONASHOGAR',
                                       'FAMI_CUARTOSHOGAR', 'FAMI_EDUCACIONPADRE', 'FAMI_EDUCACIONMADRE',
                                       'FAMI_TRABAJOLABORPADRE', 'FAMI_TRABAJOLABORMADRE',
                                       'FAMI_TIENEINTERNET', 'FAMI_TIENESERVICIOTV', 'FAMI_TIENECOMPUTADOR',
                                       'FAMI_TIENELAVADORA', 'FAMI_TIENEHORNOMICROOGAS', 'FAMI_TIENEAUTOMOVIL',
                                       'FAMI_TIENEMOTOCICLETA', 'FAMI_TIENECONSOLAVIDEOJUEGOS',
                                       'FAMI_NUMLIBROS', 'FAMI_COMELECHEDERIVADOS',
                                       'FAMI_COMECARNEPESCADOHUEVO', 'FAMI_COMECEREALFRUTOSLEGUMBRE',
                                       'FAMI_SITUACIONECONOMICA', 'ESTU_DEDICACIONLECTURADIARIA',
                                       'ESTU_DEDICACIONINTERNET', 'ESTU_HORASSEMANATRABAJA',
                                       'ESTU_TIPOREMUNERACION', 'COLE_CODIGO_ICFES',
                                       'COLE_COD_DANE_ESTABLECIMIENTO', 'COLE_NOMBRE_ESTABLECIMIENTO',
                                       'COLE_GENERO', 'COLE_NATURALEZA', 'COLE_CALENDARIO', 'COLE_BILINGUE',
                                       'COLE_CARACTER', 'COLE_COD_DANE_SEDE', 'COLE_NOMBRE_SEDE',
                                       'COLE_SEDE_PRINCIPAL', 'COLE_AREA_UBICACION', 'COLE_JORNADA',
                                       'COLE_COD_MCPIO_UBICACION', 'COLE_MCPIO_UBICACION',
                                       'COLE_COD_DEPTO_UBICACION', 'COLE_DEPTO_UBICACION',
                                       'ESTU_PRIVADO_LIBERTAD', 'ESTU_COD_MCPIO_PRESENTACION',
                                       'ESTU_MCPIO_PRESENTACION', 'ESTU_DEPTO_PRESENTACION',
                                       'ESTU_COD_DEPTO_PRESENTACION', 'PUNT_LECTURA_CRITICA',
                                       'PERCENTIL_LECTURA_CRITICA', 'DESEMP_LECTURA_CRITICA',
                                       'PUNT_MATEMATICAS', 'PERCENTIL_MATEMATICAS', 'DESEMP_MATEMATICAS',
                                       'PUNT_C_NATURALES', 'PERCENTIL_C_NATURALES', 'DESEMP_C_NATURALES',
                                       'PUNT_SOCIALES_CIUDADANAS', 'PERCENTIL_SOCIALES_CIUDADANAS',
                                       'DESEMP_SOCIALES_CIUDADANAS', 'PUNT_INGLES', 'PERCENTIL_INGLES',
                                       'DESEMP_INGLES', 'PUNT_GLOBAL', 'PERCENTIL_GLOBAL',
                                       'ESTU_INSE_INDIVIDUAL', 'ESTU_NSE_INDIVIDUAL',
                                       'ESTU_NSE_ESTABLECIMIENTO', 'ESTU_ESTADOINVESTIGACION',
                                       'ESTU_GENERACION-E'],
                              index=range(28608))
            i = 0
            while row:
                df.iloc[i] = (row)
                i = i+1
                row = cursor.fetchone()
            return df
