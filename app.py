import streamlit as st
import pandas as pd
import geopandas as gpd

@st.cache_data
def load_data():
    causes_of_death_children = pd.read_csv('data/causes-of-death-in-children.csv')
    global_vaccination_coverage = pd.read_csv('data/global-vaccination-coverage.csv')
    reported_cases_of_measles = pd.read_csv('data/reported-cases-of-measles.csv')
    mortality_vs_expenditure = pd.read_csv('data/child-mortality-vs-health-expenditure.csv')
    oop_expenditures = pd.read_csv('data/share-of-out-of-pocket-expenditure-on-healthcare.csv')
    who_regions = pd.read_csv('data/who-regions.csv')
    return causes_of_death_children, global_vaccination_coverage, reported_cases_of_measles, mortality_vs_expenditure,oop_expenditures, who_regions

causes_of_death_children, global_vaccination_coverage, reported_cases_of_measles,mortality_vs_expenditure,oop_expenditures, who_regions = load_data()

for df in [global_vaccination_coverage, causes_of_death_children, reported_cases_of_measles, mortality_vs_expenditure,oop_expenditures, who_regions]:
    df.fillna(0, inplace=True)
    df["Code"] = df["Code"].astype(str)

@st.cache_resource
def load_geodata():
    geodata = gpd.read_file('geojson/custom.geo.json')
    return geodata

geodata = load_geodata()

if 'iso_a3' in geodata.columns:
    geodata = geodata.rename(columns={"iso_a3": "Code"})

st.session_state['datasets'] = (causes_of_death_children, global_vaccination_coverage, reported_cases_of_measles, mortality_vs_expenditure,oop_expenditures, who_regions)
st.session_state['geodata'] = geodata

st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a", ["Inicio", "Gráficas", "Mapa de Coropletas"])

st.markdown("""
    <style>
    .block-container {
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 5%;
        padding-right: 5%;
        text-align:center !important;
    }
    </style>
    """, unsafe_allow_html=True)
if page == "Inicio":
    from inicio import show_inicio
    show_inicio()
elif page == "Gráficas":
    #st.write("Gráficas")
    from graficas import show_graficas
    show_graficas()
elif page == "Mapa de Coropletas":
    from mapa_de_coropletas import show_mapa_de_coropletas
    show_mapa_de_coropletas()

