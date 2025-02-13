import pandas as pd
import os

def load_parquet(file_path, columns=None):
    """Carrega um arquivo Parquet de forma otimizada, carregando apenas colunas necessárias."""
    return pd.read_parquet(file_path, columns=columns)

def save_parquet(df, file_path):
    """Salva um DataFrame como Parquet."""
    df.to_parquet(file_path, index=False)

def preprocess_imdb_data(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Caminhos dos arquivos
    files = {
        "title_basics": f"{input_dir}/title.basics.parquet",
        "title_ratings": f"{input_dir}/title.ratings.parquet",
        "title_akas": f"{input_dir}/title.akas.parquet",
        "title_crew": f"{input_dir}/title.crew.parquet",
        "title_episode": f"{input_dir}/title.episode.parquet",
        "title_principals": f"{input_dir}/title.principals.parquet",
        "name_basics": f"{input_dir}/name.basics.parquet"
    }

    # Carregar title.basics com as colunas 'tconst', 'titleType', 'startYear', 'genres', e 'primaryTitle'
    title_basics = load_parquet(files["title_basics"], columns=['tconst', 'primaryTitle', 'titleType', 'startYear', 'genres'])
    
    # Filtrar filmes dos últimos 50 anos e remover "short"
    current_year = 2025
    valid_start_year = current_year - 50  # 1975

    filtered_movies = title_basics[
        (title_basics['titleType'] == 'movie') & 
        (pd.to_numeric(title_basics['startYear'], errors='coerce').fillna(0) >= valid_start_year)
    ]

    # Manter apenas os títulos válidos
    valid_tconst = set(filtered_movies['tconst'])

    # Função para leitura e filtragem eficiente
    def filter_by_tconst(file_path, column="tconst", usecols=None):
        df = load_parquet(file_path, columns=usecols)
        return df[df[column].isin(valid_tconst)]

    title_ratings = filter_by_tconst(files["title_ratings"], usecols=['tconst', 'averageRating', 'numVotes'])
    title_akas = filter_by_tconst(files["title_akas"], column="titleId", usecols=['titleId', 'title', 'region', 'language'])
    title_crew = filter_by_tconst(files["title_crew"], usecols=['tconst', 'directors', 'writers'])
    title_episode = filter_by_tconst(files["title_episode"], usecols=['tconst', 'parentTconst', 'seasonNumber', 'episodeNumber'])
    title_principals = filter_by_tconst(files["title_principals"], usecols=['tconst', 'nconst', 'category'])

    # Manter apenas pessoas que participaram dos filmes filtrados
    valid_nconst = set(title_principals['nconst'])
    name_basics = load_parquet(files["name_basics"], columns=['nconst', 'primaryName', 'primaryProfession'])
    name_basics = name_basics[name_basics['nconst'].isin(valid_nconst)]

    # Salvar arquivos processados
    save_parquet(filtered_movies, f"{output_dir}/title.basics.parquet")
    save_parquet(title_ratings, f"{output_dir}/title.ratings.parquet")
    save_parquet(title_akas, f"{output_dir}/title.akas.parquet")
    save_parquet(title_crew, f"{output_dir}/title.crew.parquet")
    save_parquet(title_episode, f"{output_dir}/title.episode.parquet")
    save_parquet(title_principals, f"{output_dir}/title.principals.parquet")
    save_parquet(name_basics, f"{output_dir}/name.basics.parquet")

    print(f"Processamento concluído. Arquivos salvos em: {output_dir}")

# Exemplo de uso
if __name__ == "__main__":
    input_directory = "."  # Pasta onde os arquivos originais estão
    output_directory = "./imdb_processed"  # Pasta onde os arquivos filtrados serão salvos
    preprocess_imdb_data(input_directory, output_directory)
