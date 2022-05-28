import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.stats import norm
from utils import geo_json_mncp,load_pregunta
APIKEY = "cbff05426dd10f787f758fd2cc3af796"
data=pd.read_csv("Excel-Atlantico.csv")


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
        En las siguientes tablas se refleja los percentiles de cada materia evaluada en las pruebas saber en el segundo semestre del año 2020. Los cuales se usarán para responder a la siguente pregunta: 

        #### ¿Cuál colegio es mejor para mi hijo? si quiero que obtenga una beca por excelentes resultados en las pruebas saber.

        A continuación se presentan una tabla para cada materia la cual se pueden usar para responder a la pregunta anterior. Cada tabla contiene el nombre del colegio, el departamento al que pertenece y el percentil ordenado de forma descendente. Abajo de este encontrará unas medidas de estadistica descriptiva las cuales ayudan a conocer el comportamiento de los datos que se encuentran en las tablas. Estas son la Media aritmetica, la Varianza y la Desviación Estandar respectivamente.

    '''
    st.markdown(text)
    mejores_percentiles(data)


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

    
# Tabla de mejores percentiles por colegio y por municipio
def mejores_percentiles(data):
    data_atlantico = data[data["COLE_DEPTO_UBICACION"] == "ATLANTICO"]
    
    data_atlantico.rename(columns = {'COLE_MCPIO_UBICACION':'Municipio','COLE_NOMBRE_ESTABLECIMIENTO':'Nombre del Colegio','PERCENTIL_LECTURA_CRITICA':'Percentil Lectura Crítica','PERCENTIL_MATEMATICAS':'Percentil Matemáticas','PERCENTIL_C_NATURALES':'Percentil C. Naturales','PERCENTIL_SOCIALES_CIUDADANAS':'Percentil Comp. Ciudadanas','PERCENTIL_INGLES':'Percentil Inglés'}, inplace = True)
    materia = st.selectbox(label='Escoja una materia',options=['Percentil Lectura Crítica','Percentil Matemáticas','Percentil C. Naturales','Percentil Comp. Ciudadanas','Percentil Inglés'],help='Si no se selecciona uno, por defecto se escogeran todos',key=999)
    if materia:
        st.write("### Mejores percentiles de "+materia+" por colegio ")
        df = data_atlantico[['Nombre del Colegio','Municipio','Percentil Lectura Crítica','Percentil Matemáticas','Percentil C. Naturales','Percentil Comp. Ciudadanas','Percentil Inglés']]
        df=df.groupby(['Nombre del Colegio',"Municipio"],dropna=False).agg(Percentil=(materia,'mean')).reset_index()
        df=df.sort_values(by=['Percentil'],ascending=False).reset_index(drop=True)
        st.write(df,use_column_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Media",round(data_atlantico[materia].mean(),1))
        col2.metric("Varianza ",round(data_atlantico[materia].var(),1))
        col3.metric("Desviación Estandar",round(data_atlantico[materia].std(),1))

        text='''
        A continuación se elige un municipio, y respecto a ese municipio se elige un colegio, esto para obtener una gráfica de frecuencia y una Campana de Gauss el cual son gráficos que expresan de forma más visual el comportamiento de los datos. Esto para poder concluir si el colegio es malo, regular o bueno. 
        '''
        st.markdown(text)

        
        municipio = st.selectbox(label='Escoja un municipio',options=data_atlantico["Municipio"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos')
        colegio = st.selectbox(label='Escoja un colegio',options=data_atlantico[data_atlantico["Municipio"]==municipio]["Nombre del Colegio"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos')
        if municipio and colegio:
            colegio_percentiles = data_atlantico[data_atlantico["Nombre del Colegio"]==colegio][materia]
            colegio_percentiles =  colegio_percentiles.sort_values().reset_index(drop=True)
            x=colegio_percentiles.tolist()
            fig, ax = plt.subplots()
            ax.hist(x, bins=50)
            st.pyplot(fig)
            #-----------------------------------------------------------
            media=round(data_atlantico[materia].mean(),1)
            std=round(data_atlantico[materia].std(),1)
            x=colegio_percentiles.tolist()
            fig, ax = plt.subplots()
            ax.plot(x, norm.pdf(x, media, std))

            st.write(fig)
            

            
        text = '''---'''
        st.markdown(text)

        



app()
