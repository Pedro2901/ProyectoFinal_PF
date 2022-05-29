import os
import json
import streamlit as st 

import pickle as p
import pandas as pd


path = os.path.dirname(__file__)

def load_data(sample=True):
    if(sample):
        with open(f'{path}/data/sample10000.p','rb') as f:
            return p.load(f)
    else:
        return pd.read_csv(f'{path}/data/20202.csv')

#@st.cache
def geo_json_mncp():
    with open(f'{path}/data/municipios.geojson',"rb") as f:
        return json.load(f)

def load_pregunta(number):
     with open(f'{path}/data/pregunta{number}.p','rb') as f:
            return p.load(f)