import streamlit as st
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import plotly.graph_objects as go
import pandas as pd
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
def show_graficas():
    causes_of_death_children, global_vaccination_coverage,  reported_cases_of_measles, mortality_vs_expenditure, out_of_pocket_expenditure, who_regions = st.session_state['datasets']
     # Set up tabs
    tab1, tab2 = st.tabs(["Countries", "WHO Regions"])

    with tab1:
        st.header('Información por País')
       # Determine the last available year in the death data
        last_year = causes_of_death_children['Year'].max()

        # Filter death data for the last year
        data_last_year = causes_of_death_children[causes_of_death_children['Year'] == last_year]

        # Rename columns to shorten the names
        data_last_year.columns = [
            'Entity', 'Code', 'Year', 'Malaria', 'HIV/AIDS', 'Meningitis', 'Nutritional deficiencies',
            'Other neonatal disorders', 'Whooping cough', 'Lower respiratory infections', 'Congenital birth defects',
            'Measles', 'Neonatal sepsis and infections', 'Neonatal encephalopathy due to birth asphyxia and trauma',
            'Drowning', 'Tuberculosis', 'Neonatal preterm birth', 'Diarrheal diseases', 'Neoplasms', 'Syphilis'
        ]

        # Set up the Streamlit interface
        #cojo solo los datos con code
        data_last_year = data_last_year[data_last_year['Code'] != str(0)]
        # Country selector for both datasets
        country_list = data_last_year['Entity'].unique()
        selected_country = st.selectbox("Selecciona un País", country_list)

        # Filter data for the selected country
        country_data = data_last_year[data_last_year['Entity'] == selected_country]

        # Prepare data for plotting deaths
        death_causes = country_data.drop(columns=['Entity', 'Code', 'Year']).melt(var_name='Cause', value_name='Deaths')

        # Creating the bar graph for causes of death
        fig_deaths = px.bar(death_causes, x='Cause', y='Deaths', 
                    title=f"Causes of Death in {selected_country} ({last_year}) - Sex: Both, Age: Under 5 (Number)")
        st.plotly_chart(fig_deaths)


        # Obtener los años y países únicos
        years = global_vaccination_coverage['Year'].unique()
        countries = global_vaccination_coverage['Entity'].unique()

        # Selección de año mediante slider
        selected_year = st.slider("Selecciona el año", int(years.min()), int(years.max()), int(years.min()))

        # Filtrar datos por país y año
        filtered_data = global_vaccination_coverage[(global_vaccination_coverage['Year'] == selected_year) & (global_vaccination_coverage['Entity'] == selected_country)]

        if not filtered_data.empty:
            # Obtener los valores de vacunación
            categories = [
                'BCG (% of one-year-olds immunized)', 'HepB3 (% of one-year-olds immunized)', 'Hib3 (% of one-year-olds immunized)', 
                'IPV1 (% of one-year-olds immunized)', 'MCV1 (% of one-year-olds immunized)', 'PCV3 (% of one-year-olds immunized)', 
                'Pol3 (% of one-year-olds immunized)', 'RCV1 (% of one-year-olds immunized)', 'RotaC (% of one-year-olds immunized)', 
                'YFV (% of one-year-olds immunized)', 'DTP3 (% of one-year-olds immunized)'
            ]
            values = [
                filtered_data.iloc[0]['BCG (% of one-year-olds immunized)'],
                filtered_data.iloc[0]['HepB3 (% of one-year-olds immunized)'],
                filtered_data.iloc[0]['Hib3 (% of one-year-olds immunized)'],
                filtered_data.iloc[0]['IPV1 (% of one-year-olds immunized)'],
                filtered_data.iloc[0]['MCV1 (% of one-year-olds immunized)'],
                filtered_data.iloc[0]['PCV3 (% of one-year-olds immunized)'],
                filtered_data.iloc[0]['Pol3 (% of one-year-olds immunized)'],
                filtered_data.iloc[0]['RCV1 (% of one-year-olds immunized)'],
                filtered_data.iloc[0]['RotaC (% of one-year-olds immunized)'],
                filtered_data.iloc[0]['YFV (% of one-year-olds immunized)'],
                filtered_data.iloc[0]['DTP3 (% of one-year-olds immunized)']
            ]

            # Crear y mostrar el gráfico de radar usando Plotly
            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=f'Tasa de vacunación en {selected_country} ({selected_year})'
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    ),
                ),
                showlegend=False,
                title=f'Tasa de vacunación en {selected_country} ({selected_year})'
            )

            st.plotly_chart(fig)
        else:
            st.write(f"No hay datos disponibles para {selected_country} en {selected_year}.")

        # Prepare and plot the healthcare expenditure data
        expenditure_data = out_of_pocket_expenditure[out_of_pocket_expenditure['Entity'] == selected_country]
        mortality_data = mortality_vs_expenditure[mortality_vs_expenditure['Entity'] == selected_country]

        # Merge expenditure datasets on 'Year' after selecting the required expenditure columns
        expenditure_comparison = pd.merge(expenditure_data[['Year', 'Out-of-pocket expenditure per capita, PPP (current international $)']],
                                        mortality_data[['Year', 'Current health expenditure per capita, PPP (current international $)']],
                                        on='Year', how='inner')

        # Renaming columns for clarity
        expenditure_comparison.rename(columns={
            'Out-of-pocket expenditure per capita, PPP (current international $)': 'Out-of-pocket Expenditure PPP ($)',
            'Current health expenditure per capita, PPP (current international $)': 'Health Expenditure PPP ($)'
        }, inplace=True)

        # Plotting the comparison line graph
        fig_expenditure = px.line(expenditure_comparison, x='Year', y=['Out-of-pocket Expenditure PPP ($)', 'Health Expenditure PPP ($)'],
                                title=f"Healthcare Expenditure Over Time in {selected_country} (PPP $)")
        st.plotly_chart(fig_expenditure)

            
    with tab2:
        st.header('WHO Regions')
        #Creo un selector de regiones
        col1, col2, col3 = st.columns(3)
        with col1:
            region = st.selectbox("Seleccione una región", who_regions['WHO region'].unique())
            # Selector de año
            # Conservo datos entre 2000 y 2021
            who_regions = who_regions[['Code', 'WHO region']]
            # Añado una columna con las regiones
            mortality_vs_expenditure = mortality_vs_expenditure.merge(who_regions, on='Code')
            mortality_vs_expenditure = mortality_vs_expenditure[(mortality_vs_expenditure['Year'] >= 2000) & (mortality_vs_expenditure['Year'] <= 2020)]
            region_countries = mortality_vs_expenditure[mortality_vs_expenditure['WHO region'] == region]['Code'].tolist()
        with col3:

            world = gpd.read_file('geojson/custom.geo.json')
            region_map = world[world['iso_a3'].isin(region_countries)]
            map_center = [region_map.geometry.centroid.y.mean(), region_map.geometry.centroid.x.mean()]
            m = folium.Map(location=[0,0], zoom_start=0.5, scrollWheelZoom=False, dragging=False,tiles=folium.TileLayer(no_wrap=True),zoom_control=False)

            # Añadir los países de la región al mapa
            folium.GeoJson(region_map,).add_to(m)

            # Mostrar el mapa en Streamlit
            folium_static(m, width=490, height=430)

        
        years = mortality_vs_expenditure['Year'].unique()
        selected_year = st.slider("Selecciona el año", int(years.min()), int(years.max()), int(years.max()))
      
        
        print(mortality_vs_expenditure.head())
        # Filtro por región
        mortality_vs_expenditure = mortality_vs_expenditure[mortality_vs_expenditure['WHO region'] == region]
        # mortality_vs_expenditure_year = mortality_vs_expenditure[mortality_vs_expenditure['Year'] == selected_year]

        # Relación entre Gasto en Salud y Mortalidad Infantil
        st.title("Relación entre Gasto en Salud y Mortalidad Infantil")

        # Renombrar columnas para simplificar
        mortality_vs_expenditure = mortality_vs_expenditure.rename(columns={
            'Observation value - Unit of measure: Deaths per 100 live births - Indicator: Under-five mortality rate - Sex: Both sexes - Wealth quintile: All wealth quintiles': 'Mortality Rate',
            'Current health expenditure per capita, PPP (current international $)': 'Health Expenditure per Capita'
        })
        mortality_vs_expenditure_year = mortality_vs_expenditure[mortality_vs_expenditure['Year'] == selected_year]
        fig_scatter = px.scatter(mortality_vs_expenditure_year, x='Health Expenditure per Capita', y='Mortality Rate', 
                                title='Relación entre Gasto en Salud y Mortalidad Infantil',
                                labels={'Health Expenditure per Capita': 'Gasto en Salud per Cápita (USD)', 'Mortality Rate': 'Tasa de Mortalidad Infantil (por 100 nacidos vivos)', 'Entity': 'País'},
                                color='Entity')
        st.plotly_chart(fig_scatter)
        # Grafico de lineas
        st.title("Evolución del Gasto en Salud ")

        # Plotting the line graph with only the first 10 lines visible initially
        fig_line = go.Figure()

        entities = mortality_vs_expenditure['Entity'].unique()
        for i, entity in enumerate(entities):
            entity_data = mortality_vs_expenditure[mortality_vs_expenditure['Entity'] == entity]
            fig_line.add_trace(go.Scatter(
                x=entity_data['Year'], 
                y=entity_data['Health Expenditure per Capita'],
                mode='lines',
                name=entity,
                visible=True if i < 10 else 'legendonly'
            ))

        fig_line.update_layout(title='Evolución del Gasto en Salud', showlegend=True)
        st.plotly_chart(fig_line)

        #GRAFICO DE RADAR
        # Filtrar datos por país y año
        global_vaccination_coverage = global_vaccination_coverage.merge(who_regions,on='Code')
        filtered_data = global_vaccination_coverage[(global_vaccination_coverage['Year'] == selected_year) & (global_vaccination_coverage['WHO region'] == region )]

        if not filtered_data.empty:
            # Obtener los valores de vacunación
            categories = ['BCG (% of one-year-olds immunized)','HepB3 (% of one-year-olds immunized)','Hib3 (% of one-year-olds immunized)','IPV1 (% of one-year-olds immunized)','MCV1 (% of one-year-olds immunized)','PCV3 (% of one-year-olds immunized)','Pol3 (% of one-year-olds immunized)', 'RCV1 (% of one-year-olds immunized)', 'RotaC (% of one-year-olds immunized)','YFV (% of one-year-olds immunized)', 'DTP3 (% of one-year-olds immunized)']
            values = filtered_data[categories].mean().values.tolist()

            # Crear y mostrar el gráfico de radar usando Plotly
            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=f'Tasa de vacunación en ({selected_year})'
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    ),
                ),
                showlegend=False,
                title=f'Tasa de vacunación en ({selected_year})'
            )

            st.plotly_chart(fig)
        else:
            st.write(f"No hay datos disponibles para en {selected_year}.")

  