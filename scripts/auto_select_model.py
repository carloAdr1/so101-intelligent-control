"""
Automatic scene detection and model selection for SO-101 cable sorting.

Captures a frame from the lateral camera, detects black/white cables via
OpenCV HSV thresholding, and automatically launches the correct ACT policy
using lerobot-record. Saves results to Excel with checkpoint support.

Usage:
    python scripts/auto_select_model.py
"""
import cv2
import numpy as np
import subprocess
import time
import re
import threading
import sys
import json
import tempfile
import pandas as pd
import os
import shutil
from datetime import datetime

NUM_ESCENARIOS  = 10
ROBOT_PORT      = "/dev/ttyACM1"
CAMERAS         = '{"front":{"type":"opencv","index_or_path":0,"width":640,"height":480,"fps":30},"side":{"type":"opencv","index_or_path":2,"width":640,"height":480,"fps":30}}'
CHECKPOINT_FILE = "./results/metrics/checkpoint_generalisation.json"

ROI            = (0, 270, 220, 450)
UMBRAL_NEGRO   = 5700
UMBRAL_BLANCO  = 700

MODELOS = {
    "only_black": "AdrielP/act_only_black",
    "only_white": "AdrielP/act_only_white",
    "both_bw":    "AdrielP/act_both_bw",
}

def capturar_frame():
    cap = cv2.VideoCapture(2)
    time.sleep(1)
    for _ in range(10):
        cap.read()
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("ERROR: No se pudo leer la camara lateral")
        sys.exit(1)
    return frame

def detectar_situacion():
    print("  Analizando escena con camara lateral...")
    frame = capturar_frame()

    x1, y1, x2, y2 = ROI
    roi = frame[y1:y2, x1:x2]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    mask_negro  = cv2.inRange(hsv, np.array([0,   0,   0]),   np.array([180, 255,  40]))
    mask_blanco = cv2.inRange(hsv, np.array([0,   0, 200]),   np.array([180,  25, 255]))

    px_negro  = cv2.countNonZero(mask_negro)
    px_blanco = cv2.countNonZero(mask_blanco)

    print("  Negro=" + str(px_negro) + "px, Blanco=" + str(px_blanco) + "px")

    hay_negro  = px_negro  > UMBRAL_NEGRO
    hay_blanco = px_blanco > UMBRAL_BLANCO

    if hay_negro and hay_blanco:
        situacion = "both_bw"
    elif hay_blanco:
        situacion = "only_white"
    elif hay_negro:
        situacion = "only_black"
    else:
        print("  AVISO: no se detecto cable. Selecciona manualmente.")
        situacion = seleccion_manual()

    print("  -> " + situacion)
    confirmar = input("  Confirmar? (ENTER=si / escribe otro: only_black / only_white / both_bw): ").strip()
    if confirmar in MODELOS:
        situacion = confirmar
        print("  Corregido a: " + situacion)

    return situacion

def seleccion_manual():
    while True:
        r = input("  Escribe el modelo (only_black / only_white / both_bw): ").strip()
        if r in MODELOS:
            return r
        print("  Opcion invalida.")

def cargar_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            data = json.load(f)
        print("Checkpoint encontrado: " + str(len(data["resultados"])) + " escenarios registrados.")
        r = input("Continuar desde escenario " + str(data["proximo_escenario"]) + "? (s/n): ").strip().lower()
        if r == "s":
            return data["resultados"], data["proximo_escenario"]
        print("Empezando desde cero.")
        os.remove(CHECKPOINT_FILE)
    return [], 1

def guardar_checkpoint(resultados, proximo_escenario):
    os.makedirs(os.path.dirname(CHECKPOINT_FILE), exist_ok=True)
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"resultados": resultados, "proximo_escenario": proximo_escenario}, f, indent=2)

def esperar_tecla_completado():
    resultado = {"tiempo": None}
    def _escuchar():
        print("  >> Robot corriendo... presiona ENTER cuando complete la tarea <<")
        sys.stdin.readline()
        resultado["tiempo"] = datetime.now()
    threading.Thread(target=_escuchar, daemon=True).start()
    return resultado

resultados, escenario_inicio = cargar_checkpoint()

print("\n" + "="*55)
print("EVALUACION DE GENERALIZACION - " + str(NUM_ESCENARIOS) + " ESCENARIOS")
print("="*55)

for escenario in range(escenario_inicio, NUM_ESCENARIOS + 1):
    print("\n" + "-"*55)
    print("ESCENARIO " + str(escenario) + "/" + str(NUM_ESCENARIOS))
    print("-"*55)
    input("Acomoda los cables y presiona ENTER para detectar...")

    situacion    = detectar_situacion()
    modelo       = MODELOS[situacion]
    dataset_root = "./data/eval_gen_esc" + str(escenario) + "_" + situacion

    if os.path.exists(dataset_root):
        shutil.rmtree(dataset_root)

    print("  Lanzando: " + modelo)

    cmd = [
        "lerobot-record",
        "--robot.type=so101_follower",
        "--robot.port=" + ROBOT_PORT,
        "--robot.cameras=" + CAMERAS,
        "--policy.path=" + modelo,
        "--dataset.repo_id=AdrielP/eval_gen_" + situacion,
        "--dataset.root=" + dataset_root,
        "--dataset.single_task=state based cable sorting",
        "--dataset.num_episodes=1",
        "--dataset.episode_time_s=30",
        "--dataset.reset_time_s=10",
        "--dataset.fps=15",
        "--dataset.push_to_hub=false",
        "--play_sounds=false"
    ]

    error_cmd      = None
    tiempo_robot_s = None
    tiempo_tarea_s = None
    resultado_tecla = esperar_tecla_completado()

    log_file = tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False, prefix="lerobot_")
    log_path = log_file.name
    log_file.close()

    try:
        with open(log_path, "w") as lf:
            subprocess.run(cmd, timeout=300, stderr=lf)
        with open(log_path, "r") as lf:
            log = lf.read()

        pat_inicio = r"INFO (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*Recording episode"
        pat_fin    = r"INFO (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*Stop recording"
        fmt        = "%Y-%m-%d %H:%M:%S"
        m_ini = re.search(pat_inicio, log)
        m_fin = re.search(pat_fin,    log)

        if m_ini and m_fin:
            t_ini = datetime.strptime(m_ini.group(1), fmt)
            t_fin = datetime.strptime(m_fin.group(1), fmt)
            tiempo_robot_s = round((t_fin - t_ini).total_seconds(), 2)
            print("  Tiempo total: " + str(tiempo_robot_s) + "s")
            if resultado_tecla["tiempo"] is not None:
                tiempo_tarea_s = round((resultado_tecla["tiempo"] - t_ini).total_seconds(), 2)
                tiempo_tarea_s = max(0.0, min(tiempo_tarea_s, tiempo_robot_s))
                print("  Tiempo hasta completar: " + str(tiempo_tarea_s) + "s")
        else:
            print("  AVISO: no se pudo parsear el log")

    except subprocess.TimeoutExpired:
        error_cmd = "timeout"
        print("  ADVERTENCIA: timeout excedido.")
    except Exception as e:
        error_cmd = str(e)
        print("  Error: " + str(e))
    finally:
        if os.path.exists(log_path):
            os.remove(log_path)

    while True:
        r = input("Modelo seleccionado correcto? (s/n): ").strip().lower()
        if r in ["s", "n"]:
            break
    seleccion_correcta = r == "s"

    while True:
        r = input("Tarea exitosa? (s/n): ").strip().lower()
        if r in ["s", "n"]:
            break
    exitoso = r == "s"

    resultados.append({
        "escenario":           escenario,
        "modelo_seleccionado": situacion,
        "seleccion_correcta":  seleccion_correcta,
        "exitoso":             exitoso,
        "tiempo_tarea_s":      tiempo_tarea_s,
        "tiempo_total_s":      tiempo_robot_s,
        "error":               error_cmd or "",
        "timestamp":           datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    print(("EXITO" if exitoso else "FALLO") +
          (" | seleccion OK" if seleccion_correcta else " | seleccion INCORRECTA"))
    guardar_checkpoint(resultados, escenario + 1)

    if escenario < NUM_ESCENARIOS:
        input("Prepara siguiente escenario y presiona ENTER...")

df       = pd.DataFrame(resultados)
total    = len(df)
exitosos = int(df["exitoso"].sum())
sel_ok   = int(df["seleccion_correcta"].sum())

print("\n" + "="*55)
print("RESULTADOS FINALES")
print("="*55)
print("Escenarios: " + str(total))
print("Exitosos:   " + str(exitosos) + "/" + str(total) + " (" + str(round(exitosos/total*100, 1)) + "%)")
print("Seleccion correcta: " + str(sel_ok) + "/" + str(total) + " (" + str(round(sel_ok/total*100, 1)) + "%)")

resumen = df.groupby("modelo_seleccionado").agg(
    escenarios   =("exitoso",            "count"),
    exitosos     =("exitoso",            "sum"),
    success_rate =("exitoso",            lambda x: round(x.mean() * 100, 1)),
    sel_correcta =("seleccion_correcta", lambda x: round(x.mean() * 100, 1)),
    t_tarea_prom =("tiempo_tarea_s",     lambda x: round(x.dropna().mean(), 2) if x.notna().any() else None),
    t_total_prom =("tiempo_total_s",     lambda x: round(x.mean(), 2))
).reset_index()

print("\nPor modelo:")
print(resumen.to_string(index=False))

os.makedirs("./results/metrics", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
path = "./results/metrics/eval_generalisation_" + timestamp + ".xlsx"
with pd.ExcelWriter(path) as writer:
    df.to_excel(writer,      sheet_name="Escenarios", index=False)
    resumen.to_excel(writer, sheet_name="Resumen",    index=False)
print("Guardado en " + path)

if os.path.exists(CHECKPOINT_FILE):
    os.remove(CHECKPOINT_FILE)
