import cv2
import mediapipe as mp
import math
import requests
from datetime import datetime
from flask import Flask, Response
from export.exporter import guardar_detalle, guardar_resumen
from core.clasificador import Clasificador
from comparison.comparison_evaluator import ComparisonEvaluator
import threading
import time

# Flask App
app = Flask(__name__)

# Variables globales
frame_actual = None
frame_data = []
lock = threading.Lock()

# MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Parámetros del usuario
user_id = input("🧍 Ingrese el ID o nombre del usuario: ")
tiene_lesion = input("¿El paciente tiene una lesión? (s/n): ").strip().lower()
modo_comparativo = tiene_lesion == "s"


def calcular_angulo(a, b, c):
    angulo = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) -
        math.atan2(a[1] - b[1], a[0] - b[0])
    )
    angulo = abs(angulo)
    if angulo > 180:
        angulo = 360 - angulo
    return angulo


def enviar_sesion(user_id, left_elbow, right_elbow, left_knee, right_knee, prediccion):
    url = "http://localhost:5000/api/sesiones"
    data = {
        "userId": user_id,
        "timestamp": datetime.now().isoformat(),
        "leftElbow": round(left_elbow, 2),
        "rightElbow": round(right_elbow, 2),
        "leftKnee": round(left_knee, 2),
        "rightKnee": round(right_knee, 2),
        "prediccion": prediccion
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("✅ Sesión enviada correctamente al microservicio.")
        else:
            print(f"⚠️ Error al enviar sesión: {response.status_code}")
    except Exception as e:
        print(f"❌ Fallo en la conexión al microservicio: {e}")


def procesar_frame(frame):
    global frame_data
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            # Coordenadas
            shoulder_l = [landmarks[11].x, landmarks[11].y]
            elbow_l = [landmarks[13].x, landmarks[13].y]
            wrist_l = [landmarks[15].x, landmarks[15].y]
            shoulder_r = [landmarks[12].x, landmarks[12].y]
            elbow_r = [landmarks[14].x, landmarks[14].y]
            wrist_r = [landmarks[16].x, landmarks[16].y]
            hip_l = [landmarks[23].x, landmarks[23].y]
            knee_l = [landmarks[25].x, landmarks[25].y]
            ankle_l = [landmarks[27].x, landmarks[27].y]
            hip_r = [landmarks[24].x, landmarks[24].y]
            knee_r = [landmarks[26].x, landmarks[26].y]
            ankle_r = [landmarks[28].x, landmarks[28].y]

            # Cálculo
            left_elbow = calcular_angulo(shoulder_l, elbow_l, wrist_l)
            right_elbow = calcular_angulo(shoulder_r, elbow_r, wrist_r)
            left_knee = calcular_angulo(hip_l, knee_l, ankle_l)
            right_knee = calcular_angulo(hip_r, knee_r, ankle_r)

            if modo_comparativo:
                estado_rodillas = ComparisonEvaluator.evaluar_rodillas(
                    left_knee, right_knee)
                estado_codos = ComparisonEvaluator.evaluar_codos(
                    left_elbow, right_elbow)
                pred_label = "incorrecto" if "Asimetria" in estado_rodillas else "correcto"
            else:
                estado_rodillas = f"{Clasificador.movimiento_rodilla(left_knee)} | {Clasificador.movimiento_rodilla(right_knee)}"
                estado_codos = f"{Clasificador.movimiento_codo(left_elbow)} | {Clasificador.movimiento_codo(right_elbow)}"
                pred_label = Clasificador.diagnostico_general(
                    left_knee, right_knee)

            # Dibujar texto
            cv2.putText(image, f"Left Knee: {int(left_knee)}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (
                0, 255, 0) if pred_label == "correcto" else (0, 0, 255), 2)
            cv2.putText(image, f"Right Knee: {int(right_knee)}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (
                0, 255, 0) if pred_label == "correcto" else (0, 0, 255), 2)
            cv2.putText(image, f"Left Elbow: {int(left_elbow)}", (
                20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            cv2.putText(image, f"Right Elbow: {int(right_elbow)}", (
                20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            cv2.putText(image, f"Rodillas: {estado_rodillas}", (20, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (3, 190, 255), 2)
            cv2.putText(image, f"Codos: {estado_codos}", (20, 170),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (3, 190, 255), 2)

            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Guardar frame
            frame_data.append([
                datetime.now().isoformat(),
                left_elbow, right_elbow, left_knee, right_knee, pred_label
            ])
            enviar_sesion(user_id, left_elbow, right_elbow,
                          left_knee, right_knee, pred_label)

        except Exception as e:
            print("⚠️ Error procesando los landmarks:", e)

        return image


def capturar_frames():
    global frame_actual
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        procesado = procesar_frame(frame)
        with lock:
            frame_actual = procesado
        time.sleep(0.03)  # ~30 fps


def generate_stream():
    while True:
        with lock:
            if frame_actual is None:
                continue
            _, buffer = cv2.imencode('.jpg', frame_actual)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.03)


@app.route('/video_feed')
def video_feed():
    return Response(generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return '<h1>Stream en vivo</h1><img src="/video_feed" width="800"/>'


def guardar_salida():
    guardar_detalle(user_id, frame_data)
    if any(row[5] == "incorrecto" for row in frame_data):
        guardar_resumen(user_id, "Posible lesion detectada (asimetria)")


if __name__ == '__main__':
    hilo = threading.Thread(target=capturar_frames)
    hilo.daemon = True
    hilo.start()
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("🔴 Finalizando servidor y guardando resultados...")
        guardar_salida()
