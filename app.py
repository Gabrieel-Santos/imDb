import streamlit as st
import pandas as pd

# Links corrigidos
data_links = {
    "name.basics": "https://drive.google.com/uc?id=1gvQjMsZ7MWTnQf0Ryb1XuuChozExuoxF",
    "title.akas": "https://drive.google.com/uc?id=1LYpCjFMoPEasJkm6HPG2_oxYh7RpI_pN",
    "title.basics": "https://drive.google.com/uc?id=1uarqLz06y_YHmW7bNsPCV48s6fUtJ0q4",
    "title.crew": "https://drive.google.com/uc?id=1B9_r_RCk0JhfZ_kuIMHb9IB60DsFHeTn",
    "title.episode": "https://drive.google.com/uc?id=1rVmHqWGjRP3aixYlzAHii-tQfp-iryPn",
    "title.principals": "https://drive.google.com/uc?id=1r7j30kOT-i5QdXndsqDYQ0oJAE2y3T13",
    "title.ratings": "https://drive.google.com/uc?id=1-SRjvgnx9HcFO5kFA4bxxiMnmGQJXO8N"
}

st.title("Visualização dos Arquivos IMDb")

for name, url in data_links.items():
    st.subheader(f"🔍 {name}")
    
    try:
        # Carrega apenas as primeiras 1000 linhas para evitar estouro de memória
        df = pd.read_parquet(url, engine="pyarrow")  
        
        # Exibe a forma do DataFrame
        st.write(f"Tamanho do DataFrame: {df.shape}")
        
        # Exibe as primeiras 5 linhas
        st.write(df.head())  

    except Exception as e:
        st.error(f"Erro ao carregar {name}: {e}")
