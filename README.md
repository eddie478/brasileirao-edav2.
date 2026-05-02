[README.md](https://github.com/user-attachments/files/27294183/README.md)
# ⚽ Análise Exploratória do Brasileirão Série A — 2023 vs 2024

Comparativo entre as temporadas 2023 e 2024 do Campeonato Brasileiro Série A, com foco em aproveitamento dos clubes, fator mando de campo, distribuição de gols e evolução da disputa pelo título.

---

## 📊 Análises Realizadas

| # | Análise | Descrição |
|---|---------|-----------|
| 1 | **Aproveitamento Geral** | Comparativo de % de pontos aproveitados por clube entre as duas temporadas |
| 2 | **Fator Mando de Campo** | Desempenho em casa vs fora para o top 10 de cada temporada |
| 3 | **Distribuição de Gols** | Total de gols por rodada ao longo do campeonato, com médias comparadas |
| 4 | **Heatmap de Confrontos Diretos** | Pontos obtidos em cada confronto direto entre os 12 melhores clubes (2024) |
| 5 | **Evolução Acumulada de Pontos** | Corrida pelo título rodada a rodada para o top 6 de cada temporada |

---

## 🗂️ Estrutura do Projeto

```
brasileirao-eda/
│
├── data/
│   ├── gerar_dados.py          # Script de geração dos dados simulados
│   ├── brasileirao_2023.csv    # Resultados de todas as partidas — 2023
│   └── brasileirao_2024.csv    # Resultados de todas as partidas — 2024
│
├── outputs/
│   ├── 01_aproveitamento_geral.png
│   ├── 02_mando_de_campo.png
│   ├── 03_gols_por_rodada.png
│   ├── 04_heatmap_confrontos.png
│   └── 05_evolucao_pontos.png
│
├── analise_brasileirao.py      # Script principal com todas as análises
└── README.md
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**
- **pandas** — manipulação e tratamento dos dados
- **matplotlib** — visualizações de linha, barras e séries temporais
- **seaborn** — heatmap de confrontos diretos
- **numpy** — cálculos estatísticos

---

## ▶️ Como Executar

```bash
# Clone o repositório
git clone https://github.com/eddie478/brasileirao-eda
cd brasileirao-eda

# Instale as dependências
pip install pandas matplotlib seaborn numpy

# Gere os dados
python data/gerar_dados.py

# Execute as análises
python analise_brasileirao.py
```

Os gráficos serão salvos automaticamente na pasta `outputs/`.

---

## 📌 Principais Achados

- Clubes com maior aproveitamento em casa tendem a ter desempenho consistentemente superior ao longo da temporada
- A distribuição de gols por rodada revela picos nas rodadas intermediárias, com quedas no final do campeonato
- O heatmap evidencia padrões claros de dominância nos confrontos diretos entre os clubes do G4
- A evolução acumulada de pontos mostra viradas significativas na disputa pelo título entre as rodadas 20 e 30

---

## 👤 Autor

**Clayton Liberatori Gomes**  
Estudante de Ciência Matemática — Ênfase em Análise de Dados | UFRJ  
[LinkedIn](https://linkedin.com/in/claytonlgomes) · [GitHub](https://github.com/eddie478)
