import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard interactivo - Proyecto Final")

tab1, tab2 = st.tabs(["Overview", "Gráficos"])

with tab1:
    st.subheader("Overview")
    st.markdown("""# 📊 Tablero de Inteligencia de Negocios

**Universidad Panamericana CDMX — Facultad de Ingeniería**

<img src="https://posgrados-panamericana.up.edu.mx/hs-fs/hubfs/logo%20posgrados%20con%20espacio.png?width=137&name=logo%20posgrados%20con%20espacio.png" width = 100>

Este repositorio contiene el desarrollo de un **tablero interactivo** creado para la clase de **Inteligencia de Negocios**, cuyo objetivo es analizar datos reales y generar visualizaciones accionables que apoyen la toma de decisiones en contextos empresariales.

---

## 🎯 Objetivo del Proyecto

El propósito de este tablero es **permitirle al usuario visualizar tendencias en el sector restaurantero con base en reviews de yelp**, permitiendo identificar patrones, tendencias y oportunidades de mejora mediante técnicas de Business Intelligence.

---

## 🧠 Funcionalidades Principales

* 📈 Visualizaciones dinámicas para análisis descriptivo.
* 📅 Filtros interactivos (rating, review, zona, tipo de restaurante).
* 🔍 Análisis comparativo entre métricas clave.

---

## 🛠️ Tecnologías Utilizadas

* **Python (pandas, numpy, matplotlib, seaborn)**

---

## 📑 Metodología

1. **Recolección y limpieza de datos**

   * Normalización, manejo de nulos, estandarización de formatos.

2. **Transformación y modelado**

   * Creación de columnas calculadas.

3. **Construcción del tablero**

   * Diseño enfocado en claridad y usabilidad.

---

## 👨‍🎓 Sobre el Proyecto

Este tablero fue desarrollado como parte de la materia **Inteligencia de Negocios** impartida en la **Universidad Panamericana CDMX**.
El enfoque es académico, pero con estándares profesionales aplicables a escenarios reales de análisis empresarial.

---

## 📧 Contacto

**Autores:** Eduardo Llamas Brito, Emilio Hernández Contreras, Emilio Ramírez Martínez del Campo, Emilio Ignacio Romero Martínez
**Email:** 0245351@up.edu.mx, 0212417@up.edu.mx, 0212517@up.edu.mx, 0241731@up.edu.mx

""")


with tab2:
    st.markdown("""
    Este dashboard está pensado para darle al usuario una idea general de métricas importantes para determinar la vialidad y aceptación general de algunos tipos de restaurantes en estados seleccionados de los Estados Unidos de América
    """)
    st.subheader("Análisis por tipos de restaurante")

    @st.cache_data
    def load_data():
        df = pd.read_csv("Restaurantes USA 1.csv")
        df["state"] = df["state"].astype(str).str.strip()
        return df
    
    df = load_data()

    columnas_excluir = [
        'name', 'address', 'city', 'state', 'latitude', 'longitude',
        'stars', 'review_count', 'is_open', 'attributes',
        'Restaurants', 'Food', 'Nightlife', 'Bars'
    ]
    
    categorical_cols = [
        col for col in df.columns
        if df[col].dropna().isin([0, 1]).all()
    ]
    
    categorical_filtradas = [
        col for col in categorical_cols
        if col not in columnas_excluir
    ]

    state_options = ["Todos"] + sorted(df["state"].dropna().unique().tolist())

    st.sidebar.markdown("### Filtros · Histograma")
    estado_hist = st.sidebar.selectbox(
        "Estado (histograma)",
        state_options,
        index=0,
        key="estado_hist"
    )
    
    min_star = float(df["stars"].dropna().min())
    max_star = float(df["stars"].dropna().max())
    
    rango_estrellas = st.sidebar.slider(
        "Rango de estrellas",
        min_value=min_star,
        max_value=max_star,
        value=(min_star, max_star),
        step=0.5,
        key="rango_estrellas"
    )
    
    top_n_hist = st.sidebar.slider(
        "Top N categorías (histograma)",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
        key="top_n_hist"
    )

    st.sidebar.markdown("### Filtros · Ranking de categorías")
    estado_rank = st.sidebar.selectbox(
        "Estado (ranking)",
        state_options,
        index=0,
        key="estado_rank"
    )
    
    top_n_rank = st.sidebar.slider(
        "Top N categorías (ranking)",
        min_value=5,
        max_value=30,
        value=15,
        step=5,
        key="top_n_rank"
    )
    
    min_restaurantes = st.sidebar.slider(
        "Mínimo de restaurantes por categoría",
        min_value=10,
        max_value=200,
        value=60,
        step=10,
        key="min_restaurantes"
    )

    st.markdown("## Histograma de tipos de restaurante")

    rmin, rmax = rango_estrellas
    df_filtrado_hist = df.copy()
    
    if estado_hist != "Todos":
        df_filtrado_hist = df_filtrado_hist[df_filtrado_hist["state"] == estado_hist]
    
    df_filtrado_hist = df_filtrado_hist[
        (df_filtrado_hist["stars"] >= rmin) &
        (df_filtrado_hist["stars"] <= rmax)
    ]
    
    subtitulo_estado_hist = f" en {estado_hist}" if estado_hist != "Todos" else ""
    st.write(
        f"Mostrando restaurantes{subtitulo_estado_hist} con rating entre "
        f"**{rmin}** y **{rmax}**."
    )
    st.write(f"Restaurantes filtrados (histograma): **{len(df_filtrado_hist)}**")
    
    if df_filtrado_hist.empty:
        st.warning("No hay restaurantes que coincidan con estos filtros (histograma).")
    else:
        category_counts = (
            df_filtrado_hist[categorical_filtradas]
            .sum()
            .sort_values(ascending=False)
        )
    
        st.subheader(f"Top {top_n_hist} tipos de restaurante{subtitulo_estado_hist}")
    
        colors = sns.color_palette("muted", top_n_hist)
        
        fig_hist, ax_hist = plt.subplots(figsize=(12, 6))
        ax_hist.bar(
            category_counts.head(top_n_hist).index,
            category_counts.head(top_n_hist).values,
            color=colors,
            edgecolor="black"
        )
        
        ax_hist.set_title(f"Top {top_n_hist} categorías")
        ax_hist.set_xlabel("Categoría")
        ax_hist.set_ylabel("Número de restaurantes")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
    
        st.pyplot(fig_hist)
    
        st.subheader("Tabla de recuentos (Top categorías)")
        st.dataframe(
            category_counts.head(top_n_hist).rename("count").to_frame()
        )
        
    st.markdown("## Ranking de categorías por rating promedio")

    if estado_rank == "Todos":
        df_filtrado_rank = df.copy()
    else:
        df_filtrado_rank = df[df["state"] == estado_rank].copy()
    
    subtitulo_estado_rank = (
        f" en {estado_rank}" if estado_rank != "Todos" else " en todos los estados"
    )
    st.write(
        f"Mostrando categorías con al menos **{min_restaurantes}** restaurantes"
        f"{subtitulo_estado_rank}."
    )
    
    if df_filtrado_rank.empty:
        st.warning("No hay restaurantes que coincidan con este filtro de estado (ranking).")
    else:
        category_ratings = {}
    
        for col in categorical_filtradas:
            mask = df_filtrado_rank[col] == 1
            count = mask.sum()
            if count >= min_restaurantes:
                category_ratings[col] = df_filtrado_rank.loc[mask, "stars"].mean()
    
        if not category_ratings:
            st.warning(
                f"No hay categorías con al menos {min_restaurantes} restaurantes en este estado."
            )
        else:
            category_ratings = (
                pd.Series(category_ratings)
                .sort_values(ascending=False)
            )
    
            category_ratings_top = category_ratings.head(top_n_rank)
    
            fig_rank, ax_rank = plt.subplots(figsize=(10, 6))
    
            palette = sns.color_palette("muted", n_colors=len(category_ratings_top))
    
            ax_rank.barh(
                category_ratings_top.index[::-1],
                category_ratings_top.values[::-1],
                color=palette,
                edgecolor="black"
            )
    
            titulo_estado_rank = (
                f" en {estado_rank}" if estado_rank != "Todos" else " (todos los estados)"
            )
            ax_rank.set_title(
                f"Top {len(category_ratings_top)} categorías por rating promedio{titulo_estado_rank}",
                fontsize=14
            )
            ax_rank.set_xlabel("Rating promedio", fontsize=12)
            plt.tight_layout()
    
            st.pyplot(fig_rank)
    
            st.subheader("Detalle numérico")
            st.dataframe(
                category_ratings_top.rename("rating_promedio").to_frame()
            )
