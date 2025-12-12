import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Ejemplo de pestañas en Streamlit")

tab1, tab2, tab3 = st.tabs(["Overview", "Histograma", "Mapa"])

with tab1:
    st.subheader("Overview")
    st.write("Aquí van tus KPIs, texto introductorio, etc.")
    st.markdown("""# 📊 Tablero de Inteligencia de Negocios

**Universidad Panamericana CDMX — Facultad de Ingeniería**

<img src="https://posgrados-panamericana.up.edu.mx/hs-fs/hubfs/logo%20posgrados%20con%20espacio.png?width=137&name=logo%20posgrados%20con%20espacio.png" width = 100>

Este repositorio contiene el desarrollo de un **tablero interactivo** creado para la clase de **Inteligencia de Negocios**, cuyo objetivo es analizar datos reales y generar visualizaciones accionables que apoyen la toma de decisiones en contextos empresariales.

---

## 🎯 Objetivo del Proyecto

El propósito de este tablero es **transformar datos brutos en información clara, visual y estratégica**, permitiendo identificar patrones, tendencias y oportunidades de mejora mediante técnicas de Business Intelligence.

---

## 🧠 Funcionalidades Principales

* 📈 Visualizaciones dinámicas para análisis descriptivo.
* 📅 Filtros interactivos (por periodo, categoría, unidad de negocio, etc.).
* 🔍 Análisis comparativo entre métricas clave.
* 🧮 Cálculo automático de KPIs relevantes.
* 📤 Exportación de insights o reportes (opcional según tu implementación).

---

## 📂 Estructura del Repositorio

```
├── data/               # Conjuntos de datos utilizados (limpios o raw)
├── dashboards/         # Archivos del tablero (Power BI, Tableau, Python, etc.)
├── src/                # Código fuente para transformación o análisis
├── assets/             # Imágenes, logos y recursos usados en el tablero
└── README.md           # Documentación principal del proyecto
```

*Puedo personalizar esta sección con tus carpetas reales si me dices cómo está organizado tu repo.*

---

## 🛠️ Tecnologías Utilizadas

Dependiendo de tu implementación, ajusta esta sección:

* **Power BI** / **Tableau** / **Looker Studio**
* **Python (pandas, numpy, matplotlib, seaborn, plotly)**
* **Excel / CSV para ingesta de datos**
* **Git / GitHub para control de versiones**

---

## 📑 Metodología

1. **Recolección y limpieza de datos**

   * Normalización, manejo de nulos, estandarización de formatos.

2. **Transformación y modelado**

   * Creación de columnas calculadas.
   * Definición de medidas DAX (si aplica).
   * Modelado estrella o snowflake según el caso.

3. **Construcción del tablero**

   * Selección de gráficos.
   * Diseño enfocado en claridad y usabilidad.
   * Implementación de KPIs y filtros.

4. **Entrega y documentación**

   * Explicación del contexto del negocio.
   * Justificación de métricas seleccionadas.
   * Conclusiones clave.

---

## 📌 KPIs Incluidos

*(Puedo completarlos si me dices cuáles usa tu tablero)*

* Ingresos totales
* Margen operativo
* Crecimiento mensual
* Rotación de clientes
* Indicadores personalizados según el caso de estudio

---

## 📥 Cómo Ejecutar o Visualizar el Tablero

### Si usas Power BI:

1. Descargar el archivo `.pbix` del repositorio.
2. Abrirlo con **Power BI Desktop**.

### Si usas Tableau:

1. Abrir el archivo `.twbx` o conectarte a los datos incluidos.

### Si usas un dashboard en Python:

```bash
pip install -r requirements.txt
python app.py
```

---

## 👨‍🎓 Sobre el Proyecto

Este tablero fue desarrollado como parte de la materia **Inteligencia de Negocios** impartida en la **Universidad Panamericana CDMX**.
El enfoque es académico, pero con estándares profesionales aplicables a escenarios reales de análisis empresarial.

---

## 📧 Contacto

**Autor:** Eduardo Llamas Brito
**Email:** *(puedo agregarlo si quieres)*
**GitHub:** *tu usuario*""")

with tab2:
    st.subheader("Histograma")
    st.write("Aquí podrías poner tus gráficos de categorías vs estrellas.")

# -----------------------------
# 1. Cargar datos
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Restaurantes USA 1.csv")
    return df

df = load_data()

# -----------------------------
# 2. Detectar columnas categóricas (0/1) y filtrarlas
# -----------------------------
# Columnas que NO queremos como categorías
columnas_excluir = [
    'name', 'address', 'city', 'state', 'latitude', 'longitude',
    'stars', 'review_count', 'is_open', 'attributes', 'Restaurants', 'Food', 'Nightlife', 'Bars'
]

# Detectar columnas binarias (0/1)
categorical_cols = [
    col for col in df.columns
    if df[col].dropna().isin([0, 1]).all()
]

# Filtrarlas quitando las excluidas
categorical_filtradas = [
    col for col in categorical_cols
    if col not in columnas_excluir
]

# -----------------------------
# 3. Sidebar: controles (estado, rango estrellas, top N)
# -----------------------------
st.sidebar.title("Filtros")

# Estado
state_options = ["Todos"] + sorted(df["state"].dropna().unique().tolist())
estado = st.sidebar.selectbox("Estado", state_options, index=0)

# Rango de estrellas
min_star = float(df["stars"].dropna().min())
max_star = float(df["stars"].dropna().max())

rango_estrellas = st.sidebar.slider(
    "Rango de estrellas",
    min_value=min_star,
    max_value=max_star,
    value=(min_star, max_star),
    step=0.5
)

# Top N categorías a mostrar
top_n = st.sidebar.slider(
    "Top N categorías",
    min_value=5,
    max_value=50,
    value=20,
    step=5
)

# -----------------------------
# 4. Filtrado del DataFrame
# -----------------------------
rmin, rmax = rango_estrellas

df_filtrado = df.copy()

if estado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["state"] == estado]

df_filtrado = df_filtrado[
    (df_filtrado["stars"] >= rmin) &
    (df_filtrado["stars"] <= rmax)
]

st.title("Análisis de tipos de restaurante por rating y estado")

# Mostrar info de filtros
subtitulo_estado = f" en {estado}" if estado != "Todos" else ""
st.write(f"Mostrando restaurantes{subtitulo_estado} con rating entre **{rmin}** y **{rmax}**.")
st.write(f"Restaurantes filtrados: **{len(df_filtrado)}**")

if df_filtrado.empty:
    st.warning("No hay restaurantes que coincidan con estos filtros.")
else:
    # -----------------------------
    # 5. Recuento de categorías
    # -----------------------------
    category_counts = (
        df_filtrado[categorical_filtradas]
        .sum()
        .sort_values(ascending=False)
    )

    # -----------------------------
    # 6. Gráfica de barras
    # -----------------------------
    st.subheader(f"Top {top_n} tipos de restaurante{subtitulo_estado}")

    fig, ax = plt.subplots(figsize=(12, 6))
    category_counts.head(top_n).plot(kind="bar", edgecolor="black", ax=ax)

    ax.set_xlabel("Categoría")
    ax.set_ylabel("Número de restaurantes")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    st.pyplot(fig)

    # Opcional: tabla abajo
    st.subheader("Tabla de recuentos (Top categorías)")
    st.dataframe(category_counts.head(top_n).rename("count").to_frame())


with tab3:
    st.subheader("Mapa")
    st.write("Aquí iría un mapa con la ubicación de los restaurantes.")
    # Ejemplo:
    # st.map(df[["latitude", "longitude"]])
