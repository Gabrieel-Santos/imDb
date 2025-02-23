import streamlit as st
import pandas as pd
import plotly.express as px

# URLs diretas dos arquivos no Google Drive
file_urls = {
    "title_basics": "https://drive.google.com/uc?id=17w3uW_R-qJfBrUf1FlW8tA7dqnmK9gsG",
    "title_ratings": "https://drive.google.com/uc?id=1yT6P4dHwqQ_D_7KHY8IXgdS0r1FqJy-L",
    "title_akas": "https://drive.google.com/uc?id=1IwDE1-KK_35bejhRjVduw597fWTukM8Z",
    "title_crew": "https://drive.google.com/uc?id=1e4iv67CsY3i2LV7Br5q0hTDda2OmgMj4",
    "title_principals": "https://drive.google.com/uc?id=1wDR3Pkk-EHqpIe641BRyrJ8iGthbpt-F"
}

# Carregar dados processados com cache para evitar múltiplos downloads
@st.cache_data(ttl=600)
def load_data():
    try:
        title_basics = pd.read_parquet(file_urls["title_basics"])
        title_ratings = pd.read_parquet(file_urls["title_ratings"])
    except Exception as e:
        st.error(f"Erro ao carregar os arquivos: {e}")
        return None, None
    
    # Merge ratings com title_basics
    movies = title_basics.merge(title_ratings, on="tconst", how="left")
    return movies

movies = load_data()

if movies is not None:
    # Sidebar - Filtros
    st.sidebar.header("Filtros Dinâmicos")
    selected_year = st.sidebar.slider("Ano de Lançamento", 1975, 2025, (2000, 2025))
    selected_rating = st.sidebar.slider("Nota mínima no IMDb", 0.0, 10.0, 5.0)
    selected_votes = st.sidebar.slider("Número mínimo de votos", 0, 500000, 1000)
    selected_genres = st.sidebar.text_input("Filtrar por Gênero (ex: Action, Drama)")

    # Aplicar filtros
    filtered_movies = movies[
        (movies['startYear'].astype(float).between(*selected_year)) &
        (movies['averageRating'].astype(float) >= selected_rating) &
        (movies['numVotes'].astype(float) >= selected_votes)
    ]
    
    if selected_genres:
        filtered_movies = filtered_movies[filtered_movies['genres'].str.contains(selected_genres, na=False, case=False)]
    
    # Exibir tabela de filmes filtrados
    st.subheader("Filmes Filtrados")
    st.dataframe(filtered_movies[['primaryTitle', 'startYear', 'averageRating', 'numVotes', 'genres']].sort_values(by='averageRating', ascending=False))

    # Gráfico - Distribuição de notas
    st.subheader("Distribuição de Notas dos Filmes")
    fig = px.histogram(filtered_movies, x="averageRating", nbins=20, title="Distribuição das Notas no IMDb")
    st.plotly_chart(fig)

    # Gráfico - Relação entre votos e notas
    st.subheader("Relação entre Número de Votos e Nota Média")
    fig = px.scatter(filtered_movies, x="numVotes", y="averageRating", title="Número de Votos vs. Nota Média", log_x=True)
    st.plotly_chart(fig)

    # Gráfico - Evolução das notas por ano
    st.subheader("Evolução da Nota Média dos Filmes ao Longo dos Anos")
    ratings_per_year = filtered_movies.groupby("startYear")["averageRating"].mean().reset_index()
    fig = px.line(ratings_per_year, x="startYear", y="averageRating", title="Média das Notas por Ano")
    st.plotly_chart(fig)

    # Top 10 filmes mais votados
    st.subheader("Top 10 Filmes Mais Votados")
    top_movies = filtered_movies.sort_values(by="numVotes", ascending=False).head(10)
    st.table(top_movies[['primaryTitle', 'startYear', 'averageRating', 'numVotes']])
else:
    st.error("Falha ao carregar os dados. Verifique sua conexão e tente novamente.")
