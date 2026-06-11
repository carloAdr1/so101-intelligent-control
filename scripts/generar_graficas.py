"""
Genera todas las graficas de evaluacion del proyecto SO-101.
Guarda los resultados en results/plots/

Usage:
    python scripts/generar_graficas.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs("results/plots", exist_ok=True)

BG    = "#0F1117"
PANEL = "#1A1D27"
COLORES = {
    "only_black": "#2D6A9F",
    "only_white": "#E8A838",
    "both_bw":    "#3BAF74"
}
LABELS = {
    "only_black": "Solo Negro",
    "only_white": "Solo Blanco",
    "both_bw":    "Ambos (B&W)"
}

# ─────────────────────────────────────────────────────────────────────────────
# GRAFICA 1: Evaluacion de modelos ACT (10 episodios por modelo)
# ─────────────────────────────────────────────────────────────────────────────

modelos   = ["only_black", "only_white", "both_bw"]
etiquetas = [LABELS[m] for m in modelos]
cols      = [COLORES[m] for m in modelos]

success_rate = [80, 90, 90]
tiempo_promedio = [18.98, 14.26, 7.90]

tiempos = {
    "only_black": [20.39, 20.70, 18.16, 17.76, 18.26, 19.69, 18.59, 18.27],
    "only_white": [11.41, 11.43, 13.23, 14.18, 14.78, 16.19, 15.53, 16.07, 15.55],
    "both_bw":    [11.04,  7.02, 11.16,  9.39,  7.17,  7.32,  4.94,  6.79,  6.25],
}
episodios_raw = {
    "only_black": [True, True, True, False, True, True, False, True, True, True],
    "only_white": [True, True, False, True, True, True, True, True, True, True],
    "both_bw":    [True, True, True, True, True, True, True, True, False, True],
}

fig = plt.figure(figsize=(16, 12))
fig.patch.set_facecolor(BG)
fig.suptitle("Evaluacion de Modelos ACT — Cable Sorting (SO-101)",
             fontsize=16, fontweight="bold", color="white", y=0.98)

ax1 = fig.add_subplot(2, 3, 1)
ax1.set_facecolor(PANEL)
bars = ax1.bar(etiquetas, success_rate, color=cols, width=0.5,
               edgecolor="white", linewidth=0.4)
for bar, val in zip(bars, success_rate):
    ax1.text(bar.get_x() + bar.get_width()/2, val + 1.5,
             f"{val}%", ha="center", va="bottom",
             fontsize=13, fontweight="bold", color="white")
ax1.set_ylim(0, 110)
ax1.set_title("Tasa de Exito", color="white", fontsize=12, pad=8)
ax1.set_ylabel("% Exitos", color="white")
ax1.tick_params(colors="white")
ax1.spines[:].set_color("#444")
ax1.axhline(100, color="#555", linewidth=0.6, linestyle="--")

ax2 = fig.add_subplot(2, 3, 2)
ax2.set_facecolor(PANEL)
bars2 = ax2.bar(etiquetas, tiempo_promedio, color=cols, width=0.5,
                edgecolor="white", linewidth=0.4)
for bar, val in zip(bars2, tiempo_promedio):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.3,
             f"{val}s", ha="center", va="bottom",
             fontsize=13, fontweight="bold", color="white")
ax2.set_ylim(0, 25)
ax2.set_title("Tiempo Promedio de Tarea", color="white", fontsize=12, pad=8)
ax2.set_ylabel("Segundos", color="white")
ax2.tick_params(colors="white")
ax2.spines[:].set_color("#444")

ax3 = fig.add_subplot(2, 3, 3)
ax3.set_facecolor(PANEL)
bp = ax3.boxplot(
    [tiempos["only_black"], tiempos["only_white"], tiempos["both_bw"]],
    patch_artist=True, widths=0.4,
    medianprops=dict(color="white", linewidth=2),
    whiskerprops=dict(color="#AAA"),
    capprops=dict(color="#AAA"),
    flierprops=dict(markerfacecolor="#AAA", marker="o", markersize=4)
)
for patch, color in zip(bp["boxes"], cols):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
ax3.set_xticks([1, 2, 3])
ax3.set_xticklabels(etiquetas, color="white", fontsize=9)
ax3.set_title("Distribucion Tiempo de Tarea", color="white", fontsize=12, pad=8)
ax3.set_ylabel("Segundos", color="white")
ax3.tick_params(colors="white")
ax3.spines[:].set_color("#444")

for idx, modelo in enumerate(modelos):
    ax = fig.add_subplot(2, 3, 4 + idx)
    ax.set_facecolor(PANEL)
    eps = list(range(1, 11))
    resultados = episodios_raw[modelo]
    t_vals = tiempos[modelo]
    t_iter = iter(t_vals)
    for ep, ok in zip(eps, resultados):
        if ok:
            t = next(t_iter)
            ax.bar(ep, t, color=COLORES[modelo], alpha=0.75,
                   edgecolor="white", linewidth=0.3)
        else:
            ax.bar(ep, 0, color="#555", alpha=0.5)
            ax.text(ep, 0.5, "X", ha="center", va="bottom",
                    color="#FF5555", fontsize=11, fontweight="bold")
    ax.set_xlim(0.3, 10.7)
    ax.set_ylim(0, 28)
    ax.set_xticks(eps)
    ax.set_title(LABELS[modelo], color="white", fontsize=11, pad=8)
    ax.set_xlabel("Episodio", color="white", fontsize=9)
    ax.set_ylabel("Tiempo tarea (s)", color="white", fontsize=9)
    ax.tick_params(colors="white", labelsize=8)
    ax.spines[:].set_color("#444")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("results/plots/graficas_eval.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
plt.close()
print("Guardado: results/plots/graficas_eval.png")

# ─────────────────────────────────────────────────────────────────────────────
# GRAFICA 2: Generalizacion
# ─────────────────────────────────────────────────────────────────────────────

escenarios   = list(range(1, 11))
modelos_esc  = ["both_bw","both_bw","both_bw",
                "only_black","only_black","only_black",
                "only_white","only_white","only_white",
                "both_bw"]
exitosos_esc = [True,True,True, True,True,True, True,True,True, False]
tiempos_esc  = [10.18,11.68,11.14, 24.95,25.57,23.23, 16.15,17.75,17.28, None]

resumen_gen = {
    "both_bw":    {"n": 4, "exit": 3, "sr": 75.0,  "sel": 100.0, "t": 11.00},
    "only_black": {"n": 3, "exit": 3, "sr": 100.0, "sel": 100.0, "t": 24.58},
    "only_white": {"n": 3, "exit": 3, "sr": 100.0, "sel": 100.0, "t": 17.06},
}

fig2 = plt.figure(figsize=(18, 13))
fig2.patch.set_facecolor(BG)
fig2.suptitle("Evaluacion de Generalizacion — Seleccion Automatica de Modelo (SO-101)",
              fontsize=15, fontweight="bold", color="white", y=0.98)

ax1 = fig2.add_subplot(2, 3, 1)
ax1.set_facecolor(PANEL)
sr = [resumen_gen[m]["sr"] for m in modelos]
bars = ax1.bar(etiquetas, sr, color=cols, width=0.5,
               edgecolor="white", linewidth=0.4)
for bar, val in zip(bars, sr):
    ax1.text(bar.get_x()+bar.get_width()/2, val+1.5,
             f"{val}%", ha="center", fontsize=12, fontweight="bold", color="white")
ax1.set_ylim(0, 115)
ax1.set_title("Tasa de Exito por Modelo", color="white", fontsize=11, pad=8)
ax1.set_ylabel("% Exitos", color="white")
ax1.tick_params(colors="white")
ax1.spines[:].set_color("#444")
ax1.axhline(100, color="#555", linewidth=0.6, linestyle="--")

ax2 = fig2.add_subplot(2, 3, 2)
ax2.set_facecolor(PANEL)
sel = [resumen_gen[m]["sel"] for m in modelos]
bars2 = ax2.bar(etiquetas, sel, color=cols, width=0.5,
                edgecolor="white", linewidth=0.4)
for bar, val in zip(bars2, sel):
    ax2.text(bar.get_x()+bar.get_width()/2, val+1.5,
             f"{val}%", ha="center", fontsize=12, fontweight="bold", color="white")
ax2.set_ylim(0, 115)
ax2.set_title("Accuracy del Detector de Escena", color="white", fontsize=11, pad=8)
ax2.set_ylabel("% Seleccion Correcta", color="white")
ax2.tick_params(colors="white")
ax2.spines[:].set_color("#444")
ax2.axhline(100, color="#555", linewidth=0.6, linestyle="--")
ax2.text(1, 108, "100% en todos los modelos", ha="center",
         color="#AAA", fontsize=9, style="italic")

ax3 = fig2.add_subplot(2, 3, 3)
ax3.set_facecolor(PANEL)
ts = [resumen_gen[m]["t"] for m in modelos]
bars3 = ax3.bar(etiquetas, ts, color=cols, width=0.5,
                edgecolor="white", linewidth=0.4)
for bar, val in zip(bars3, ts):
    ax3.text(bar.get_x()+bar.get_width()/2, val+0.3,
             f"{val}s", ha="center", fontsize=12, fontweight="bold", color="white")
ax3.set_ylim(0, 32)
ax3.set_title("Tiempo Promedio de Tarea", color="white", fontsize=11, pad=8)
ax3.set_ylabel("Segundos", color="white")
ax3.tick_params(colors="white")
ax3.spines[:].set_color("#444")

ax4 = fig2.add_subplot(2, 3, 4)
ax4.set_facecolor(PANEL)
for i, (esc, modelo, ok) in enumerate(zip(escenarios, modelos_esc, exitosos_esc)):
    marker = "★" if ok else "✗"
    ax4.scatter(esc, 1, s=600, color=COLORES[modelo],
                edgecolors="white" if ok else "#FF5555",
                linewidths=1.5 if not ok else 0.5, zorder=3)
    ax4.text(esc, 1, marker, ha="center", va="center",
             fontsize=9, color="white" if ok else "#FF5555", fontweight="bold")
    ax4.text(esc, 0.7, LABELS[modelo][:4], ha="center",
             fontsize=6.5, color="#CCC")
patches = [mpatches.Patch(color=COLORES[m], label=LABELS[m]) for m in modelos]
ax4.legend(handles=patches, loc="upper right", fontsize=7,
           facecolor=PANEL, edgecolor="#444", labelcolor="white")
ax4.set_xlim(0.3, 10.7)
ax4.set_ylim(0.4, 1.3)
ax4.set_xticks(escenarios)
ax4.set_title("Timeline de Escenarios", color="white", fontsize=11, pad=8)
ax4.set_xlabel("Escenario", color="white")
ax4.set_yticks([])
ax4.tick_params(colors="white")
ax4.spines[:].set_color("#444")

ax5 = fig2.add_subplot(2, 3, 5)
ax5.set_facecolor(PANEL)
for esc, modelo, t, ok in zip(escenarios, modelos_esc, tiempos_esc, exitosos_esc):
    if t is not None:
        ax5.bar(esc, t, color=COLORES[modelo], alpha=0.8,
                edgecolor="white", linewidth=0.3)
    else:
        ax5.bar(esc, 0, color="#555")
        ax5.text(esc, 0.5, "✗", ha="center", color="#FF5555",
                 fontsize=11, fontweight="bold")
ax5.set_xlim(0.3, 10.7)
ax5.set_ylim(0, 32)
ax5.set_xticks(escenarios)
ax5.set_title("Tiempo de Tarea por Escenario", color="white", fontsize=11, pad=8)
ax5.set_xlabel("Escenario", color="white")
ax5.set_ylabel("Segundos", color="white")
ax5.tick_params(colors="white")
ax5.spines[:].set_color("#444")
patches2 = [mpatches.Patch(color=COLORES[m], label=LABELS[m]) for m in modelos]
ax5.legend(handles=patches2, fontsize=7, facecolor=PANEL,
           edgecolor="#444", labelcolor="white")

ax6 = fig2.add_subplot(2, 3, 6)
ax6.set_facecolor(PANEL)
ax6.axis("off")
ax6.set_title("Resumen Global", color="white", fontsize=11, pad=8)
metricas = [
    ("Escenarios totales",       "10"),
    ("Tareas exitosas",          "9 / 10  (90%)"),
    ("Seleccion correcta",       "10 / 10  (100%)"),
    ("", ""),
    ("both_bw  exito",           "3 / 4  (75%)"),
    ("both_bw  tiempo prom",     "11.0 s"),
    ("", ""),
    ("only_black exito",         "3 / 3  (100%)"),
    ("only_black tiempo prom",   "24.6 s"),
    ("", ""),
    ("only_white exito",         "3 / 3  (100%)"),
    ("only_white tiempo prom",   "17.1 s"),
]
y = 0.95
for label, val in metricas:
    if label == "":
        y -= 0.04
        continue
    ax6.text(0.02, y, label, transform=ax6.transAxes,
             color="#AAA", fontsize=9, va="top")
    ax6.text(0.98, y, val, transform=ax6.transAxes,
             color="white", fontsize=9, va="top", ha="right", fontweight="bold")
    y -= 0.08

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("results/plots/graficas_generalizacion.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
plt.close()
print("Guardado: results/plots/graficas_generalizacion.png")

# ─────────────────────────────────────────────────────────────────────────────
# GRAFICA 3: Dataset summary
# ─────────────────────────────────────────────────────────────────────────────

fig3, axes = plt.subplots(1, 3, figsize=(15, 5))
fig3.patch.set_facecolor(BG)
fig3.suptitle("Dataset de Demostraciones — SO-101 Cable Sorting",
              fontsize=14, fontweight="bold", color="white", y=1.02)

ax1 = axes[0]
ax1.set_facecolor(PANEL)
etiq_ds = ["Solo Negro\n(only_black)", "Solo Blanco\n(only_white)", "Ambos B&W\n(both_bw)"]
bars = ax1.bar(etiq_ds, [101, 101, 101], color=cols, width=0.5,
               edgecolor="white", linewidth=0.4)
for bar in bars:
    ax1.text(bar.get_x()+bar.get_width()/2, 101+0.5,
             "101", ha="center", fontsize=13, fontweight="bold", color="white")
ax1.set_ylim(0, 120)
ax1.set_title("Episodios por Clase", color="white", fontsize=11, pad=8)
ax1.set_ylabel("# Demostraciones", color="white")
ax1.tick_params(colors="white", labelsize=8)
ax1.spines[:].set_color("#444")
ax1.axhline(50, color="#666", linewidth=0.8, linestyle="--")
ax1.text(2.4, 51.5, "min recomendado", color="#888", fontsize=7)

ax2 = axes[1]
ax2.set_facecolor(PANEL)
frames = [76300, 78000, 30200]
bars2 = ax2.bar(etiq_ds, [f/1000 for f in frames], color=cols,
                width=0.5, edgecolor="white", linewidth=0.4)
for bar, f in zip(bars2, frames):
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
             f"{f/1000:.1f}k", ha="center", fontsize=12,
             fontweight="bold", color="white")
ax2.set_ylim(0, 95)
ax2.set_title("Frames Totales por Clase", color="white", fontsize=11, pad=8)
ax2.set_ylabel("Miles de frames", color="white")
ax2.tick_params(colors="white", labelsize=8)
ax2.spines[:].set_color("#444")

ax3 = axes[2]
ax3.set_facecolor(PANEL)
ax3.axis("off")
ax3.set_title("Resumen del Dataset", color="white", fontsize=11, pad=8)
headers = ["Dataset", "Episodios", "Frames", "FPS"]
rows = [
    ["only_black", "101", "76.3k", "30"],
    ["only_white", "101", "78.0k", "30"],
    ["both_bw",    "101", "30.2k", "30"],
    ["TOTAL",      "303", "184.5k", "—"],
]
col_x = [0.0, 0.42, 0.62, 0.82]
y = 0.88
for x, h in zip(col_x, headers):
    ax3.text(x, y, h, transform=ax3.transAxes,
             color="#AAA", fontsize=9, fontweight="bold", va="top")
y -= 0.08
ax3.plot([0, 1], [0.82, 0.82], color="#444", linewidth=0.6,
         transform=ax3.transAxes, clip_on=False)
for i, row in enumerate(rows):
    color_row = "white" if i < 3 else "#FFD700"
    modelo_key = modelos[i] if i < 3 else None
    for j, (x, val) in enumerate(zip(col_x, row)):
        c = COLORES.get(modelo_key, "#FFD700") if j == 0 else color_row
        ax3.text(x, y, val, transform=ax3.transAxes,
                 color=c, fontsize=9, va="top",
                 fontweight="bold" if i == 3 else "normal")
    y -= 0.13
    if i == 2:
        ax3.plot([0, 1], [y+0.06, y+0.06], color="#444", linewidth=0.6,
                 transform=ax3.transAxes, clip_on=False)
ax3.text(0.0, 0.08,
         "Tarea: Cable sorting con distractores\n"
         "Observacion: 2 camaras RGB + estado joints\n"
         "Politica: ACT (Action Chunking Transformer)",
         transform=ax3.transAxes,
         color="#888", fontsize=7.5, va="bottom", linespacing=1.6)

plt.tight_layout()
plt.savefig("results/plots/graficas_dataset.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
plt.close()
print("Guardado: results/plots/graficas_dataset.png")
print("\nTodas las graficas generadas en results/plots/")
