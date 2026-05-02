"""
Análise Exploratória do Brasileirão Série A — 2023 vs 2024
=============================================================
Análises:
  1. Aproveitamento geral por clube (comparativo entre temporadas)
  2. Fator mando de campo (% pontos em casa vs fora)
  3. Distribuição de gols por rodada
  4. Heatmap de confrontos diretos
  5. Evolução acumulada de pontos ao longo do campeonato
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Configuração visual ──────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "figure.dpi": 130,
})
COR_2023 = "#1A5276"
COR_2024 = "#D4AC0D"
CINZA    = "#7F8C8D"

# ── Carrega dados ────────────────────────────────────────────────────────────
df23 = pd.read_csv("data/brasileirao_2023.csv")
df24 = pd.read_csv("data/brasileirao_2024.csv")

# ── Função auxiliar: calcula tabela de classificação ────────────────────────
def calcular_tabela(df):
    clubes = pd.unique(df[["mandante", "visitante"]].values.ravel())
    registros = []
    for clube in clubes:
        casa = df[df["mandante"] == clube]
        fora = df[df["visitante"] == clube]

        v_casa  = (casa["gols_mandante"] > casa["gols_visitante"]).sum()
        e_casa  = (casa["gols_mandante"] == casa["gols_visitante"]).sum()
        d_casa  = (casa["gols_mandante"] < casa["gols_visitante"]).sum()

        v_fora  = (fora["gols_visitante"] > fora["gols_mandante"]).sum()
        e_fora  = (fora["gols_visitante"] == fora["gols_mandante"]).sum()
        d_fora  = (fora["gols_visitante"] < fora["gols_mandante"]).sum()

        jogos   = len(casa) + len(fora)
        vit     = v_casa + v_fora
        emp     = e_casa + e_fora
        der     = d_casa + d_fora
        pts     = vit * 3 + emp
        gp      = casa["gols_mandante"].sum() + fora["gols_visitante"].sum()
        gc      = casa["gols_visitante"].sum() + fora["gols_mandante"].sum()

        pts_casa = v_casa * 3 + e_casa
        pts_fora = v_fora * 3 + e_fora
        jogos_casa = len(casa)
        jogos_fora = len(fora)

        registros.append({
            "clube": clube, "jogos": jogos, "vitorias": vit, "empates": emp,
            "derrotas": der, "pontos": pts, "gols_pro": gp, "gols_contra": gc,
            "saldo": gp - gc,
            "aproveitamento": round(pts / (jogos * 3) * 100, 1),
            "pts_casa": pts_casa, "jogos_casa": jogos_casa,
            "pts_fora": pts_fora, "jogos_fora": jogos_fora,
            "aprov_casa": round(pts_casa / (jogos_casa * 3) * 100, 1) if jogos_casa else 0,
            "aprov_fora": round(pts_fora / (jogos_fora * 3) * 100, 1) if jogos_fora else 0,
        })
    return pd.DataFrame(registros).sort_values("pontos", ascending=False).reset_index(drop=True)

tab23 = calcular_tabela(df23)
tab24 = calcular_tabela(df24)

# ════════════════════════════════════════════════════════════════════════════
# ANÁLISE 1 — Aproveitamento geral: Top 10 de cada temporada
# ════════════════════════════════════════════════════════════════════════════
clubes_comuns = set(tab23["clube"]) & set(tab24["clube"])
t23c = tab23[tab23["clube"].isin(clubes_comuns)].set_index("clube")["aproveitamento"]
t24c = tab24[tab24["clube"].isin(clubes_comuns)].set_index("clube")["aproveitamento"]

top_clubes = t24c.sort_values(ascending=False).head(12).index.tolist()
df_comp = pd.DataFrame({"2023": t23c[top_clubes], "2024": t24c[top_clubes]}).sort_values("2024", ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
y = np.arange(len(df_comp))
bars23 = ax.barh(y - 0.2, df_comp["2023"], height=0.38, color=COR_2023, label="2023", alpha=0.9)
bars24 = ax.barh(y + 0.2, df_comp["2024"], height=0.38, color=COR_2024, label="2024", alpha=0.9)
ax.set_yticks(y)
ax.set_yticklabels(df_comp.index, fontsize=11)
ax.set_xlabel("Aproveitamento (%)", fontsize=11)
ax.set_title("Aproveitamento Geral — Top 12 Clubes (2023 vs 2024)", fontsize=13, fontweight="bold", pad=14)
ax.legend(fontsize=11)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
for bar in bars23:
    ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height()/2,
            f"{bar.get_width():.0f}%", va="center", fontsize=8.5, color=COR_2023)
for bar in bars24:
    ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height()/2,
            f"{bar.get_width():.0f}%", va="center", fontsize=8.5, color="#8B6914")
plt.tight_layout()
plt.savefig("outputs/01_aproveitamento_geral.png", bbox_inches="tight")
plt.close()
print("✓ Análise 1 — Aproveitamento geral salva")

# ════════════════════════════════════════════════════════════════════════════
# ANÁLISE 2 — Fator mando de campo
# ════════════════════════════════════════════════════════════════════════════
top10_24 = tab24.head(10)["clube"].tolist()

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), sharey=False)
for ax, (ano, tabela, cor) in zip(axes, [("2023", tab23, COR_2023), ("2024", tab24, COR_2024)]):
    top = tabela[tabela["clube"].isin(top10_24 if ano == "2024" else tab23.head(10)["clube"].tolist())].copy()
    top = top.sort_values("aprov_casa", ascending=True)
    y = np.arange(len(top))
    ax.barh(y - 0.2, top["aprov_casa"],  height=0.38, color=cor,  label="Casa",  alpha=0.9)
    ax.barh(y + 0.2, top["aprov_fora"],  height=0.38, color=CINZA, label="Fora",  alpha=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(top["clube"], fontsize=10)
    ax.set_title(f"Mando de Campo — {ano}", fontsize=12, fontweight="bold")
    ax.set_xlabel("Aproveitamento (%)")
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
    ax.legend(fontsize=10)
fig.suptitle("Fator Mando de Campo: Desempenho em Casa vs Fora", fontsize=13, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("outputs/02_mando_de_campo.png", bbox_inches="tight")
plt.close()
print("✓ Análise 2 — Mando de campo salva")

# ════════════════════════════════════════════════════════════════════════════
# ANÁLISE 3 — Distribuição de gols por rodada
# ════════════════════════════════════════════════════════════════════════════
for df in [df23, df24]:
    df["total_gols"] = df["gols_mandante"] + df["gols_visitante"]

gols_rod23 = df23.groupby("rodada")["total_gols"].sum().reset_index()
gols_rod24 = df24.groupby("rodada")["total_gols"].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(gols_rod23["rodada"], gols_rod23["total_gols"], color=COR_2023, lw=2, label="2023", alpha=0.9)
ax.plot(gols_rod24["rodada"], gols_rod24["total_gols"], color=COR_2024, lw=2, label="2024", alpha=0.9)
media23 = gols_rod23["total_gols"].mean()
media24 = gols_rod24["total_gols"].mean()
ax.axhline(media23, color=COR_2023, lw=1, ls="--", alpha=0.6)
ax.axhline(media24, color=COR_2024, lw=1, ls="--", alpha=0.6)
ax.text(39.2, media23 + 0.2, f"Média\n{media23:.1f}", color=COR_2023, fontsize=9)
ax.text(39.2, media24 - 1.2, f"Média\n{media24:.1f}", color="#8B6914", fontsize=9)
ax.set_xlabel("Rodada", fontsize=11)
ax.set_ylabel("Total de Gols", fontsize=11)
ax.set_title("Distribuição de Gols por Rodada — 2023 vs 2024", fontsize=13, fontweight="bold", pad=14)
ax.legend(fontsize=11)
ax.set_xlim(1, 42)
plt.tight_layout()
plt.savefig("outputs/03_gols_por_rodada.png", bbox_inches="tight")
plt.close()
print("✓ Análise 3 — Distribuição de gols salva")

# ════════════════════════════════════════════════════════════════════════════
# ANÁLISE 4 — Heatmap de confrontos diretos (2024)
# ════════════════════════════════════════════════════════════════════════════
top12 = tab24.head(12)["clube"].tolist()
df24_top = df24[df24["mandante"].isin(top12) & df24["visitante"].isin(top12)].copy()

def resultado_mandante(row):
    if row["gols_mandante"] > row["gols_visitante"]:   return 3
    elif row["gols_mandante"] == row["gols_visitante"]: return 1
    else:                                                return 0

df24_top["pts_mandante"] = df24_top.apply(resultado_mandante, axis=1)
pivot = df24_top.pivot_table(index="mandante", columns="visitante", values="pts_mandante", aggfunc="sum")
pivot = pivot.reindex(index=top12, columns=top12)

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.eye(len(top12), dtype=bool)
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", linewidths=0.5,
            linecolor="#dddddd", mask=mask, ax=ax,
            cbar_kws={"label": "Pontos obtidos pelo mandante"},
            annot_kws={"size": 10})
ax.set_title("Heatmap de Confrontos Diretos — Brasileirão 2024\n(pontos obtidos pelo mandante)", fontsize=12, fontweight="bold", pad=14)
ax.set_xlabel("Visitante", fontsize=11)
ax.set_ylabel("Mandante", fontsize=11)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", rotation=0)
plt.tight_layout()
plt.savefig("outputs/04_heatmap_confrontos.png", bbox_inches="tight")
plt.close()
print("✓ Análise 4 — Heatmap de confrontos salva")

# ════════════════════════════════════════════════════════════════════════════
# ANÁLISE 5 — Evolução acumulada de pontos (top 6 do 2024)
# ════════════════════════════════════════════════════════════════════════════
top6 = tab24.head(6)["clube"].tolist()
cores_top6 = ["#1A5276","#D4AC0D","#1E8449","#922B21","#6C3483","#1A535C"]

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

for ax, (ano, df, tabela) in zip(axes, [("2023", df23, tab23), ("2024", df24, tab24)]):
    top6_ano = tabela.head(6)["clube"].tolist()
    for idx, clube in enumerate(top6_ano):
        pts_acum = []
        total = 0
        for rod in sorted(df["rodada"].unique()):
            rodada_df = df[df["rodada"] == rod]
            casa = rodada_df[rodada_df["mandante"] == clube]
            fora = rodada_df[rodada_df["visitante"] == clube]
            if not casa.empty:
                g = casa.iloc[0]
                total += 3 if g["gols_mandante"] > g["gols_visitante"] else (1 if g["gols_mandante"] == g["gols_visitante"] else 0)
            if not fora.empty:
                g = fora.iloc[0]
                total += 3 if g["gols_visitante"] > g["gols_mandante"] else (1 if g["gols_visitante"] == g["gols_mandante"] else 0)
            pts_acum.append(total)
        rodadas = sorted(df["rodada"].unique())
        ax.plot(rodadas[:len(pts_acum)], pts_acum, color=cores_top6[idx], lw=2, label=clube)
        ax.text(rodadas[len(pts_acum)-1] + 0.3, pts_acum[-1], clube, fontsize=8, color=cores_top6[idx], va="center")
    ax.set_title(f"Evolução de Pontos — {ano}", fontsize=12, fontweight="bold")
    ax.set_xlabel("Rodada")
    ax.set_ylabel("Pontos acumulados")
    ax.set_xlim(1, max(df["rodada"]) + 7)
    ax.legend(fontsize=8, loc="upper left")

fig.suptitle("Evolução Acumulada de Pontos — Top 6 por Temporada", fontsize=13, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("outputs/05_evolucao_pontos.png", bbox_inches="tight")
plt.close()
print("✓ Análise 5 — Evolução acumulada salva")

print("\n✅ Todas as análises concluídas! Imagens salvas em outputs/")
