import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados processados
@st.cache_data
def load_data():
    title_basics = pd.read_parquet("title.basics.parquet")
    title_ratings = pd.read_parquet("title.ratings.parquet")
    title_akas = pd.read_parquet("title.akas.parquet")
    title_crew = pd.read_parquet("title.crew.parquet")
    title_principals = pd.read_parquet("title.principals.parquet")
    
    # Merge ratings com title_basics
    movies = title_basics.merge(title_ratings, on="tconst", how="left")
    return movies, title_akas, title_crew, title_principals

movies, title_akas, title_crew, title_principals = load_data()

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
st.subheader("🎬 Filmes Filtrados")
st.dataframe(filtered_movies[['primaryTitle', 'startYear', 'averageRating', 'numVotes', 'genres']].sort_values(by='averageRating', ascending=False))

# Gráfico - Distribuição de notas
st.subheader("📊 Distribuição de Notas dos Filmes")
fig = px.histogram(filtered_movies, x="averageRating", nbins=20, title="Distribuição das Notas no IMDb")
st.plotly_chart(fig)

# Gráfico - Relação entre votos e notas
st.subheader("📈 Relação entre Número de Votos e Nota Média")
fig = px.scatter(filtered_movies, x="numVotes", y="averageRating", title="Número de Votos vs. Nota Média", log_x=True)
st.plotly_chart(fig)

# Gráfico - Evolução das notas por ano
st.subheader("📅 Evolução da Nota Média dos Filmes ao Longo dos Anos")
ratings_per_year = filtered_movies.groupby("startYear")["averageRating"].mean().reset_index()
fig = px.line(ratings_per_year, x="startYear", y="averageRating", title="Média das Notas por Ano")
st.plotly_chart(fig)

# Top 10 filmes mais votados
st.subheader("🏆 Top 10 Filmes Mais Votados")
top_movies = filtered_movies.sort_values(by="numVotes", ascending=False).head(10)
st.table(top_movies[['primaryTitle', 'startYear', 'averageRating', 'numVotes']])

