import subprocess
import time
import re
import threading
import sys
import json
import pandas as pd
import os
import shutil
from datetime import datetime

MODELOS = {
    "only_black": "AdrielP/act_only_black",
}
NUM_EPISODIOS = 10
ROBOT_PORT = "/dev/ttyACM0"
CAMERAS = '{"front":{"type":"opencv","index_or_path":0,"width":640,"height":480,"fps":30},"side":{"type":"opencv","index_or_path":2,"width":640,"height":480,"fps":30}}'

CHECKPOINT_FILE = "./results/metrics/checkpoint_only_black.json"

# ── checkpoint helpers ────────────────────────────────────────────────────────

def cargar_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            data = json.load(f)
        print("Checkpoint encontrado: " + str(len(data["resultados"])) + " episodios ya registrados.")
        r = input("Continuar desde episodio " + str(data["proximo_episodio"]) + "? (s/n): ").strip().lower()
        if r == "s":
            return data["resultados"], data["proximo_episodio"]
        else:
            print("Empezando desde cero.")
            os.remove(CHECKPOINT_FILE)
    return [], 1

def guardar_checkpoint(resultados, proximo_episodio):
    os.makedirs(os.path.dirname(CHECKPOINT_FILE), exist_ok=True)
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"resultados": resultados, "proximo_episodio": proximo_episodio}, f, indent=2)

# ── tecla de completado ───────────────────────────────────────────────────────

def esperar_tecla_completado():
    evento = threading.Event()
    resultado = {"tiempo": None}

    def _escuchar():
        print("  >> Robot corriendo... presiona ENTER cuando complete la tarea <<")
        sys.stdin.readline()
        resultado["tiempo"] = datetime.now()
        evento.set()

    hilo = threading.Thread(target=_escuchar, daemon=True)
    hilo.start()
    return evento, resultado

# ── main ──────────────────────────────────────────────────────────────────────

resultados, episodio_inicio = cargar_checkpoint()

for situacion, modelo in MODELOS.items():
    print("\n" + "="*50)
    print("MODELO: " + situacion)
    print("="*50)

    if episodio_inicio == 1:
        input("Prepara la escena para " + situacion + " y presiona ENTER...")
    else:
        input("Continuando desde episodio " + str(episodio_inicio) + ". Prepara la escena y presiona ENTER...")

    for episodio in range(episodio_inicio, NUM_EPISODIOS + 1):
        print("\n--- Episodio " + str(episodio) + "/" + str(NUM_EPISODIOS) + " ---")
        dataset_root = "./data/eval_" + situacion + "_ep" + str(episodio)

        if os.path.exists(dataset_root):
            shutil.rmtree(dataset_root)

        cmd = [
            "lerobot-record",
            "--robot.type=so101_follower",
            "--robot.port=" + ROBOT_PORT,
            "--robot.cameras=" + CAMERAS,
            "--policy.path=" + modelo,
            "--dataset.repo_id=AdrielP/eval_" + situacion,
            "--dataset.root=" + dataset_root,
            "--dataset.single_task=state based cable sorting",
            "--dataset.num_episodes=1",
            "--dataset.episode_time_s=30",
            "--dataset.reset_time_s=10",
            "--dataset.fps=30",
            "--dataset.push_to_hub=false",
            "--play_sounds=false"
        ]

        error_cmd = None
        tiempo_robot_s = None
        tiempo_tarea_s = None

        evento_completado, resultado_tecla = esperar_tecla_completado()

        try:
            result = subprocess.run(cmd, timeout=180, stderr=subprocess.PIPE, text=True)
            log = result.stderr

            pat_inicio = r"INFO (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*Recording episode"
            pat_fin    = r"INFO (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*Stop recording"
            fmt = "%Y-%m-%d %H:%M:%S"

            match_inicio = re.search(pat_inicio, log)
            match_fin    = re.search(pat_fin,    log)

            if match_inicio and match_fin:
                t_inicio = datetime.strptime(match_inicio.group(1), fmt)
                t_fin    = datetime.strptime(match_fin.group(1),    fmt)
                tiempo_robot_s = round((t_fin - t_inicio).total_seconds(), 2)
                print("Tiempo total de ejecucion (log): " + str(tiempo_robot_s) + "s")

                if resultado_tecla["tiempo"] is not None:
                    tiempo_tarea_s = round(
                        (resultado_tecla["tiempo"] - t_inicio).total_seconds(), 2
                    )
                    tiempo_tarea_s = max(0.0, min(tiempo_tarea_s, tiempo_robot_s))
                    print("Tiempo hasta completar tarea (tecla): " + str(tiempo_tarea_s) + "s")
                else:
                    print("AVISO: no se registro tiempo de tarea (no se presiono ENTER)")
            else:
                print("AVISO: no se pudo parsear el log de lerobot")

        except subprocess.TimeoutExpired:
            error_cmd = "timeout"
            print("ADVERTENCIA: timeout excedido.")
        except Exception as e:
            error_cmd = str(e)
            print("Error: " + str(e))

        while True:
            r = input("Exitoso? (s/n): ").strip().lower()
            if r in ["s", "n"]:
                break

        exitoso = r == "s"
        resultados.append({
            "modelo": situacion,
            "episodio": episodio,
            "exitoso": exitoso,
            "tiempo_tarea_s": tiempo_tarea_s,
            "tiempo_total_s": tiempo_robot_s,
            "error": error_cmd or "",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print("EXITO" if exitoso else "FALLO")

        # Guardar checkpoint despues de cada episodio
        guardar_checkpoint(resultados, episodio + 1)
        print("Checkpoint guardado (episodio " + str(episodio) + " completado)")

        if episodio < NUM_EPISODIOS:
            input("Prepara siguiente escena y presiona ENTER...")

# ── resultados finales ────────────────────────────────────────────────────────

df = pd.DataFrame(resultados)
resumen = df.groupby("modelo").agg(
    exitosos=("exitoso", "sum"),
    total=("exitoso", "count"),
    success_rate=("exitoso", lambda x: round(x.mean() * 100, 1)),
    tiempo_tarea_promedio_s=("tiempo_tarea_s", lambda x: round(x.dropna().mean(), 2) if x.notna().any() else None),
    tiempo_total_promedio_s=("tiempo_total_s", lambda x: round(x.mean(), 2))
).reset_index()

print("\nRESULTADOS FINALES")
print(resumen.to_string(index=False))

os.makedirs("./results/metrics", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
path = "./results/metrics/eval_results_" + timestamp + ".xlsx"
with pd.ExcelWriter(path) as writer:
    df.to_excel(writer, sheet_name="Episodios", index=False)
    resumen.to_excel(writer, sheet_name="Resumen", index=False)
print("Guardado en " + path)

# Borrar checkpoint al terminar exitosamente
if os.path.exists(CHECKPOINT_FILE):
    os.remove(CHECKPOINT_FILE)
    print("Checkpoint eliminado (evaluacion completa)")