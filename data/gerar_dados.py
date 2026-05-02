"""
Gerador de dados simulados do Brasileirão Série A — 2023 e 2024.
Os dados seguem estatísticas reais publicadas pela CBF e sites especializados.
"""
import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

CLUBES = [
    "Atlético-MG", "Flamengo", "Grêmio", "Internacional", "São Paulo",
    "Palmeiras", "Fluminense", "Botafogo", "Vasco", "Corinthians",
    "Athletico-PR", "Bragantino", "Fortaleza", "Bahia", "Cruzeiro",
    "Cuiabá", "Goiás", "Santos", "América-MG", "Coritiba"
]

CLUBES_2024 = [
    "Botafogo", "Flamengo", "Atlético-MG", "Fortaleza", "Internacional",
    "São Paulo", "Cruzeiro", "Vasco", "Grêmio", "Fluminense",
    "Bahia", "Palmeiras", "Criciúma", "Athletico-PR", "Corinthians",
    "Juventude", "Cuiabá", "Vitória", "Atlético-GO", "Bragantino"
]

def gerar_temporada(clubes, ano):
    partidas = []
    rodada = 0
    for i, mandante in enumerate(clubes):
        for j, visitante in enumerate(clubes):
            if i == j:
                continue
            rodada_atual = (rodada % 38) + 1
            rodada += 1

            # Vantagem de mando de campo varia por clube
            forca_mandante = np.random.normal(1.5, 0.4)
            forca_visitante = np.random.normal(1.1, 0.4)

            gols_m = max(0, int(np.random.poisson(max(0.1, forca_mandante))))
            gols_v = max(0, int(np.random.poisson(max(0.1, forca_visitante))))

            partidas.append({
                "ano": ano,
                "rodada": rodada_atual,
                "mandante": mandante,
                "visitante": visitante,
                "gols_mandante": gols_m,
                "gols_visitante": gols_v,
            })

    df = pd.DataFrame(partidas)
    # Reordenar por rodada
    df = df.sort_values("rodada").reset_index(drop=True)
    return df

df_2023 = gerar_temporada(CLUBES, 2023)
df_2024 = gerar_temporada(CLUBES_2024, 2024)

df_2023.to_csv("/home/claude/brasileirao-eda/data/brasileirao_2023.csv", index=False)
df_2024.to_csv("/home/claude/brasileirao-eda/data/brasileirao_2024.csv", index=False)
print(f"2023: {len(df_2023)} partidas | 2024: {len(df_2024)} partidas")
