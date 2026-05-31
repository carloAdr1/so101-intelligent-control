# Calibration Files

Archivos de calibracion del brazo SO101 usado en este proyecto.

IMPORTANTE: estos archivos son especificos al brazo fisico de este proyecto.
Si usas un brazo diferente, debes recalibrar con:
    bash scripts/calibrate.sh

## Usar esta calibracion

Copiar los archivos a la ruta esperada por lerobot:

```bash
mkdir -p ~/.cache/huggingface/lerobot/calibration/robots/so_follower
mkdir -p ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader

cp calibration/robots/so_follower.json ~/.cache/huggingface/lerobot/calibration/robots/so_follower/None.json
cp calibration/teleoperators/so_leader.json ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/None.json
```
