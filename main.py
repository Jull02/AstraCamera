import cv2
import mediapipe as mp
import math
import requests
from datetime import datetime

# Inicializar MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Captura del ID del usuario
user_id = input("Ingrese el ID o nombre del usuario: ")


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


# Captura desde cámara
cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Recolorar imagen a RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Detección
        results = pose.process(image)

        # Recolorar de nuevo a BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extraer landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Obtener puntos clave
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

            # Calcular ángulos
            left_elbow = calcular_angulo(shoulder_l, elbow_l, wrist_l)
            right_elbow = calcular_angulo(shoulder_r, elbow_r, wrist_r)
            left_knee = calcular_angulo(hip_l, knee_l, ankle_l)
            right_knee = calcular_angulo(hip_r, knee_r, ankle_r)

            # Clasificación simple
            pred_label = "correcto" if 80 <= left_knee <= 110 and 80 <= right_knee <= 110 else "incorrecto"

            # Mostrar en pantalla
            cv2.putText(image, f"Left Knee: {int(left_knee)}", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0) if pred_label == "correcto" else (0, 0, 255), 2)
            cv2.putText(image, f"Right Knee: {int(right_knee)}", (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0) if pred_label == "correcto" else (0, 0, 255), 2)

            # Enviar datos al microservicio
            enviar_sesion(user_id, left_elbow, right_elbow,
                          left_knee, right_knee, pred_label)

        except Exception as e:
            print("⚠️ Error procesando los landmarks:", e)

        # Renderizar landmarks
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow("Evaluacion de Postura", image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
