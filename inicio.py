import streamlit as st

def show_inicio():
        
    # Título de la página
    st.title("Proyecto Académico: Web Visualización de Datos")
    
    st.markdown("""
        <style>
        .block-container {
            max-width: 100% !important;
            width: 100% !important;
            padding-left: 5%;
            padding-right: 5%;
            text-align:left !important;
        }
        </style>
        """, unsafe_allow_html=True)
    # Descripción del proyecto
    st.markdown("""
        ## Bienvenido al Proyecto de Visualización de Datos de Marta García

        Este proyecto tiene como objetivo analizar y visualizar datos de salud y mortalidad infantil a nivel global. Utilizamos la librería Streamlit para crear una interfaz interactiva que permite a los usuarios explorar distintos aspectos de los datos a través de gráficas y mapas.

        ### Funcionalidades del Proyecto

        - **Gráficas Interactivas**: 
        - Análisis de causas de mortalidad infantil.
        - Cobertura de vacunación
        - Comparación de mortalidad y gasto en salud a lo largo del tiempo.

        - **Mapa de Coropletas**:
        - Visualización de la cobertura de vacunación y las muertes relacionadas con enfermedades específicas por país y año.
        - Interactividad para seleccionar diferentes parámetros y años para personalizar la visualización.

      
        """)