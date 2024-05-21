import streamlit as st
import pandas as pd

df = pd.read_excel('grilla.xlsx')

# Título de la aplicación
st.title("Grilla")

# Sección de filtros
st.sidebar.subheader("Filtros")

# Filtro por Nombre
carrera = st.sidebar.multiselect("Carrera", options=df['Carrera'].unique(), default=df['Carrera'].unique())

# Filtro por Dia
dia = st.sidebar.multiselect("Dia", options=df['Dia'].unique(), default=df['Dia'].unique())

# Filtro por horario
hs_min, hs_max = st.sidebar.slider("Horario", min_value=int(df['Horario'].min()), max_value=int(df['Horario'].max()),value=(int(df['Horario'].min()), int(df['Horario'].max())))

# Aplicar filtros
df_filtrado = df[
    (df['Carrera'].isin(carrera)) &
    (df['Dia'].isin(dia)) &
    (df['Horario'] >= hs_min) &
    (df['Horario'] <= hs_max)
]

# Mostrar el DataFrame filtrado
st.dataframe(df_filtrado)

# Mostrar el número de resultados
st.write(f"Total de resultados: {df_filtrado.shape[0]}")
