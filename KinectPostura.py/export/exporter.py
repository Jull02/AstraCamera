# Archivo: exporter.py

import os
import csv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def crear_carpetas_base(user_id):
    base_path = os.path.join(BASE_DIR, "Pacientes", f"Paciente_{user_id}")
    detalle_path = os.path.join(base_path, "detalle")
    resumen_path = os.path.join(base_path, "resumen")
    os.makedirs(detalle_path, exist_ok=True)
    os.makedirs(resumen_path, exist_ok=True)
    return detalle_path, resumen_path


def guardar_detalle(user_id, frame_data):
    detalle_path, _ = crear_carpetas_base(user_id)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(detalle_path, f"sesion_{timestamp}.csv")
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "LeftElbow", "RightElbow",
                        "LeftKnee", "RightKnee", "Prediccion"])
        for row in frame_data:
            writer.writerow(row)
    print(f"📁 Detalle guardado en {filename}")


def guardar_resumen(user_id, resumen_data):
    _, resumen_path = crear_carpetas_base(user_id)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(resumen_path, f"resumen_{timestamp}.csv")
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["UserId", "Fecha", "Diagnostico"])
        writer.writerow([user_id, datetime.now().isoformat(), resumen_data])
    print(f"📁 Resumen guardado en {filename}")
