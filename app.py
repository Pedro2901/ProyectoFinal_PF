from asyncio.windows_events import NULL
from nbformat import write
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats 
import seaborn as sns 
import requests 
from scipy.stats import norm
#from conexion_sql_server import connect
from utils import geo_json_mncp,load_pregunta
APIKEY = "cbff05426dd10f787f758fd2cc3af796"

url="https://www.datos.gov.co/resource/rnvb-vnyh.csv"
data=pd.read_csv("Excel-Atlantico.csv")


def app():
    # Visuals
    st.title("Colegios del Atlántico")
    

    pre(data)
    MejoresPruebasPorMunicii()
    mapa()
    mejores_percentiles(data)

def pre(data):
    if st.checkbox("Mostrar tabla de datos completa"):
        data_atlantico = data[data["COLE_DEPTO_UBICACION"] == "ATLANTICO"]
        st.write(data_atlantico)
    
    def grafica1():
        df = data[data["COLE_DEPTO_UBICACION"] == "ATLANTICO"]
        
        df = df[["COLE_NOMBRE_ESTABLECIMIENTO","COLE_MCPIO_UBICACION"]]
        df=df.drop_duplicates(subset = "COLE_NOMBRE_ESTABLECIMIENTO")
        df = df.groupby(["COLE_MCPIO_UBICACION"]).count().reset_index()
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
    text = '''---'''
    st.markdown(text)

def MejoresPruebasPorMunicii():
    data_atlantico = data[data["COLE_DEPTO_UBICACION"] == "ATLANTICO"]
    st.write("### Mejor puntaje de pruebas saber de cada colegio por municipio")
    df = data_atlantico[['COLE_MCPIO_UBICACION','PUNT_GLOBAL','COLE_NOMBRE_ESTABLECIMIENTO']].sort_values(by='PUNT_GLOBAL',ascending=False).reset_index(drop=True)
    st.write(df[['COLE_MCPIO_UBICACION','COLE_NOMBRE_ESTABLECIMIENTO','PUNT_GLOBAL']],use_column_width=True)
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

        st.write("### Mejores percentiles de matemáticas por colegio ")
        data_atlantico.rename(columns = {'COLE_NOMBRE_ESTABLECIMIENTO':'Nombre del Colegio'}, inplace = True)
        df = data_atlantico[['Nombre del Colegio','COLE_MCPIO_UBICACION','PERCENTIL_LECTURA_CRITICA','PERCENTIL_MATEMATICAS','PERCENTIL_C_NATURALES','PERCENTIL_SOCIALES_CIUDADANAS','PERCENTIL_INGLES']]
        df=df.groupby(['Nombre del Colegio',"COLE_MCPIO_UBICACION"],dropna=False).agg(Percentil_Mat=('PERCENTIL_MATEMATICAS','mean')).reset_index()
        df=df.sort_values(by=['Percentil_Mat'],ascending=False).reset_index(drop=True)
        st.write(df,use_column_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Media",round(data_atlantico["PERCENTIL_MATEMATICAS"].mean(),1))
        col2.metric("Varianza ",round(data_atlantico["PERCENTIL_MATEMATICAS"].var(),1))
        col3.metric("Desviación Estandar",round(data_atlantico["PERCENTIL_MATEMATICAS"].std(),1))

        municipio = st.multiselect(label='Escoja un municipio',options=data_atlantico["COLE_MCPIO_UBICACION"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos')
        colegio = st.multiselect(label='Escoja un colegio',options=data_atlantico[data_atlantico["COLE_MCPIO_UBICACION"].isin(municipio)]["Nombre del Colegio"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos')
        if len(municipio) > 0 and len(colegio) > 0:
            colegio_percentiles = data_atlantico[data_atlantico["Nombre del Colegio"].isin(colegio)]["PERCENTIL_MATEMATICAS"]
            colegio_percentiles =  colegio_percentiles.sort_values().reset_index(drop=True)
            x=colegio_percentiles.tolist()
            # histograma de distribución normal.
            fig, ax = plt.subplots()
            ax.hist(x, bins=50)
            st.pyplot(fig)
            #-----------------------------------------------------------
            media=round(data_atlantico["PERCENTIL_MATEMATICAS"].mean(),1)
            std=round(data_atlantico["PERCENTIL_MATEMATICAS"].std(),1)
            x=colegio_percentiles.tolist()
            print(x)
            fig, ax = plt.subplots()
            ax.plot(x, norm.pdf(x, media, std))

            st.write(fig)
            

            
        text = '''---'''
        st.markdown(text)

        st.write("### Mejores percentiles de lectura crítica por colegio ")
        df = data_atlantico[['Nombre del Colegio','COLE_MCPIO_UBICACION','PERCENTIL_LECTURA_CRITICA','PERCENTIL_MATEMATICAS','PERCENTIL_C_NATURALES','PERCENTIL_SOCIALES_CIUDADANAS','PERCENTIL_INGLES']]
        df=df.groupby(['Nombre del Colegio',"COLE_MCPIO_UBICACION"],dropna=False).agg(Percentil_Lect_Crit=('PERCENTIL_LECTURA_CRITICA','mean')).reset_index()
        df=df.sort_values(by=['Percentil_Lect_Crit'],ascending=False).reset_index(drop=True)
        st.write(df,use_column_width=True)

        col_1, col_2, col_3 = st.columns(3)
        col_1.metric("Media",round(data_atlantico["PERCENTIL_LECTURA_CRITICA"].mean(),1))
        col_2.metric("Varianza ",round(data_atlantico["PERCENTIL_LECTURA_CRITICA"].var(),1))
        col_3.metric("Desviación Estandar",round(data_atlantico["PERCENTIL_LECTURA_CRITICA"].std(),1))

        municipio = st.multiselect(label='Escoja un municipio',options=data_atlantico["COLE_MCPIO_UBICACION"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos',key=1000)
        colegio = st.multiselect(label='Escoja un colegio',options=data_atlantico[data_atlantico["COLE_MCPIO_UBICACION"].isin(municipio)]["Nombre del Colegio"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos',key=1001)
        if len(municipio) > 0 and len(colegio) > 0:
            colegio_percentiles = data_atlantico[data_atlantico["Nombre del Colegio"].isin(colegio)]["PERCENTIL_LECTURA_CRITICA"]
            colegio_percentiles =  colegio_percentiles.sort_values().reset_index(drop=True)
            x=colegio_percentiles.tolist()
            # histograma de distribución normal.
            fig, ax = plt.subplots()
            ax.hist(x, bins=50)
            st.pyplot(fig)
            #-----------------------------------------------------------
            media=round(data_atlantico["PERCENTIL_LECTURA_CRITICA"].mean(),1)
            std=round(data_atlantico["PERCENTIL_LECTURA_CRITICA"].std(),1)
            x=colegio_percentiles.tolist()
            print(x)
            fig, ax = plt.subplots()
            ax.plot(x, norm.pdf(x, media, std))

            st.write(fig)

        text = '''---'''
        st.markdown(text)

        st.write("### Mejores percentiles de ciencias naturales por colegio ")
        df = data_atlantico[['Nombre del Colegio','COLE_MCPIO_UBICACION','PERCENTIL_LECTURA_CRITICA','PERCENTIL_MATEMATICAS','PERCENTIL_C_NATURALES','PERCENTIL_SOCIALES_CIUDADANAS','PERCENTIL_INGLES']]
        df=df.groupby(['Nombre del Colegio',"COLE_MCPIO_UBICACION"],dropna=False).agg(PERCENTIL_C_NATURALES=('PERCENTIL_C_NATURALES','mean')).reset_index()
        df=df.sort_values(by=['PERCENTIL_C_NATURALES'],ascending=False).reset_index(drop=True)
        st.write(df,use_column_width=True)

        col_1, col_2, col_3 = st.columns(3)
        col_1.metric("Media",round(data_atlantico["PERCENTIL_C_NATURALES"].mean(),1))
        col_2.metric("Varianza ",round(data_atlantico["PERCENTIL_C_NATURALES"].var(),1))
        col_3.metric("Desviación Estandar",round(data_atlantico["PERCENTIL_C_NATURALES"].std(),1))

        municipio = st.multiselect(label='Escoja un municipio',options=data_atlantico["COLE_MCPIO_UBICACION"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos',key=1002)
        colegio = st.multiselect(label='Escoja un colegio',options=data_atlantico[data_atlantico["COLE_MCPIO_UBICACION"].isin(municipio)]["Nombre del Colegio"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos',key=1003)
        if len(municipio) > 0 and len(colegio) > 0:
            colegio_percentiles = data_atlantico[data_atlantico["Nombre del Colegio"].isin(colegio)]["PERCENTIL_C_NATURALES"]
            colegio_percentiles =  colegio_percentiles.sort_values().reset_index(drop=True)
            x=colegio_percentiles.tolist()
            # histograma de distribución normal.
            fig, ax = plt.subplots()
            ax.hist(x, bins=50)
            st.pyplot(fig)
            #-----------------------------------------------------------
            media=round(data_atlantico["PERCENTIL_C_NATURALES"].mean(),1)
            std=round(data_atlantico["PERCENTIL_C_NATURALES"].std(),1)
            x=colegio_percentiles.tolist()
            print(x)
            fig, ax = plt.subplots()
            ax.plot(x, norm.pdf(x, media, std))

            st.write(fig)

        text = '''---'''
        st.markdown(text)

        st.write("### Mejores percentiles de sociales por colegio ")
        df = data_atlantico[['Nombre del Colegio','COLE_MCPIO_UBICACION','PERCENTIL_LECTURA_CRITICA','PERCENTIL_MATEMATICAS','PERCENTIL_C_NATURALES','PERCENTIL_SOCIALES_CIUDADANAS','PERCENTIL_INGLES']]
        df=df.groupby(['Nombre del Colegio',"COLE_MCPIO_UBICACION"],dropna=False).agg(Percentil_sociales_ciudadana=('PERCENTIL_SOCIALES_CIUDADANAS','mean')).reset_index()
        df=df.sort_values(by=['Percentil_sociales_ciudadana'],ascending=False).reset_index(drop=True)
        st.write(df,use_column_width=True)

        col_1, col_2, col_3 = st.columns(3)
        col_1.metric("Media",round(data_atlantico["PERCENTIL_SOCIALES_CIUDADANAS"].mean(),1))
        col_2.metric("Varianza ",round(data_atlantico["PERCENTIL_SOCIALES_CIUDADANAS"].var(),1))
        col_3.metric("Desviación Estandar",round(data_atlantico["PERCENTIL_SOCIALES_CIUDADANAS"].std(),1))

        municipio = st.multiselect(label='Escoja un municipio',options=data_atlantico["COLE_MCPIO_UBICACION"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos',key=1004)
        colegio = st.multiselect(label='Escoja un colegio',options=data_atlantico[data_atlantico["COLE_MCPIO_UBICACION"].isin(municipio)]["Nombre del Colegio"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos',key=1005)
        if len(municipio) > 0 and len(colegio) > 0:
            colegio_percentiles = data_atlantico[data_atlantico["Nombre del Colegio"].isin(colegio)]["PERCENTIL_SOCIALES_CIUDADANAS"]
            colegio_percentiles =  colegio_percentiles.sort_values().reset_index(drop=True)
            x=colegio_percentiles.tolist()
            # histograma de distribución normal.
            fig, ax = plt.subplots()
            ax.hist(x, bins=50)
            st.pyplot(fig)
            #-----------------------------------------------------------
            media=round(data_atlantico["PERCENTIL_SOCIALES_CIUDADANAS"].mean(),1)
            std=round(data_atlantico["PERCENTIL_SOCIALES_CIUDADANAS"].std(),1)
            x=colegio_percentiles.tolist()
            print(x)
            fig, ax = plt.subplots()
            ax.plot(x, norm.pdf(x, media, std))

            st.write(fig)
            
        text = '''---'''
        st.markdown(text)

        st.write("### Mejores percentiles de inglés por colegio.")
        df = data_atlantico[['Nombre del Colegio','COLE_MCPIO_UBICACION','PERCENTIL_LECTURA_CRITICA','PERCENTIL_MATEMATICAS','PERCENTIL_C_NATURALES','PERCENTIL_SOCIALES_CIUDADANAS','PERCENTIL_INGLES']]
        df=df.groupby(['Nombre del Colegio',"COLE_MCPIO_UBICACION"],dropna=False).agg(Percentil_ingle=('PERCENTIL_INGLES','mean')).reset_index()
        
        df=df.sort_values(by=['Percentil_ingle'],ascending=False).reset_index(drop=True)
        st.write(df,use_column_width=True)

        col_1, col_2, col_3 = st.columns(3)
        col_1.metric("Media",round(data_atlantico["PERCENTIL_INGLES"].mean(),1))
        col_2.metric("Varianza ",round(data_atlantico["PERCENTIL_INGLES"].var(),1))
        col_3.metric("Desviación Estandar",round(data_atlantico["PERCENTIL_INGLES"].std(),1))

        municipio = st.multiselect(label='Escoja un municipio',options=data_atlantico["COLE_MCPIO_UBICACION"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos',key=1006)
        colegio = st.multiselect(label='Escoja un colegio',options=data_atlantico[data_atlantico["COLE_MCPIO_UBICACION"].isin(municipio)]["Nombre del Colegio"].unique(),help='Si no se selecciona uno, por defecto se escogeran todos',key=1007)
        if len(municipio) > 0 and len(colegio) > 0:
            colegio_percentiles = data_atlantico[data_atlantico["Nombre del Colegio"].isin(colegio)]["PERCENTIL_INGLES"]
            colegio_percentiles =  colegio_percentiles.sort_values().reset_index(drop=True)
            x=colegio_percentiles.tolist()
            # histograma de distribución normal.
            fig, ax = plt.subplots()
            ax.hist(x, bins=50)
            st.pyplot(fig)
            #-----------------------------------------------------------
            media=round(data_atlantico["PERCENTIL_INGLES"].mean(),1)
            std=round(data_atlantico["PERCENTIL_INGLES"].std(),1)
            x=colegio_percentiles.tolist()
            print(x)
            fig, ax = plt.subplots()
            ax.plot(x, norm.pdf(x, media, std))

            st.write(fig)




app()
