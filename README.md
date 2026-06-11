# SO-101 Intelligent Control — Cable Sorting with Imitation Learning

**Intelligent Control Module · Tecnológico de Monterrey · Equipo 6**

El robot SO-101 aprende a tomar un cable de color de una terminal y depositarlo en su caja correspondiente, en presencia de cables distractores (negro/blanco). Un sistema de visión computacional basado en OpenCV HSV detecta automáticamente el ambiente y selecciona la política ACT correcta sin intervención humana.

| Track | Tarea | Robot | Método |
|---|---|---|---|
| Imitation Learning — Behaviour Cloning | Option 2 — Laboratory Setup with Clip Wires | SO-101 Follower (6 DOF) | ACT — Action Chunking Transformer |

---

## Resultados

| Modelo | Tasa de Éxito | Tiempo Promedio |
|---|---|---|
| act_only_black | 80% | 18.98 s |
| act_only_white | 90% | 14.26 s |
| act_both_bw | 90% | 7.9 s |
| **Generalización (10 escenarios)** | **90%** | — |
| **Accuracy selector automático** | **100%** | — |

Todos los episodios completados en < 27 segundos ✅

---

## Videos de Demostración

| Modelo | Descripción | Video |
|---|---|---|
| act_only_black | Distractor negro presente | [YouTube ↗](https://youtu.be/7gXFCimDjyQ) |
| act_only_white | Distractor blanco presente | [YouTube ↗](https://youtu.be/EpvfbroREuE) |
| act_both_bw | Ambos distractores presentes | [YouTube ↗](https://youtu.be/U0JogTCIOnQ) |

---

## Dataset — HuggingFace

| Dataset | Episodios | Frames | FPS |
|---|---|---|---|
| [AdrielP/cables_il_only_black](https://huggingface.co/datasets/AdrielP/cables_il_only_black) | 101 | 76.3k | 30 |
| [AdrielP/cables_il_only_white](https://huggingface.co/datasets/AdrielP/cables_il_only_white) | 101 | 78.0k | 30 |
| [AdrielP/cables_il_both_bw](https://huggingface.co/datasets/AdrielP/cables_il_both_bw) | 101 | 30.2k | 10 |
| **TOTAL** | **303** | **184.5k** | — |

Cada episodio incluye imágenes RGB de 2 cámaras (front + side, 640×480), estados articulares (6 joints) y acciones del operador.

> `both_bw` grabado a 10 FPS — misma duración de tarea, menor densidad de frames. El modelo aprende movimientos más directos.

---

## Modelos — HuggingFace

| Modelo | Ambiente que detecta | Tarea ejecutada |
|---|---|---|
| [AdrielP/act_only_black](https://huggingface.co/AdrielP/act_only_black) | Solo cable negro visible | Toma cable amarillo → caja amarilla |
| [AdrielP/act_only_white](https://huggingface.co/AdrielP/act_only_white) | Solo cable blanco visible | Toma cable verde → caja verde |
| [AdrielP/act_both_bw](https://huggingface.co/AdrielP/act_both_bw) | Negro Y blanco visibles | Toma cable rojo → caja roja |

---

## Pipeline del Sistema
<img width="5367" height="1376" alt="_Diagrama de flujo -  Diagrama de flujo Flujo dual ACT y detección de color (1)" src="https://github.com/user-attachments/assets/eec3f453-f79e-433a-9b90-08fd419664f8" />

**Lógica del selector (OpenCV HSV):**
- Negro detectado (V < 40, > 4000 px) y Blanco detectado (V > 200, S < 25, > 600 px) → `act_both_bw`
- Solo negro → `act_only_black`
- Solo blanco → `act_only_white`

---

## Arquitectura — ACT (Action Chunking Transformer)
πθ(aₜ | oₜ) — Behaviour Cloning
Observación oₜ:

Imagen front camera  640×480 → ResNet18 → features
Imagen side camera   640×480 → ResNet18 → features
Joint states (6 DOF)

Arquitectura:

Backbone visual: ResNet18 (pesos ImageNet)
Encoder: 4 capas Transformer
Decoder: 1 capa Transformer
Attention heads: 8 · Dim model: 512
Chunk size: 100 acciones por inferencia
VAE latent dim: 32 · KL weight: 10.0

Entrenamiento:

Steps: 50,000 por modelo
Optimizer: AdamW · lr 1e-5 · weight decay 1e-4
Hardware: Google Colab GPU A100
Framework: LeRobot (HuggingFace)

Inferencia:

Hardware: CPU — WSL2 Ubuntu 22.04 (~10 Hz)


---

## Gráficas de Resultados

### Dataset
![Dataset](results/plots/graficas_dataset.png)

### Evaluación por Modelo
![Evaluación](results/plots/graficas_eval.png)

### Generalización y Selección Automática
![Generalización](results/plots/graficas_generalizacion.png)

---

## Instalación

### Requisitos
- Ubuntu 22.04 (o WSL2)
- Python 3.10+
- Robot SO-101 conectado por USB

```bash
git clone https://github.com/carloAdr1/so101-intelligent-control.git
cd so101-intelligent-control
python -m venv venv
source venv/bin/activate
pip install lerobot
```

### Configuración de hardware
/dev/ttyACM0  →  SO101 follower (robot)
/dev/ttyACM1  →  SO101 leader (teleop)
/dev/video0   →  cámara frontal
/dev/video2   →  cámara lateral

---

## Uso

### Selección automática de modelo (sistema completo)
```bash
python scripts/auto_select_model.py
```
Captura un frame de la cámara lateral, detecta el ambiente mediante HSV y lanza automáticamente el modelo correcto.

### Ejecutar un modelo manualmente
```bash
# only_black
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.cameras='{"front":{"type":"opencv","index_or_path":0,"width":640,"height":480,"fps":30},"side":{"type":"opencv","index_or_path":2,"width":640,"height":480,"fps":30}}' \
  --policy.path=AdrielP/act_only_black \
  --dataset.repo_id=AdrielP/eval_only_black \
  --dataset.single_task="state based cable sorting" \
  --dataset.num_episodes=5 \
  --dataset.fps=15 \
  --play_sounds=false
```
Sustituir `act_only_black` / `eval_only_black` por `act_only_white`, `act_both_bw` según el ambiente.

### Grabar nuevas demostraciones
```bash
bash scripts/record_il.sh both_bw 100
bash scripts/record_il.sh only_black 100
bash scripts/record_il.sh only_white 100
```

---

## Docker

```bash
# Build
docker build -t so101-intelligent-control .

# Run
docker run --rm -it \
  -v $(pwd)/results:/app/results \
  so101-intelligent-control
```

Para acceso al hardware (cámaras, robot):
```bash
docker run --rm -it \
  --privileged \
  --device=/dev/ttyACM0 \
  --device=/dev/ttyACM1 \
  --device=/dev/video0 \
  --device=/dev/video2 \
  -v $(pwd)/results:/app/results \
  so101-intelligent-control
```

---

## Protocolo de Evaluación

**Evaluación por modelo (30 episodios total):** 10 episodios × 3 modelos, posición fija del cable, solo cambia el distractor presente. Mide: éxito/fallo de la tarea.

**Evaluación de generalización (10 escenarios):** Combinación aleatoria de distractores. El sistema selecciona automáticamente el modelo. Mide: (1) accuracy del selector, (2) task success rate.

Ver métricas detalladas en [`results/metrics/`](results/metrics/).

---

## Limitaciones

- Inferencia en CPU (~10 Hz vs 30 Hz ideal) — el robot se mueve más lento que durante el entrenamiento
- Posición fija del cable durante entrenamiento — poca variabilidad de pose
- Detector HSV sensible a cambios de iluminación
- No generaliza a cables en posiciones no vistas durante entrenamiento

**Trabajo futuro:** mayor variabilidad de posición en el dataset, Diffusion Policy como alternativa a ACT, migrar inferencia a GPU, más condiciones de iluminación.

---

## Estructura del Repositorio
so101-intelligent-control/
├── calibration/          # Archivos de calibración SO101
├── docs/                 # Documentación técnica
│   ├── SETUP_WSL_USB.md
│   ├── CAMERA_TESTS.md
│   ├── TELEOPERATION.md
│   ├── CALIBRATION.md
│   └── DATASET_PLAN.md
├── models/               # Referencias a modelos HuggingFace
├── results/
│   ├── metrics/          # Archivos de métricas (CSV/JSON)
│   ├── plots/            # Gráficas generadas
│   │   ├── graficas_dataset.png
│   │   ├── graficas_eval.png
│   │   └── graficas_generalizacion.png
│   └── videos/
│       └── demo_links.md # Links a videos en YouTube
├── scripts/              # Scripts de grabación y utilidades
├── Dockerfile
├── requirements.txt
└── README.md

---

## Presentación

Presentación final del proyecto (Equipo 6): [Google Drive ↗](https://drive.google.com/drive/folders/1DEdYMGSX__oJ1wk36yFZZiM75tav75kf?usp=drive_link)

---

## Equipo 6 · Intelligent Control Module · Tecnológico de Monterrey
