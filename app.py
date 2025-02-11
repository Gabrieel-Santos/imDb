import streamlit as st
import pandas as pd

# Dicionário com os links dos arquivos Parquet no Google Drive
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
        df = pd.read_parquet(url)
        st.write(df.head())  # Exibe as primeiras linhas do dataframe
    except Exception as e:
        st.error(f"Erro ao carregar {name}: {e}")
