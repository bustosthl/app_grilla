import streamlit as st
import pandas as pd, datetime as dt
from streamlit_javascript import st_javascript

st.set_page_config(page_title='Grilla Sociales', 
                   page_icon='images/favicon.png')

df = pd.read_excel('202503_grilla.xlsx', sheet_name='consolidado')
df['Dia'] = df['Dia'].astype(str).str.lower()

st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")
if st_theme == "dark":
    ruta_imagen = 'images/emergente pp logo blanco.png'
    ruta_imagen = 'images/mella logo fondo oscuro.png'
else:
    ruta_imagen = 'images/emergente pp logo negro.png'
    ruta_imagen = 'images/mella logo fondo claro.png'

# Título de la aplicación
st.title("Grilla Sociales-UBA")

# Sección de filtros
st.sidebar.subheader("Filtros")

# Filtro por Nombre
carrera = st.sidebar.multiselect("Carrera", options=df['Carrera'].unique(), default=['SOCIO','COMU']) # default = df['Carrera'].unique()
ala = st.sidebar.multiselect("ala", options=df['ala'].unique(), default=['SJ','HU','SG']) # default = df['Carrera'].unique()

# Filtro por clave
clave = st.sidebar.checkbox('Materias clave', True)
if clave:
    filtro_clave = df['Materia clave'].isin(['si'])
else:
    filtro_clave = df['Materia clave'].isin(['si','no'])

# Filtro por Dia
dic = {'0':'lunes','1':'martes','2':'miercoles','3':'jueves','4':'viernes'}
hoy = '0'
hoy = dt.datetime.now().weekday()
if hoy >= 5: 
    hoy = '0'
for k in dic.keys():
    hoy = str(hoy).replace(k, dic[k])

dia = st.sidebar.multiselect("Dia", options=df['Dia'].unique(), default=[hoy]) # df['Dia'].unique()

# Filtro por horario
hs_min, hs_max = st.sidebar.slider("Horario", min_value=int(df['Horario'].min()), max_value=int(df['Horario'].max()),value=(int(df['Horario'].min()), int(df['Horario'].max())))

# Aplicar filtros
df_filtrado = df[
    (df['Carrera'].isin(carrera)) &
    (df['ala'].isin(ala)) &
    #(df['Materia clave'].isin(clave)) &
    (filtro_clave) &
    (df['Dia'].isin(dia)) &
    (df['Horario'] >= hs_min) &
    (df['Horario'] <= hs_max)
]

# Mostrar el DataFrame filtrado
def color(value):
    if value=='SOCIO':
        color = 'darkred'
    elif value=='COMU':
        color = 'darkgreen'
    elif value=='CP':
        color = 'navy'
    elif value=='TS':
        color = 'violet'
    else:
        return
    return f'background-color: {color}'

df_style = df_filtrado.dropna(axis=1, how='all').style.map(color, subset=['Carrera'])

st.dataframe(df_style, hide_index=True, use_container_width=True, )

# Mostrar el número de resultados
st.write(f"Total de resultados: {df_filtrado.shape[0]}")
st.image(ruta_imagen)
