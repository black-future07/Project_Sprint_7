import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURACIÓN INICIAL Y CARGA DE DATOS ---

st.set_page_config(layout="wide", page_title="Análisis de Vehículos", page_icon="🚗")

@st.cache_data
def load_data():
    """Carga el CSV y realiza la limpieza/preparación inicial."""
    try:
        car_data = pd.read_csv('vehicles_us_bootcamp.csv')
        
        # Generar la columna 'manufacturer' a partir de la columna 'model'
        # Esto es clave para los selectores de fabricante
        car_data['manufacturer'] = car_data['model'].apply(lambda x: x.split(' ')[0].capitalize())
        
        return car_data
    except FileNotFoundError:
        st.error("Error: Archivo de datos no encontrado. Verifica el nombre.")
        st.stop()

df = load_data()

# --- 2. ENCABEZADO Y CONTROLES LATERALES ---

st.title('📈 Análisis Interactivo del Mercado de Vehículos')
st.markdown('***Explore la relación entre precio, kilometraje y condición.***')

st.sidebar.header('Filtros y Controles Globales')

# Filtro 1: Rango de Años del Modelo
min_year = int(df['model_year'].min()) if df['model_year'].min() > 0 else 1950 # Asegura un valor mínimo razonable
max_year = int(df['model_year'].max())
year_range = st.sidebar.slider(
    'Seleccionar Rango de Años del Modelo',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Aplicar el filtro de año
filtered_df = df[
    (df['model_year'] >= year_range[0]) & 
    (df['model_year'] <= year_range[1])
].copy()

# Opciones de Fabricantes disponibles después de filtrar
manufacturer_options = sorted(filtered_df['manufacturer'].unique())

st.sidebar.info(f"Mostrando {len(filtered_df)} de {len(df)} vehículos.")

# --- 3. SECCIÓN DE COMPARACIÓN DE FABRICANTES (NUEVA FUNCIONALIDAD) ---

st.header('1. Comparación de Distribución de Precios por Fabricante')

# Selector para Fabricante 1
manufacturer1 = st.selectbox(
    'Seleccionar Fabricante 1:',
    options=[''] + manufacturer_options,
    index=manufacturer_options.index('Chevrolet') + 1 if 'Chevrolet' in manufacturer_options else 0
)

# Selector para Fabricante 2
manufacturer2 = st.selectbox(
    'Seleccionar Fabricante 2:',
    options=[''] + manufacturer_options,
    index=manufacturer_options.index('Hyundai') + 1 if 'Hyundai' in manufacturer_options else 0
)

if manufacturer1 and manufacturer2:
    # Filtrar datos para los fabricantes seleccionados
    comparison_df = filtered_df[
        (filtered_df['manufacturer'] == manufacturer1) | 
        (filtered_df['manufacturer'] == manufacturer2)
    ]
    
    # Crear el histograma comparativo (similar al ejemplo que enviaste)
    fig_comp = px.histogram(
        comparison_df, 
        x="price", 
        color="manufacturer", 
        barmode="overlay", 
        title=f"Distribución de Precios: {manufacturer1} vs {manufacturer2}",
        opacity=0.7 
    )
    st.plotly_chart(fig_comp, use_container_width=True)
elif manufacturer1 or manufacturer2:
    st.info("Selecciona dos fabricantes para la comparación.")


# --- 4. VISUALIZACIONES BÁSICAS (REQUISITOS DEL BOOTCAMP) ---

st.markdown('---')
st.header('2. Análisis General de Datos')

col1, col2, col3 = st.columns(3)
with col1:
    build_histogram = st.checkbox('Mostrar Histograma de Precio y Condición', value=True)
with col2:
    build_scatter = st.checkbox('Mostrar Gráfico de Dispersión (Precio vs. Kilometraje)', value=True)
with col3:
    show_data_viewer = st.checkbox('Mostrar Visor de Datos', value=False)


# Histograma Mejorado (por condición/año)
if build_histogram:
    st.subheader('Distribución de Kilometraje por Condición (Visión del EDA)')
    fig_hist = px.histogram(
        filtered_df, 
        x="odometer", 
        color="condition",
        title="Frecuencia de Kilometraje por Condición del Vehículo",
        opacity=0.8,
        marginal="box"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# Gráfico de Dispersión (Precio vs. Odómetro)
if build_scatter:
    st.subheader('Relación Precio y Odómetro (Filtrado por Año)')
    fig_scatter = px.scatter(
        filtered_df, 
        x="odometer", 
        y="price", 
        title="Precio en función del Kilometraje (Odómetro)",
        color="condition", 
        hover_data=['model_year', 'model']
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# Visor de Datos
if show_data_viewer:
    st.subheader('Visor Interactivo de Datos Filtrados')
    st.dataframe(filtered_df, use_container_width=True)