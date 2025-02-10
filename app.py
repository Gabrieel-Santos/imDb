import pandas as pd

# Lista de arquivos do Google Drive
urls = {
    "name.basics": "https://drive.google.com/uc?id=1WqfVGRwrgQVssX-c0gYgTJSOu1daqoYU",
    "title.akas": "https://drive.google.com/uc?id=1Y2dyx2IXE6meDOjxsRe2ADLGVmUjPYaM",
    "title.basics": "https://drive.google.com/uc?id=130l9jmHkSgqzBkyP_THjbpgBzc4Bcr3i",
    "title.crew": "https://drive.google.com/uc?id=1QJtP_Adw0yS5od76_hbyFH6fql0ySJvD",
    "title.episode": "https://drive.google.com/uc?id=1dHvZh1uAGV-KIXUTY-jdGM1zxkZLeva_",
    "title.principals": "https://drive.google.com/uc?id=1lh9ldNkF48n_5EGOHhsusFSU32Xw4poh",
    "title.ratings": "https://drive.google.com/uc?id=15bwv9vNWiBA74b9v4VSRrogR_1DuNyd1"
}

# Testar carregamento dos arquivos
for name, url in urls.items():
    try:
        print(f"Carregando {name}...")
        df = pd.read_csv(url, sep="\t", low_memory=False)  # TSV usa tabulação como separador
        print(df.head(), "\n")
    except Exception as e:
        print(f"Erro ao carregar {name}: {e}\n")
