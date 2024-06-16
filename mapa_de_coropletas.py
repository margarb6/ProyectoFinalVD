import streamlit as st
import folium
import pandas as pd
import json
import streamlit.components.v1 as components
import math
import geopandas as gpd
from branca.colormap import LinearColormap

def show_mapa_de_coropletas():
    # Obtener los datos cargados desde app.py
    causes_of_death_children = st.session_state['datasets'][0]
    global_vaccination_coverage = st.session_state['datasets'][1]
    geodata = st.session_state['geodata']

   

    def max_deaths(df, disease_column):
        max_death = df[disease_column].max()
        print(max_death)
        return math.ceil(max_death / 1000) * 1000

    # Crear un mapa de coropletas usando GeoDataFrame
    def create_choropleth_map(data, geodata, key_on, fill_color, fill_opacity, line_opacity, legend_name, bins):
        m = folium.Map(location=[20, 0], zoom_start=1.1)
       
        # Merge data with geodata
        merged = geodata.merge(data, left_on='Code', right_on='code')
     
        choropleth = folium.Choropleth(
            geo_data=geodata,
            data=data,
            columns=['country', 'value'],
            key_on=key_on,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            line_opacity=line_opacity,
            legend_name=legend_name,
            bins=bins

        )
        choropleth.color_scale.width=500
        
        
        choropleth.add_to(m)

        folium.GeoJson(
            merged,
            style_function=lambda feature: {
            'fillColor': 'transparent',
            'color': 'transparent',
            'weight': 0,
            'fillOpacity': 0
        },
            highlight_function=lambda feature: {
                'fillColor': '#FFFF00',
                'color': 'grey',
                'weight': 2,
                'fillOpacity': 0.5
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['country', 'value'],
                aliases=['Country:', 'Value:'],
                localize=True,
                sticky=False,
                labels=True,
                style=("background-color: white; color: black; font-weight: bold;")
            )
        ).add_to(m)

        # colormap.add_to(m)  # Add the colormap to the map

        return m

    # Filtrar los datos por año y vacuna/muerte
    def filter_data(df, year, column):
        filtered_df = df[df['Year'] == year]
        filtered_df = filtered_df[['Entity', 'Code', column]]
        filtered_df.columns = ['country', 'code', 'value']
      
        return filtered_df

    vaccines = {
        'BCG': 'BCG (% of one-year-olds immunized)',
        'HepB3': 'HepB3 (% of one-year-olds immunized)',
        'Hib3': 'Hib3 (% of one-year-olds immunized)',
        'MCV1': 'MCV1 (% of one-year-olds immunized)',
        'PCV3': 'PCV3 (% of one-year-olds immunized)',
        'RotaC': 'RotaC (% of one-year-olds immunized)',
        'DTP3': 'DTP3 (% of one-year-olds immunized)'
    }

    deaths = {
        'BCG': {
            'column': 'Deaths - Tuberculosis - Sex: Both - Age: Under 5 (Number)',
            'bins': [0, 1000,  15000, 35000, 75000,100000 ]
        },
        'HepB3': {
            'column': 'Deaths - HIV/AIDS - Sex: Both - Age: Under 5 (Number)',
            'bins': [0, 10000, 75000, 100000]
        },
        'Hib3': {
            'column': 'Deaths - Meningitis - Sex: Both - Age: Under 5 (Number)',
            'bins': [0, 1000, 10000, 100000]
        },
        'MCV1': {
            'column': 'Deaths - Measles - Sex: Both - Age: Under 5 (Number)',
            'bins': [0  , 20000, 100000, 200000, 500000]
        },
        'PCV3': {
            'column': 'Deaths - Lower respiratory infections - Sex: Both - Age: Under 5 (Number)',
            'bins': [0, 1000, 10000, 100000]
        },
        'RotaC': {
            'column': 'Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Number)',
            'bins': [0,  10000, 40000, 100000, 150000]
        },
        'DTP3': {
            'column': 'Deaths - Whooping cough - Sex: Both - Age: Under 5 (Number)',
            'bins': [0  , 10000, 20000, 50000, 100000]
        }
    }

    # Selección de año mediante slider
    years = global_vaccination_coverage['Year'].unique()
    print(years)
    print(causes_of_death_children['Year'].unique())
    min_year=max(global_vaccination_coverage['Year'].min(),causes_of_death_children['Year'].min())
    max_year=min(global_vaccination_coverage['Year'].max(),causes_of_death_children['Year'].max())
    #nos quedamos solo con los años que estén entre ambos años

    causes_of_death_children=causes_of_death_children[(causes_of_death_children['Year']>=min_year) & (causes_of_death_children['Year']<=max_year)]
    global_vaccination_coverage=global_vaccination_coverage[(global_vaccination_coverage['Year']>=min_year) & (global_vaccination_coverage['Year']<=max_year)]


    selected_year = st.slider("Selecciona el año", int(min_year), int(max_year), int(min_year))

    # Selección de vacuna
    selected_vaccine = st.selectbox("Selecciona la vacuna", list(vaccines.keys()))

    # Filtrar datos
    vaccination_selected_year = filter_data(global_vaccination_coverage, selected_year, vaccines[selected_vaccine])
    death_selected_year = filter_data(causes_of_death_children, selected_year,deaths[selected_vaccine]['column'] )
   

    # Añadimos el maximo posible para el seleccionado
    deaths[selected_vaccine]['bins'].append(max_deaths(causes_of_death_children, deaths[selected_vaccine]['column']))
    print(deaths[selected_vaccine]['bins'])

    # Crear mapas
    map_vaccination = create_choropleth_map(
        vaccination_selected_year,
        geodata,
        'properties.name',
        'viridis',
        0.7,
        0.2,
        f'Cobertura de vacunación {selected_vaccine} en {selected_year} (%)',
        bins=[0, 50, 60, 70, 80, 90, 100]
    )

    map_deaths = create_choropleth_map(
        death_selected_year,
        geodata,
        'properties.name',
        'viridis',
        0.7,
        0.2,
        f'Muertes por {str(deaths[selected_vaccine]["column"])} en {selected_year} (Número)',
        bins=deaths[selected_vaccine]['bins']
    )
    
  

    # Mostrar el título y el slider en Streamlit
    st.title(f"Mapa de Cobertura de Vacunación y Muertes en {selected_year}")
    st.write(f"Este mapa muestra la cobertura de vacunación y las muertes provocadas por la enfermedad correspondiente en {selected_year}.")

    # Estilos CSS para ampliar el contenedor HTML
    st.markdown("""
        <style>
        .block-container {
            max-width: 90% !important;
            width: 80% !important;
            padding-left: 5%;
            padding-right: 5%;
        }
        </style>
        """, unsafe_allow_html=True)

    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns(2)

    # Renderizar el primer mapa en HTML (vacunación)
    with col1:
        st.subheader("Cobertura de Vacunación")
        map_html1 = map_vaccination._repr_html_()
        components.html(map_html1, height=600)

    # Renderizar el segundo mapa en HTML (muertes)
    with col2:
        st.subheader("Muertes")
        map_html2 = map_deaths._repr_html_()
        components.html(map_html2, height=600)

