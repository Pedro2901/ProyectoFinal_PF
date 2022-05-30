import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.stats import norm
from conexion_sql_server import info 
from utils import geo_json_mncp,load_pregunta
import plotly.figure_factory as ff
APIKEY = "cbff05426dd10f787f758fd2cc3af796"
data=info()

def app():
    st.title("Sistema de recolección, visualización y análisis de datos de colegios del departamento del Atlántico")

    text =  '''
    Este es un prototipo funcional de una página web con el objetivo de mostrar información relevante sobre los colegios del departamento del Atlántico, para así, poder informar a los padres de familia y apoyarlos en una posible elección de colegio para su hijo.

    Este proyecto fue creado y desarrollado por estudiantes de Ingeniería de Sistemas y Computación de la Universidad del Norte como proyecto de grado.

    #### Indice:    
    - ¿Cuántos colegios hay en el departamento del Atlántico?
    - Mejor puntaje de pruebas saber de cada colegio por municipio.
    - ¿Que colegios sacaron la mayor cantidad de personas con puntaje superior a 300?
    - Análisis de los percentiles de cada materia evaluada en las pruebas saber.

    La información que se utilizó en este proyecto es proporcionada de la base de datos de Datos Abiertos del Gobierno de Colombia. Para ver la información completa oprima en la celda.
    '''

    st.markdown(text)

    if st.checkbox("Mostrar tabla de datos completa"):
        data_atlantico = data[data["COLE_DEPTO_UBICACION"] == "ATLANTICO"]
        st.write(data_atlantico)

    text = '''

        A continuación se presentará información general de los colegios del departamento en forma de tablas y graficos las cuales responden a preguntas cotidianas sobre los colegios en temas generales y de pruebas saber.

    '''
    st.markdown(text)

    st.write("")
    pre(data)

    MejoresPruebasPorMunicipio()
    mapa()

    st.write("## Análisis de los percentiles de cada materia evaluada en las pruebas saber.")
    text='''
        En las siguientes tablas se refleja los percentiles de cada materia evaluada en las pruebas saber en el segundo semestre del año 2020.

        A continuación se presenta una lista desplegable en la cual se podrá escoger un percentil de una de las materias evaluadas en las pruebas saber, esto para poder analizar su comportamiento y así poder llegar a ciertas conclusiones sobre la pregunta anterior. Cada materia muestra una tabla que contiene el nombre del colegio, el departamento al que pertenece y el promedio por colegio del percentil escogido. Abajo de este encontrará unas medidas de estadistica descriptiva. Estas son la [Media aritmética](https://es.wikipedia.org/wiki/Media_aritm%C3%A9tica), la [Varianza](https://es.wikipedia.org/wiki/Varianza) y la [Desviación Estandar](https://es.wikipedia.org/wiki/Desviaci%C3%B3n_t%C3%ADpicaDesviación) respectivamente.

    '''
    st.markdown(text)
    mejores_percentiles(data)
    text='''
    ###### Si tienes alguna duda, inquietud, crítica o problema con los datos presentados, por favor notificarlo al siguiente correo:
    ###### [colegiosatlanticoun@gmail.com](mailto:colegiosatlanticoun@gmail.com)
    '''
    st.markdown(text)


def pre(data):
    
    def grafica1():
        df = data[data["COLE_DEPTO_UBICACION"] == "ATLANTICO"]
        
        df = df[["COLE_NOMBRE_ESTABLECIMIENTO","COLE_MCPIO_UBICACION"]]
        df=df.drop_duplicates(subset = "COLE_NOMBRE_ESTABLECIMIENTO")
        df = df.groupby(["COLE_MCPIO_UBICACION"]).count().reset_index()
        df.columns = ["Municipio","Conteo"]
        return df

    st.write("### ¿Cuántos colegios hay en el departamento del Atlántico?")
    data = grafica1()
    fig = px.bar(data,x="Municipio",y="Conteo")
    st.write(fig)
    

def MejoresPruebasPorMunicipio():
    data_atlantico = data[data["COLE_DEPTO_UBICACION"] == "ATLANTICO"]
    data_atlantico.rename(columns = {'COLE_MCPIO_UBICACION':'Municipio','COLE_NOMBRE_ESTABLECIMIENTO':'Nombre del Colegio', 'PUNT_GLOBAL':'Puntaje'}, inplace = True)
    st.write("### Mejor puntaje de pruebas saber de cada colegio por municipio")
    df = data_atlantico[['Municipio','Puntaje','Nombre del Colegio']].sort_values(by='Puntaje',ascending=False).reset_index(drop=True)
    st.write(df[['Municipio','Nombre del Colegio','Puntaje']],use_column_width=True)
    text = '''---'''
    st.markdown(text)

def mapa():
    data = load_pregunta(1)

    st.write("### ¿Que colegios sacaron la mayor cantidad de personas con puntaje superior a 300?")

    c1,c2 = st.columns(2)

    outlines = geo_json_mncp()


    df = data[['Municipio','Promedio']].sort_values(by='Promedio',ascending=False).reset_index(drop=True)
    c1.write(df,use_column_width=True)
    
    fig = px.choropleth_mapbox(data, geojson=outlines, locations='ID',
                           color="Promedio",
                           color_continuous_scale="Viridis",
                           featureidkey='properties.OBJECTID',
                           range_color=(data['Promedio'].min(), data['Promedio'].max()),
                           mapbox_style="carto-positron",
                           hover_name='Municipio',
                           zoom=8.5, center = {"lat": 10.6556, "lon": -75.0451},
                           opacity=0.5,
                           width=500
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    c2.write(fig,use_column_width=True)
    text = '''---'''
    st.markdown(text)


def mejores_percentiles(data):
    data_atlantico = data[data["COLE_DEPTO_UBICACION"] == "ATLANTICO"]
    
    data_atlantico.rename(columns = {'COLE_MCPIO_UBICACION':'Municipio','COLE_NOMBRE_ESTABLECIMIENTO':'Nombre del Colegio','PERCENTIL_LECTURA_CRITICA':'Percentil Lectura Crítica','PERCENTIL_MATEMATICAS':'Percentil Matemáticas','PERCENTIL_C_NATURALES':'Percentil C. Naturales','PERCENTIL_SOCIALES_CIUDADANAS':'Percentil Comp. Ciudadanas','PERCENTIL_INGLES':'Percentil Inglés'}, inplace = True)
    materia = st.selectbox(label='Escoja una materia',options=['Percentil Lectura Crítica','Percentil Matemáticas','Percentil C. Naturales','Percentil Comp. Ciudadanas','Percentil Inglés'],help='Por defecto se escogerá el primero de la lista.',key=999)
    if materia:
        st.write("### Mejores percentiles de "+materia+" por colegio ")
        data_atlantico[materia]=data_atlantico[materia].astype(float)
        df = data_atlantico[['Nombre del Colegio','Municipio','Percentil Lectura Crítica','Percentil Matemáticas','Percentil C. Naturales','Percentil Comp. Ciudadanas','Percentil Inglés']]
        df[materia]=df[materia].astype('int64')
        df=df.groupby(['Nombre del Colegio',"Municipio"],dropna=False).agg(Percentil=(materia,'mean')).reset_index()
        df=df.sort_values(by=['Percentil'],ascending=False).reset_index(drop=True)
        st.write(df,use_column_width=True)

        col1, col2, col3 = st.columns(3)
        media_general = round(data_atlantico[materia].mean(),1)
        col1.metric("Media",media_general)
        col2.metric("Varianza ",round(data_atlantico[materia].var(),1))
        col3.metric("Desviación Estandar",round(data_atlantico[materia].std(),1))

        text='''
        La Media aritmetica, la Varianza y la Desviación Estandar son medidas de dispersión estadistica las cuales muestran de forma general como se comportan los datos. La media es un promedio de todos los percentiles de la materia; la varianza es la diferencia entre los datos y la media aritmetica y la desviación estandar es que tan cerca están los datos de su media, si este valor es pequeño significa que los datos están muy cerca y en el caso contrario que estan muy lejanos.


        A continuación se elige un municipio, y respecto a ese municipio se elige un colegio, esto para obtener unas gráficas las cuales son gráficas que expresan de forma más visual el comportamiento de los datos.
        '''
        st.markdown(text)

        
        municipio = st.selectbox(label='Escoja un municipio',options=data_atlantico["Municipio"].unique(),help='Por defecto se escogerá el primero de la lista.')
        colegio = st.selectbox(label='Escoja un colegio',options=data_atlantico[data_atlantico["Municipio"]==municipio]["Nombre del Colegio"].unique(),help='Por defecto se escogerá el primero de la lista.')
        if municipio and colegio:
            st.write("#### Diagrama de Densidad")
            colegio_percentiles = data_atlantico[data_atlantico["Nombre del Colegio"]==colegio][materia]
            colegio_percentiles =  colegio_percentiles.sort_values().reset_index(drop=True)
            x=colegio_percentiles.tolist()
            group_labels = ['Percentiles'] # name of the dataset
            hist_data = [x]
            fig = ff.create_distplot(hist_data,group_labels)
            st.plotly_chart(fig)
            text='''
            Esta es una gráfica de densidad, la cual se puede ver la distribución que tienen los datos, en el cual los picos del gráfico nos ayudan a mostrar dónde los valores se concentran en el intervalo. Estos gráficos son mejores en la demostración del comportamiento de unos datos especificos.
            '''
            st.markdown(text)
            #-----------------------------------------------------------          
            st.write("#### Diagrama de Caja y Bigotes")  
            fig = px.box(colegio_percentiles, y=materia)    
            st.plotly_chart(fig)
            text='''
            Esta es una gráfica de caja y bigote, el cual nos ayuda a ver tanto dispersion de los datos como su simetría. Dentro de la caja están los datos más agrupados. las líneas que se extienden paralelas a las cajas se conocen como "bigotes", y se usan para indicar variabilidad fuera de los cuartiles superior e inferior. Los valores atípicos se representan a veces como puntos individuales que están en línea con los bigotes. Esta es una muy buena gráfica para mirar el comportamiento de estos datos.
            '''
            st.markdown(text)
        text = '''---'''
        st.markdown(text)

app()
