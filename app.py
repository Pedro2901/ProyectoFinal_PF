from nbformat import write
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np 
import requests 
#from conexion_sql_server import connect
from utils import geo_json_mncp,load_pregunta
APIKEY = "cbff05426dd10f787f758fd2cc3af796"

def app():
    # Visuals
    st.title("Colegios del Atlántico")
    url="https://www.datos.gov.co/resource/rnvb-vnyh.csv"
    data=pd.read_csv(url)

    pre(data)
    pregunta_1()
    pregunta_2()
    pregunta_3()
    estadisticas(data)
    mejores_percentiles(data)

def pre(data):
    if st.checkbox("Mostrar tabla de datos completa"):
        data_atlantico = data[data["cole_depto_ubicacion"] == "ATLANTICO"]
        st.write(data_atlantico)
    
    def grafica1():
        df = data[data["cole_depto_ubicacion"] == "ATLANTICO"]
        df = df[["cole_depto_ubicacion","cole_mcpio_ubicacion"]]
        df = df.groupby(["cole_mcpio_ubicacion"]).count().reset_index()
        df.columns = ["Municipio","Conteo"]
        return df

    def get_pos(dpto,munc):
        response =  requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={munc},{dpto},&limit={3}&appid={APIKEY}")
        r = response.json()
        lat = r[0]['lat']
        lon = r[0]['lon']
        new_df = pd.DataFrame.from_dict({'Latitud': [lat],'Longitud': [lon], 'Magnitud': [10]})
        return new_df
    
    def grafica3():
        return get_pos("ATLANTICO","BARRANQUILLA")

    st.write("### ¿Cuántos colegios hay en el departamento del Atlántico?")
    data = grafica1()
    fig = px.bar(data,x="Municipio",y="Conteo")
    st.write(fig)

#¿Que colegios sacaron la mayor cantidad de personas con puntaje superior a 300?
def pregunta_1():
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

def pregunta_2():
    data = load_pregunta(2)

    st.write("### Promedio de cada colegio de las pruebas icfes por municipio")

    c1,c2 = st.columns(2)

    outlines = geo_json_mncp()


    df = data[['Municipio','Puntaje','ID']].sort_values(by='Puntaje',ascending=False).reset_index(drop=True)
    c1.write(df[['Municipio','Puntaje']],use_column_width=True)
    
    fig = px.choropleth_mapbox(data, geojson=outlines, locations='ID',
                                color="Puntaje",
                                color_continuous_scale="Viridis",
                                featureidkey='properties.OBJECTID',
                                range_color=(data['Puntaje'].min(),data['Puntaje'].max()),
                                mapbox_style="carto-positron",
                                hover_name='Municipio',
                                zoom=8.5, center = {"lat": 10.6556, "lon": -75.0451},
                                opacity=0.5,
                                width=500
                                )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    c2.write(fig,use_column_width=True)

def pregunta_3():
    data = load_pregunta(3)

    st.write("### Mejor puntaje por municipio")

    c1,c2 = st.columns(2)

    outlines = geo_json_mncp()


    df = data[['Municipio','Puntaje','ID']].sort_values(by='Puntaje',ascending=False).reset_index(drop=True)
    c1.write(df[['Municipio','Puntaje']],use_column_width=True)

    fig = px.choropleth_mapbox(data, geojson=outlines, locations='ID',
                                color="Puntaje",
                                color_continuous_scale="Viridis",
                                featureidkey='properties.OBJECTID',
                                range_color=(data['Puntaje'].min(),data['Puntaje'].max()),
                                mapbox_style="carto-positron",
                                hover_name='Municipio',
                                zoom=8.5, center = {"lat": 10.6556, "lon": -75.0451},
                                opacity=0.5,
                                width=500
                                )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    c2.write(fig,use_column_width=True)

# Media, desviación estandar y varianza de los resultados del dpto del atlantico
def estadisticas(data):
    data_atlantico = data[data["cole_depto_ubicacion"] == "ATLANTICO"]
    # Por defecto si no hay dpto, son todos (ya no xd)
    municipios = st.multiselect(label='Escoja un municipio',options=data_atlantico["cole_mcpio_ubicacion"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos',default=data_atlantico["cole_mcpio_ubicacion"].unique())
    if len(municipios) > 0:
        data_atlantico = data_atlantico[data_atlantico["cole_mcpio_ubicacion"].isin(municipios)]
    
        resultados = data_atlantico['punt_global']
        st.write("Resultados del Atlantico")
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Media", round(resultados.mean(),1))
        col2.metric("Desviación", round(resultados.std(),1))
        col3.metric("Varianza", round(resultados.var(),1))

        data_atlantico.rename(columns = {'cole_nombre_sede':'Nombre del Colegio', 'punt_global':'Puntaje'}, inplace = True)
        st.write(data_atlantico.groupby(['Nombre del Colegio'],dropna=False).agg({'Puntaje':['mean',lambda x: pd.DataFrame.std(x,ddof=0),'var']}).reset_index())

# Tabla de mejores percentiles por colegio y por municipio
def mejores_percentiles(data):
        data_atlantico = data[data["cole_depto_ubicacion"] == "ATLANTICO"]
        data_atlantico.rename(columns = {'cole_nombre_establecimiento':'Nombre del Colegio'}, inplace = True)
        #mun=data_atlantico['cole_mcpio_ubicacion']
        df = data_atlantico[['Nombre del Colegio','cole_mcpio_ubicacion','percentil_lectura_critica','percentil_matematicas','percentil_c_naturales','percentil_sociales_ciudadanas','percentil_ingles']]

        df=df.groupby(['Nombre del Colegio'],dropna=False).agg(Percentil_Mat=('percentil_matematicas','mean'),Percentil_Lect_Crit=('percentil_lectura_critica','mean')).reset_index()

        df=df.sort_values(by=['Percentil_Mat','Percentil_Lect_Crit'],ascending=False).reset_index(drop=True)

        st.write("### Mejores percentiles por colegio")
        st.write(df,use_column_width=True)


app()
