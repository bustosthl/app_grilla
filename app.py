import streamlit as st
import pandas as pd, datetime as dt

df = pd.read_excel('grilla.xlsx')

# Título de la aplicación
st.title("Grilla")

# Sección de filtros
st.sidebar.subheader("Filtros")

# Filtro por Nombre
carrera = st.sidebar.multiselect("Carrera", options=df['Carrera'].unique(), default=['SOCIO','COMU']) # default = df['Carrera'].unique()

# Filtro por clave
clave = st.sidebar.multiselect("Clave", options=df['Materia clave'].unique(), default=['si']) 

# Filtro por Dia
dic = {'0':'lunes','1':'martes','2':'miercoles','3':'jueves','4':'viernes'}
hoy = '0'
hoy = dt.datetime.now().weekday()
for k in dic.keys():
    if int(hoy) >= 5: 
        hoy = '4'
    hoy = str(hoy).replace(k, dic[k])
dia = st.sidebar.multiselect("Dia", options=df['Dia'].unique(), default=[hoy]) # df['Dia'].unique()

# Filtro por horario
hs_min, hs_max = st.sidebar.slider("Horario", min_value=int(df['Horario'].min()), max_value=int(df['Horario'].max()),value=(int(df['Horario'].min()), int(df['Horario'].max())))

# Aplicar filtros
df_filtrado = df[
    (df['Carrera'].isin(carrera)) &
    (df['Materia clave'].isin(clave)) &
    (df['Dia'].isin(dia)) &
    (df['Horario'] >= hs_min) &
    (df['Horario'] <= hs_max)
]

# Mostrar el DataFrame filtrado
def color(value):
    if value=='SOCIO':
        color = 'salmon'
    elif value=='COMU':
        color = 'lightgreen'
    elif value=='CP':
        color = 'skyblue'
    elif value=='TS':
        color = 'violet'
    else:
        return
    return f'background-color: {color}'

df_style = df_filtrado.style.applymap(color, subset=['Carrera']).background_gradient(subset=['Horario'], cmap='Greys')

st.dataframe(df_filtrado, hide_index=True, use_container_width=True, )

# Mostrar el número de resultados
st.write(f"Total de resultados: {df_filtrado.shape[0]}")